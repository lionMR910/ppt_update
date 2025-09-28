#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云百炼大模型接口测试程序
测试DashScope API的各种功能和响应情况
"""

import os
import time
import json
from datetime import datetime
from openai import OpenAI


class DashScopeAPITester:
    def __init__(self, api_key=None):
        """初始化测试器"""
        self.api_key = api_key or "sk-3739d12ced0a41b4b12881f2e7fc1209"
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.client = None
        self.test_results = []
    
    def safe_extract_response(self, completion):
        """安全提取API响应内容"""
        if completion is None:
            raise Exception("API响应为空")
        if not hasattr(completion, 'choices') or not completion.choices:
            raise Exception("API响应中没有choices")
        if len(completion.choices) == 0:
            raise Exception("API响应choices为空列表")
        if not completion.choices[0].message:
            raise Exception("API响应中没有message")
        
        content = completion.choices[0].message.content
        model_name = getattr(completion, 'model', 'unknown')
        
        return content, model_name
        
    def initialize_client(self):
        """初始化OpenAI客户端"""
        try:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
            )
            print("✓ 客户端初始化成功")
            return True
        except Exception as e:
            print(f"✗ 客户端初始化失败: {str(e)}")
            return False
    
    def test_basic_chat(self):
        """测试基本的对话功能"""
        print("\n" + "="*50)
        print("测试1: 基本对话功能")
        print("="*50)
        
        try:
            start_time = time.time()
            completion = self.client.chat.completions.create(
                model="qwen-plus",
                messages=[
                    {"role": "system", "content": "你是一个有帮助的AI助手。"},
                    {"role": "user", "content": "你是谁？请简单介绍一下自己。"},
                ],
            )
            end_time = time.time()
            
            response_time = end_time - start_time
            
            # 安全提取响应内容
            response_content, model_name = self.safe_extract_response(completion)
            
            print(f"✓ 请求成功")
            print(f"响应时间: {response_time:.2f}秒")
            print(f"模型: {model_name}")
            print(f"响应内容: {response_content[:200] if response_content else '(空响应)'}...")
            
            # 记录测试结果
            self.test_results.append({
                "test": "基本对话功能",
                "status": "成功",
                "response_time": response_time,
                "model": model_name,
                "content_length": len(response_content)
            })
            
            return True
            
        except Exception as e:
            print(f"✗ 测试失败: {str(e)}")
            self.test_results.append({
                "test": "基本对话功能", 
                "status": "失败",
                "error": str(e)
            })
            return False
    
    def test_chinese_processing(self):
        """测试中文处理能力"""
        print("\n" + "="*50)
        print("测试2: 中文处理能力")
        print("="*50)
        
        try:
            start_time = time.time()
            completion = self.client.chat.completions.create(
                model="qwen-plus",
                messages=[
                    {"role": "system", "content": "你是一个专业的中文助手。"},
                    {"role": "user", "content": "请用中文解释什么是人工智能，并举一个生活中的应用例子。"},
                ],
            )
            end_time = time.time()
            
            response_time = end_time - start_time
            
            # 安全提取响应内容
            response_content, model_name = self.safe_extract_response(completion)
            
            print(f"✓ 中文处理测试成功")
            print(f"响应时间: {response_time:.2f}秒")
            print(f"响应内容: {response_content[:300] if response_content else '(空响应)'}...")
            
            self.test_results.append({
                "test": "中文处理能力",
                "status": "成功", 
                "response_time": response_time,
                "content_length": len(response_content)
            })
            
            return True
            
        except Exception as e:
            print(f"✗ 中文处理测试失败: {str(e)}")
            self.test_results.append({
                "test": "中文处理能力",
                "status": "失败",
                "error": str(e)
            })
            return False
    
    def test_data_analysis_task(self):
        """测试数据分析任务"""
        print("\n" + "="*50)
        print("测试3: 数据分析任务")
        print("="*50)
        
        try:
            start_time = time.time()
            completion = self.client.chat.completions.create(
                model="qwen-plus",
                messages=[
                    {"role": "system", "content": "你是一个专业的数据分析师。"},
                    {"role": "user", "content": """
                    请分析以下销售数据并给出结论：
                    1月销量: 1000件
                    2月销量: 1200件  
                    3月销量: 800件
                    4月销量: 1500件
                    5月销量: 1300件
                    
                    请分析销量趋势并提出建议。
                    """},
                ],
            )
            end_time = time.time()
            
            response_time = end_time - start_time
            
            # 安全提取响应内容
            response_content, model_name = self.safe_extract_response(completion)
            
            print(f"✓ 数据分析测试成功")
            print(f"响应时间: {response_time:.2f}秒")
            print(f"分析结果: {response_content[:400] if response_content else '(空响应)'}...")
            
            self.test_results.append({
                "test": "数据分析任务",
                "status": "成功",
                "response_time": response_time,
                "content_length": len(response_content)
            })
            
            return True
            
        except Exception as e:
            print(f"✗ 数据分析测试失败: {str(e)}")
            self.test_results.append({
                "test": "数据分析任务",
                "status": "失败", 
                "error": str(e)
            })
            return False
    
    def test_multiple_messages(self):
        """测试多轮对话"""
        print("\n" + "="*50)
        print("测试4: 多轮对话")
        print("="*50)
        
        try:
            start_time = time.time()
            completion = self.client.chat.completions.create(
                model="qwen-plus",
                messages=[
                    {"role": "system", "content": "你是一个有帮助的助手。"},
                    {"role": "user", "content": "请告诉我北京的天气如何？"},
                    {"role": "assistant", "content": "我无法获取实时天气信息，建议您查看天气预报应用获取准确信息。"},
                    {"role": "user", "content": "那你能推荐一些查看天气的应用吗？"},
                ],
            )
            end_time = time.time()
            
            response_time = end_time - start_time
            
            # 安全提取响应内容
            response_content, model_name = self.safe_extract_response(completion)
            
            print(f"✓ 多轮对话测试成功")
            print(f"响应时间: {response_time:.2f}秒")
            print(f"推荐内容: {response_content[:300] if response_content else '(空响应)'}...")
            
            self.test_results.append({
                "test": "多轮对话",
                "status": "成功",
                "response_time": response_time,
                "content_length": len(response_content)
            })
            
            return True
            
        except Exception as e:
            print(f"✗ 多轮对话测试失败: {str(e)}")
            self.test_results.append({
                "test": "多轮对话",
                "status": "失败",
                "error": str(e)
            })
            return False
    
    def test_different_models(self):
        """测试不同模型"""
        print("\n" + "="*50)
        print("测试5: 不同模型测试")
        print("="*50)
        
        models_to_test = ["qwen-plus", "qwen-turbo", "qwen-max"]
        
        for model in models_to_test:
            try:
                print(f"\n测试模型: {model}")
                start_time = time.time()
                completion = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "你是一个AI助手。"},
                        {"role": "user", "content": "请用一句话介绍你使用的模型。"},
                    ],
                )
                end_time = time.time()
                
                response_time = end_time - start_time
                
                # 安全提取响应内容
                response_content, model_name = self.safe_extract_response(completion)
                
                print(f"  ✓ {model} 测试成功")
                print(f"  响应时间: {response_time:.2f}秒")
                print(f"  响应: {response_content[:150] if response_content else '(空响应)'}...")
                
                self.test_results.append({
                    "test": f"模型_{model}",
                    "status": "成功",
                    "response_time": response_time,
                    "model": model_name,
                    "content_length": len(response_content)
                })
                
            except Exception as e:
                print(f"  ✗ {model} 测试失败: {str(e)}")
                self.test_results.append({
                    "test": f"模型_{model}",
                    "status": "失败",
                    "model": model,
                    "error": str(e)
                })
    
    def test_error_handling(self):
        """测试错误处理"""
        print("\n" + "="*50)
        print("测试6: 错误处理")
        print("="*50)
        
        # 测试无效模型
        try:
            print("测试无效模型...")
            completion = self.client.chat.completions.create(
                model="invalid-model",
                messages=[
                    {"role": "user", "content": "测试"},
                ],
            )
            print("✗ 应该返回错误，但成功了")
            
        except Exception as e:
            print(f"✓ 正确捕获模型错误: {str(e)[:100]}...")
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "="*60)
        print("测试报告")
        print("="*60)
        
        total_tests = len(self.test_results)
        successful_tests = len([r for r in self.test_results if r["status"] == "成功"])
        failed_tests = total_tests - successful_tests
        
        print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"总测试数: {total_tests}")
        print(f"成功测试: {successful_tests}")
        print(f"失败测试: {failed_tests}")
        print(f"成功率: {(successful_tests/total_tests*100):.1f}%" if total_tests > 0 else "无测试")
        
        if successful_tests > 0:
            avg_response_time = sum([r.get("response_time", 0) for r in self.test_results if r["status"] == "成功"]) / successful_tests
            print(f"平均响应时间: {avg_response_time:.2f}秒")
        
        # 详细结果
        print("\n详细测试结果:")
        print("-" * 40)
        for result in self.test_results:
            status_symbol = "✓" if result["status"] == "成功" else "✗"
            print(f"{status_symbol} {result['test']}: {result['status']}")
            if result["status"] == "成功" and "response_time" in result:
                print(f"  响应时间: {result['response_time']:.2f}秒")
            elif result["status"] == "失败":
                print(f"  错误: {result.get('error', 'Unknown error')[:100]}...")
        
        # 保存报告到文件
        report_data = {
            "test_time": datetime.now().isoformat(),
            "summary": {
                "total": total_tests,
                "successful": successful_tests,
                "failed": failed_tests,
                "success_rate": (successful_tests/total_tests*100) if total_tests > 0 else 0
            },
            "details": self.test_results
        }
        
        with open("dashscope_test_report.json", "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n测试报告已保存到: dashscope_test_report.json")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("阿里云百炼大模型API测试开始")
        print("="*60)
        
        # 初始化客户端
        if not self.initialize_client():
            print("客户端初始化失败，无法进行测试")
            return
        
        # 运行各项测试
        test_functions = [
            self.test_basic_chat,
            self.test_chinese_processing,
            self.test_data_analysis_task,
            self.test_multiple_messages,
            self.test_different_models,
            self.test_error_handling,
        ]
        
        for test_func in test_functions:
            try:
                test_func()
                time.sleep(1)  # 避免请求过快
            except Exception as e:
                print(f"测试执行错误: {str(e)}")
        
        # 生成报告
        self.generate_report()


def main():
    """主函数"""
    print("DashScope API 测试程序")
    print("API Key: sk-3739d12ced0a41b4b12881f2e7fc1209")
    print("Base URL: https://dashscope.aliyuncs.com/compatible-mode/v1")
    
    # 创建测试器并运行测试
    tester = DashScopeAPITester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
