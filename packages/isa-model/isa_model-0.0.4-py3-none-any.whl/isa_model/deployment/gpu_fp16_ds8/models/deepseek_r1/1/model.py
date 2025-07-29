import json
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os 
import triton_python_backend_utils as pb_utils

class TritonPythonModel:
    def initialize(self, args):
        """初始化模型"""
        self.model_config = json.loads(args['model_config'])
        
        # --- START: CORRECTED PATH LOGIC ---

        # model_repository 是父目录, e.g., /models/deepseek_r1
        model_repository = args['model_repository']
        # model_version 是版本号, e.g., '1'
        model_version = args['model_version']
        
        # 将它们拼接成指向模型文件的确切路径
        model_path = os.path.join(model_repository, model_version)

        print(f"Loading model from specific version path: {model_path}")

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path,  # 从正确的版本目录加载
            trust_remote_code=True
        )
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,  # 从正确的版本目录加载
            torch_dtype=torch.bfloat16, 
            device_map="gpu",           
            trust_remote_code=True
        )
        
        # --- END: CORRECTED PATH LOGIC ---
        
        # ... (您代码的其余部分保持不变) ...
        output_config = pb_utils.get_output_config_by_name(
            self.model_config, "OUTPUT_TEXT"
        )
        self.output_dtype = pb_utils.triton_string_to_numpy(
            output_config['data_type']
        )
        
        self.generation_config = {
            'max_new_tokens': 512,
            'temperature': 0.7,
            'do_sample': True,
            'top_p': 0.9,
            'repetition_penalty': 1.1,
            'pad_token_id': self.tokenizer.eos_token_id
        }
        
        print("Model loaded successfully!")
    
    def execute(self, requests):
        """执行推理"""
        responses = []
        
        for request in requests:
            # 获取输入文本
            input_text = pb_utils.get_input_tensor_by_name(
                request, "INPUT_TEXT"
            ).as_numpy()
            
            # 解码输入文本
            input_texts = [text.decode('utf-8') for text in input_text.flatten()]
            
            # 批量推理
            output_texts = []
            for text in input_texts:
                try:
                    # 编码输入
                    inputs = self.tokenizer.encode(
                        text, 
                        return_tensors="pt"
                    ).to(self.model.device)
                    
                    # 生成响应
                    with torch.no_grad():
                        outputs = self.model.generate(
                            inputs,
                            **self.generation_config
                        )
                    
                    # 解码输出
                    response = self.tokenizer.decode(
                        outputs[0][inputs.shape[-1]:], 
                        skip_special_tokens=True
                    )
                    
                    output_texts.append(response)
                    
                except Exception as e:
                    print(f"Error processing text: {e}")
                    output_texts.append(f"Error: {str(e)}")
            
            # 准备输出
            output_texts_np = np.array(
                [[text.encode('utf-8')] for text in output_texts], 
                dtype=object
            )
            
            output_tensor = pb_utils.Tensor(
                "OUTPUT_TEXT", 
                output_texts_np.astype(self.output_dtype)
            )
            
            response = pb_utils.InferenceResponse(
                output_tensors=[output_tensor]
            )
            responses.append(response)
        
        return responses
    
    def finalize(self):
        """清理资源"""
        print("Cleaning up...")