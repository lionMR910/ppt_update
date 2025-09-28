# AI分析模块

import requests
import json
import time
import random
from typing import Optional, Tuple, List
from config import MODEL_CONFIG, VERIFICATION_CONFIG
from analysis_data_text_order import analysis_data_text
from precise_corrector import PreciseCorrector


class AIAnalyzer:
    def __init__(self):
        self.base_url = MODEL_CONFIG['base_url']
        self.model_name = MODEL_CONFIG['llm_model']
        self.timeout = MODEL_CONFIG['timeout']
        self.max_retries = MODEL_CONFIG['max_retries']
        # API key从配置文件获取
        self.api_key = MODEL_CONFIG.get('api_key', 'sk-XIval4xD5HWrvG7956C534B6Cd7348C2B22dFc22B1Ca308e')
        # 根据配置决定是否初始化精确修正器
        self.enable_verification = VERIFICATION_CONFIG.get('enable_verification', True)
        self.corrector = PreciseCorrector() if self.enable_verification else None
    
    def analyze_data(self, task_info: dict, data_content: str) -> Optional[str]:
        """调用专业分析函数进行数据分析，并进行验证和修正"""
        
        print(f"🤖 开始AI分析: {task_info.get('anaylsis_name', '未知任务')}")
        
        # 构建用户输入
        user_input = f"请分析{task_info.get('anaylsis_name', '数据')}，分析月份：{task_info.get('op_month', '未知')}"
        
        # 生成对话ID
        conversation_uid = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        
        # 重试机制
        original_result = None
        for attempt in range(self.max_retries):
            try:
                # 调用专业分析函数
                result = analysis_data_text(
                    api_key=self.api_key,
                    user_input=user_input,
                    conversation_uid=conversation_uid,
                    chart_obj=data_content
                )
                
                if result and isinstance(result, str) and result.strip():
                    original_result = result.strip()
                    print(f"✓ AI分析完成")
                    break
                else:
                    print(f"⚠️ 第 {attempt + 1} 次尝试失败，准备重试...")
                    
            except Exception as e:
                print(f"❌ 第 {attempt + 1} 次调用失败: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2)  # 等待2秒后重试
        
        if not original_result:
            print(f"❌ AI分析失败，已重试 {self.max_retries} 次")
            return None
        
        # 进行精确数据修正（如果启用）
        if self.enable_verification and self.corrector:
            try:
                corrected_result, corrections = self.corrector.correct_data_errors(
                    original_result, data_content
                )
                
                if corrections:
                    print(f"🔧 完成 {len(corrections)} 项数据修正，格式保持不变")
                    for correction in corrections:
                        print(f"   - {correction}")
                
                return corrected_result
                
            except Exception as e:
                print(f"⚠️ 数据修正过程出错: {e}")
                print("📝 使用原始分析结果")
                return original_result
        else:
            print("📝 数据修正功能已禁用，使用原始分析结果")
            return original_result
    
    def test_connection(self) -> bool:
        """测试AI服务连接"""
        try:
            # 使用简单的测试数据验证分析函数
            test_data = """地市\t测试指标
沈阳\t100
大连\t90"""
            
            test_result = analysis_data_text(
                api_key=self.api_key,
                user_input="测试连接",
                conversation_uid="test123",
                chart_obj=test_data
            )
            
            if test_result:
                print("✓ AI分析服务连接正常")
                return True
            else:
                print("❌ AI分析服务连接失败")
                return False
                
        except Exception as e:
            print(f"❌ AI服务连接测试失败: {e}")
            return False