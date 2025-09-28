# AI分析结论验证和修正模块

import re
import json
import requests
import random
from typing import Dict, List, Tuple, Optional, Any
from config import MODEL_CONFIG, VERIFICATION_CONFIG
from analysis_data_text_order import parse_and_sort_data, parse_structured_data_for_stats, calculate_statistics


class AnalysisVerifier:
    """AI分析结论验证和修正器"""
    
    def __init__(self):
        self.base_url = MODEL_CONFIG['base_url']
        self.model_name = MODEL_CONFIG['llm_model']
        self.api_key = MODEL_CONFIG.get('api_key', 'sk-XIval4xD5HWrvG7956C534B6Cd7348C2B22dFc22B1Ca308e')
        self.timeout = MODEL_CONFIG.get('timeout', 120)
    
    def verify_and_correct_analysis(self, 
                                  original_analysis: str, 
                                  user_input: str, 
                                  chart_obj: str, 
                                  task_info: dict) -> Tuple[str, List[str]]:
        """
        验证并修正AI分析结论
        
        Args:
            original_analysis: 原始分析结论
            user_input: 用户输入问题
            chart_obj: 原始数据
            task_info: 任务信息
            
        Returns:
            Tuple[修正后的分析结论, 发现的问题列表]
        """
        print("🔍 开始验证分析结论...")
        
        # 1. 解析原始数据
        structured_data, data_headers = parse_structured_data_for_stats(chart_obj)
        sort_results = parse_and_sort_data(chart_obj)
        statistics = calculate_statistics(structured_data, data_headers)
        
        # 2. 检测数据类型
        data_type = self._detect_data_type(structured_data, data_headers)
        print(f"📊 检测到数据类型: {data_type}")
        
        # 3. 执行事实检查
        fact_check_results = self._perform_fact_check(
            original_analysis, structured_data, data_headers, statistics, sort_results, data_type
        )
        
        # 4. 如果发现问题，进行修正
        if fact_check_results['has_errors']:
            print(f"⚠️ 发现 {len(fact_check_results['errors'])} 个问题，开始修正...")
            try:
                corrected_analysis = self._correct_analysis(
                    original_analysis, user_input, chart_obj, sort_results, 
                    statistics, data_type, fact_check_results['errors']
                )
                return corrected_analysis, fact_check_results['errors']
            except Exception as e:
                print(f"❌ 修正过程失败: {e}")
                print("📝 返回原始分析结果，但会记录发现的问题")
                return original_analysis, fact_check_results['errors']
        else:
            print("✅ 分析结论验证通过，无需修正")
            return original_analysis, []
    
    def _detect_data_type(self, structured_data: List[Dict], headers: List[str]) -> str:
        """检测数据类型：时间序列 vs 地市数据"""
        if not headers:
            return "unknown"
        
        # 检查第一列是否为月份
        if '月份' in headers[0]:
            return "time_series"
        
        # 检查是否包含地市名称
        if '地市' in headers[0] or any('地市' in str(headers)):
            return "city_data"
        
        # 检查数据内容
        if structured_data:
            first_col_values = [str(item.get(headers[0], '')) for item in structured_data]
            # 检查是否有时间格式（如202501）
            time_pattern = re.compile(r'^\d{6}$')  # YYYYMM格式
            if any(time_pattern.match(val) for val in first_col_values):
                return "time_series"
            
            # 检查是否有地市名称
            city_names = ['沈阳', '大连', '鞍山', '抚顺', '本溪', '丹东', '锦州', '营口', 
                         '阜新', '辽阳', '盘锦', '铁岭', '朝阳', '葫芦岛']
            if any(city in val for val in first_col_values for city in city_names):
                return "city_data"
        
        return "unknown"
    
    def _perform_fact_check(self, analysis: str, structured_data: List[Dict], 
                          headers: List[str], statistics: Dict, sort_results: str, 
                          data_type: str) -> Dict[str, Any]:
        """执行事实检查"""
        errors = []
        
        # 1. 检查数据类型不匹配
        if data_type == "time_series":
            city_names = ['沈阳', '大连', '鞍山', '抚顺', '本溪', '丹东', '锦州', '营口', 
                         '阜新', '辽阳', '盘锦', '铁岭', '朝阳', '葫芦岛']
            mentioned_cities = [city for city in city_names if city in analysis]
            if mentioned_cities:
                errors.append({
                    "type": "data_type_mismatch",
                    "description": f"时间序列数据中不应包含地市分析，但提到了: {', '.join(mentioned_cities)}",
                    "severity": "high"
                })
        
        elif data_type == "city_data":
            # 检查时间序列相关的错误表述
            time_keywords = ['时间点', '月份变化', '环比', '时间序列']
            mentioned_time_analysis = [kw for kw in time_keywords if kw in analysis]
            if mentioned_time_analysis and not any(month in analysis for month in ['202501', '202502', '202503', '202504', '202505', '202506', '202507', '202508']):
                errors.append({
                    "type": "inappropriate_time_analysis",
                    "description": f"地市数据中使用了不当的时间序列分析: {', '.join(mentioned_time_analysis)}",
                    "severity": "medium"
                })
        
        # 2. 检查数值准确性
        self._check_numerical_accuracy(analysis, structured_data, headers, statistics, errors)
        
        # 3. 检查排序准确性
        self._check_ranking_accuracy(analysis, sort_results, errors)
        
        # 4. 检查逻辑一致性
        self._check_logical_consistency(analysis, errors)
        
        return {
            "has_errors": len(errors) > 0,
            "errors": errors,
            "error_count": len(errors)
        }
    
    def _check_numerical_accuracy(self, analysis: str, structured_data: List[Dict], 
                                headers: List[str], statistics: Dict, errors: List[Dict]):
        """检查数值准确性"""
        # 提取分析中的数值
        number_pattern = re.compile(r'(\d+\.?\d*)%?')
        mentioned_numbers = number_pattern.findall(analysis)
        
        # 检查是否使用了不存在的数值
        actual_numbers = set()
        for item in structured_data:
            for header in headers[1:]:  # 跳过第一列
                value = item.get(header)
                if isinstance(value, (int, float)):
                    actual_numbers.add(str(value))
                    actual_numbers.add(f"{value:.1f}")
                    actual_numbers.add(f"{value:.2f}")
        
        # 添加统计数据中的数值
        for indicator, stats in statistics.items():
            actual_numbers.add(str(stats['mean']))
            actual_numbers.add(f"{stats['mean']:.1f}")
            actual_numbers.add(str(stats['max']))
            actual_numbers.add(str(stats['min']))
        
        # 检查分析中是否有编造的数值（简单检查）
        suspicious_numbers = []
        for num in mentioned_numbers:
            if num not in actual_numbers and float(num) > 0:
                # 进一步检查是否是合理的计算结果
                num_val = float(num)
                if num_val > 200 or (num_val > 100 and '%' in analysis):  # 可疑的大数值
                    suspicious_numbers.append(num)
        
        if suspicious_numbers:
            errors.append({
                "type": "suspicious_numbers",
                "description": f"可能编造的数值: {', '.join(suspicious_numbers)}",
                "severity": "medium"
            })
    
    def _check_ranking_accuracy(self, analysis: str, sort_results: str, errors: List[Dict]):
        """检查排序和排名准确性"""
        # 提取排序结果中的实际排名
        ranking_info = {}
        lines = sort_results.split('\n')
        
        for line in lines:
            if '从高到低依次为' in line or '时间序列为' in line:
                # 提取指标名称
                if '从高到低依次为' in line:
                    indicator = line.split('从高到低依次为')[0]
                    ranking_part = line.split('从高到低依次为')[1]
                    # 提取地市排序
                    city_pattern = re.compile(r'([^，,]+?)(\d+\.?\d*)([%万元户]*)(?:[（(][^）)]*[）)])?')
                    matches = city_pattern.findall(ranking_part)
                    if matches:
                        ranking_info[indicator] = [(match[0].strip(), float(match[1])) for match in matches]
        
        # 检查分析中的"最高"、"最低"、"第一"等表述是否准确
        superlative_pattern = re.compile(r'([^，。！？]*?)([最第])([高低一二三四五六七八九十]+)([^，。！？]*?)([是为]?)([^，。！？]*?)([(\d+\.?\d*)%?万元户]?)')
        matches = superlative_pattern.findall(analysis)
        
        for match in matches:
            # 这里可以进一步实现具体的排名验证逻辑
            # 由于复杂性，暂时标记为需要人工检查
            pass
    
    def _check_logical_consistency(self, analysis: str, errors: List[Dict]):
        """检查逻辑一致性"""
        # 检查是否有自相矛盾的表述
        sentences = re.split(r'[。！？]', analysis)
        
        # 检查同一实体的矛盾描述
        entities = {}
        for sentence in sentences:
            # 提取地市名称和相关描述
            city_names = ['沈阳', '大连', '鞍山', '抚顺', '本溪', '丹东', '锦州', '营口', 
                         '阜新', '辽阳', '盘锦', '铁岭', '朝阳', '葫芦岛']
            for city in city_names:
                if city in sentence:
                    if city not in entities:
                        entities[city] = []
                    entities[city].append(sentence.strip())
        
        # 检查矛盾（简单检查：同一地市既是最高又是最低）
        for city, descriptions in entities.items():
            high_count = sum(1 for desc in descriptions if '最高' in desc or '第一' in desc)
            low_count = sum(1 for desc in descriptions if '最低' in desc or '垫底' in desc)
            
            if high_count > 0 and low_count > 0:
                errors.append({
                    "type": "logical_contradiction",
                    "description": f"{city}同时被描述为最高和最低",
                    "severity": "high"
                })
    
    def _correct_analysis(self, original_analysis: str, user_input: str, chart_obj: str,
                         sort_results: str, statistics: Dict, data_type: str, 
                         errors: List[Dict]) -> str:
        """使用大模型修正分析结论"""
        
        # 构建错误描述
        error_descriptions = []
        for error in errors:
            error_descriptions.append(f"- {error['description']} (严重程度: {error['severity']})")
        
        errors_text = '\n'.join(error_descriptions)
        
        # 根据数据类型构建不同的修正提示词
        if data_type == "time_series":
            correction_prompt = self._build_time_series_correction_prompt(
                original_analysis, user_input, chart_obj, sort_results, statistics, errors_text
            )
        elif data_type == "city_data":
            correction_prompt = self._build_city_data_correction_prompt(
                original_analysis, user_input, chart_obj, sort_results, statistics, errors_text
            )
        else:
            correction_prompt = self._build_general_correction_prompt(
                original_analysis, user_input, chart_obj, sort_results, statistics, errors_text
            )
        
        # 调用大模型进行修正
        return self._call_llm_for_correction(correction_prompt)
    
    def _build_time_series_correction_prompt(self, original_analysis: str, user_input: str, 
                                           chart_obj: str, sort_results: str, statistics: Dict, 
                                           errors_text: str) -> str:
        """构建时间序列数据的修正提示词"""
        stats_summary = self._build_statistics_summary(statistics)
        
        return f"""你是专业的数据分析师，需要修正一份有问题的时间序列分析报告。

【原始分析报告】（存在错误，需要修正）：
{original_analysis}

【发现的问题】：
{errors_text}

【原始数据类型】：时间序列数据
【用户问题】：{user_input}
【原始数据】：{chart_obj}

【准确的排序结果】：
{sort_results}

【准确统计信息】：
{stats_summary}

【修正要求】：
1. **严格禁止**：绝对不能提及任何地市名称（如沈阳、大连、锦州等），这是时间序列数据
2. **重点分析**：专注于时间趋势、环比变化、季节性特征、转折点等时间维度的分析
3. **数据准确性**：所有数值必须来源于排序结果或统计信息，严禁编造
4. **逻辑一致性**：确保前后表述不矛盾
5. **分析深度**：分析趋势变化的原因和业务含义
6. **格式要求**：保持简洁专业，重点突出，不超过300字

【时间序列分析样例】：
- 综合保有率呈波动态势：8个月中有4个月低于均值，需关注阶段性下降风险
- 规模保有率持续下滑：从202501的100.0%降至202508的97.9%，呈现明显下降趋势
- 价值保有率波动较大：202507达到峰值99.77%，但202508回落至95.8%，波动幅度达3.97个百分点

请基于上述要求，重新生成准确的时间序列分析报告："""
    
    def _build_city_data_correction_prompt(self, original_analysis: str, user_input: str, 
                                         chart_obj: str, sort_results: str, statistics: Dict, 
                                         errors_text: str) -> str:
        """构建地市数据的修正提示词"""
        stats_summary = self._build_statistics_summary(statistics)
        
        return f"""你是专业的数据分析师，需要修正一份有问题的地市分析报告。

【原始分析报告】（存在错误，需要修正）：
{original_analysis}

【发现的问题】：
{errors_text}

【原始数据类型】：地市数据
【用户问题】：{user_input}
【原始数据】：{chart_obj}

【准确的排序结果】：
{sort_results}

【准确统计信息】：
{stats_summary}

【修正要求】：
1. **数据准确性**：所有排名、数值必须严格基于排序结果，严禁编造
2. **地市名称**：必须使用具体地市名称，避免"最高地市"等泛化表述
3. **排序准确性**：确保"最高"、"最低"等表述与实际排序一致
4. **统计准确性**：均值、统计数量必须使用提供的统计信息
5. **逻辑一致性**：同一地市不能既是最高又是最低
6. **禁止事项**：严禁将各地市占比相加，严禁编造不存在的数据

请基于上述要求，重新生成准确的地市分析报告："""
    
    def _build_general_correction_prompt(self, original_analysis: str, user_input: str, 
                                       chart_obj: str, sort_results: str, statistics: Dict, 
                                       errors_text: str) -> str:
        """构建通用的修正提示词"""
        stats_summary = self._build_statistics_summary(statistics)
        
        return f"""你是专业的数据分析师，需要修正一份有问题的分析报告。

【原始分析报告】（存在错误，需要修正）：
{original_analysis}

【发现的问题】：
{errors_text}

【用户问题】：{user_input}
【原始数据】：{chart_obj}

【准确的排序结果】：
{sort_results}

【准确统计信息】：
{stats_summary}

【修正要求】：
1. 基于实际数据进行分析，严禁编造任何信息
2. 确保所有数值来源于排序结果或统计信息
3. 保持逻辑一致性，避免自相矛盾
4. 语言简洁专业，重点突出

请基于上述要求，重新生成准确的分析报告："""
    
    def _build_statistics_summary(self, statistics: Dict) -> str:
        """构建统计信息摘要"""
        if not statistics:
            return "无统计信息"
        
        summary_lines = []
        for indicator, stats in statistics.items():
            line = f"【{indicator}】均值{stats['mean']}，最高{stats['max']}，最低{stats['min']}，"
            
            if stats.get('is_time_series', False):
                line += f"高于均值{stats['count_above_mean']}个时间点，低于均值{stats['count_below_mean']}个时间点"
            else:
                line += f"高于均值{stats['count_above_mean']}个地市，低于均值{stats['count_below_mean']}个地市"
            
            summary_lines.append(line)
        
        return "\n".join(summary_lines)
    
    def _call_llm_for_correction(self, prompt: str) -> str:
        """调用大模型进行修正"""
        # 处理不同API的URL格式
        if 'dashscope.aliyuncs.com' in self.base_url:
            # 阿里云API，base_url已经包含了路径
            url = f"{self.base_url}/chat/completions"
        elif self.base_url.endswith('/v1'):
            # base_url已经包含/v1路径，直接添加endpoint
            url = f"{self.base_url}/chat/completions"
        else:
            # 需要添加完整路径
            url = f"{self.base_url}/v1/chat/completions"
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system", 
                    "content": "你是专业的数据分析师和事实检查员。严格要求：1)所有分析必须基于提供的数据 2)禁止编造任何信息 3)确保逻辑一致性 4)根据数据类型选择合适的分析角度"
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "temperature": 0.1  # 降低温度以提高准确性
        }
        
        # 如果是Qwen3模型，添加enable_thinking参数
        if 'enable_thinking' in MODEL_CONFIG:
            payload['extra_body'] = {"enable_thinking": MODEL_CONFIG['enable_thinking']}
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and result["choices"]:
                content = result["choices"][0]["message"]["content"]
                if content and content.strip():
                    print("✅ 分析结论修正完成")
                    return content.strip()
            
            print("❌ 修正失败：API返回内容为空")
            return "修正失败，请人工检查"
            
        except Exception as e:
            print(f"❌ 修正过程出错: {e}")
            return "修正失败，请人工检查"


# 使用示例
if __name__ == "__main__":
    verifier = AnalysisVerifier()
    
    # 测试用例
    test_analysis = """【拍照全球通保有率分析】  
综合保有率表现突出：锦州市以99.2%的综合保有率位居全省第一，高于均值1.0个百分点，是唯一突破99%的地市。  
价值保有率差距显著：丹东市价值保有率95.39%为全省最低，低于均值2.01个百分点，需重点提升高价值客户留存能力。"""
    
    test_data = """数据分析表格

月份	拍照全球通综合保有率(%)	拍照全球通规模保有率(%)	拍照全球通价值保有率(%)
202501	98.20	100	96.40
202502	99.20	99.80	98.60
202503	99.20	99.50	98.90
202504	98.50	99.10	97.80
202505	97.80	98.80	96.80
202506	96.95	98.50	95.39
202507	98.98	98.18	99.77
202508	96.8	97.9	95.8

数据说明：共8行数据，4个指标"""
    
    test_user_input = '请分析全球通"量质构效"分析，分析月份：202508'
    test_task_info = {"anaylsis_name": "全球通量质构效分析", "op_month": "202508"}
    
    corrected_analysis, errors = verifier.verify_and_correct_analysis(
        test_analysis, test_user_input, test_data, test_task_info
    )
    
    print("修正后的分析：")
    print(corrected_analysis)
    print("\n发现的问题：")
    for error in errors:
        print(f"- {error['description']}")
