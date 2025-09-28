import requests
import json
import random
import re
try:
    from .config import MODEL_CONFIG
except ImportError:
    from config import MODEL_CONFIG

def calculate_statistics(data, headers):
    """计算准确的统计信息"""
    statistics = {}
    
    # 判断是否为时间序列数据
    is_time_series = len(headers) > 0 and '月份' in headers[0]
    
    for header in headers[1:]:  # 跳过第一列（地市或月份）
        if header.strip():
            values = []
            for item in data:
                if header in item and isinstance(item[header], (int, float)):
                    values.append(float(item[header]))
            
            if values:
                mean_val = sum(values) / len(values)
                max_val = max(values)
                min_val = min(values)
                count_above_mean = sum(1 for v in values if v > mean_val)
                count_below_mean = sum(1 for v in values if v < mean_val)
                count_above_60 = sum(1 for v in values if v >= 60.0)
                count_below_60 = sum(1 for v in values if v < 60.0)
                
                statistics[header] = {
                    "mean": round(mean_val, 1),
                    "max": max_val,
                    "min": min_val,
                    "count_total": len(values),
                    "count_above_mean": count_above_mean,
                    "count_below_mean": count_below_mean,
                    "count_above_60": count_above_60,
                    "count_below_60": count_below_60,
                    "is_time_series": is_time_series
                }
    
    return statistics

def parse_structured_data_for_stats(chart_obj):
    """解析结构化数据用于统计计算"""
    try:
        lines = chart_obj.strip().split('\n')
        
        # 找表头
        headers = []
        for line in lines:
            if ('地市' in line or '月份' in line):
                # 尝试制表符分隔，如果没有制表符则使用空格分隔
                if '\t' in line:
                    headers = line.split('\t')
                else:
                    # 使用多个空格作为分隔符
                    headers = [h.strip() for h in line.split() if h.strip()]
                break
        
        if not headers:
            return [], []
        
        # 判断是否为时间序列数据
        is_time_series = '月份' in headers[0] if headers else False
        
        # 解析数据行
        data = []
        for line in lines:
            if is_time_series:
                # 时间序列数据：查找包含年月的行
                if any(line.strip().startswith(month) for month in ['202501', '202502', '202503', '202504', '202505', '202506', '202507', '202508', '202509', '202510', '202511', '202512']):
                    # 尝试制表符分隔，如果没有则使用空格分隔
                    if '\t' in line:
                        parts = line.split('\t')
                    else:
                        parts = line.split()
                    
                    if len(parts) >= len(headers):
                        row = {}
                        for i, header in enumerate(headers):
                            if i < len(parts):
                                value = parts[i].strip()
                                if i == 0:  # 月份
                                    row[header] = value
                                else:  # 数值
                                    try:
                                        row[header] = float(value)
                                    except:
                                        row[header] = value
                        data.append(row)
            else:
                # 地市数据：原有逻辑
                if any(city in line for city in ['辽阳', '本溪', '葫芦岛', '盘锦', '鞍山', '丹东', '阜新', '大连', '锦州', '铁岭', '营口', '朝阳', '抚顺', '沈阳']):
                    if '全省' not in line:  # 跳过全省数据
                        parts = line.split('\t')
                        if len(parts) >= len(headers):
                            row = {}
                            for i, header in enumerate(headers):
                                if i < len(parts):
                                    value = parts[i].strip()
                                    if i == 0:  # 地市名
                                        row[header] = value
                                    else:  # 数值
                                        try:
                                            row[header] = float(value)
                                        except:
                                            row[header] = value
                            data.append(row)
        
        return data, headers
        
    except Exception as e:
        return [], []

def build_statistics_summary(statistics):
    """构建统计信息摘要"""
    if not statistics:
        return "无统计信息"
    
    summary_lines = []
    for indicator, stats in statistics.items():
        line = f"【{indicator}】均值{stats['mean']}，最高{stats['max']}，最低{stats['min']}，"
        
        # 对于时间序列数据，使用"个时间点"而不是"个地市"
        if stats.get('is_time_series', False):
            line += f"高于均值{stats['count_above_mean']}个时间点，低于均值{stats['count_below_mean']}个时间点"
        else:
            line += f"高于均值{stats['count_above_mean']}个地市，低于均值{stats['count_below_mean']}个地市"
        
        if stats['count_above_60'] > 0 or stats['count_below_60'] > 0:
            if stats.get('is_time_series', False):
                line += f"，超过60的时间点{stats['count_above_60']}个，低于60的时间点{stats['count_below_60']}个"
            else:
                line += f"，超过60的地市{stats['count_above_60']}个，低于60的地市{stats['count_below_60']}个"
        
        summary_lines.append(line)
    
    return "\n".join(summary_lines)

def parse_and_sort_data(chart_obj):
    """解析数据并进行排序，返回排序结果"""
    try:
        # 将chart_obj按行分割
        lines = chart_obj.strip().split('\n')
        
        # 找到数据表的开始（包含地市的行或时间数据的行）
        data_lines = []
        for line in lines:
            if '\t' in line:
                # 检查是否为地市数据
                if any(city in line for city in ['辽阳', '本溪', '葫芦岛', '盘锦', '鞍山', '丹东', '阜新', '大连', '锦州', '铁岭', '营口', '全省', '朝阳', '抚顺', '沈阳']):
                    data_lines.append(line)
                # 检查是否为时间序列数据（如202501, 202502等）
                elif any(line.strip().startswith(month) for month in ['202501', '202502', '202503', '202504', '202505', '202506', '202507', '202508', '202509', '202510', '202511', '202512']):
                    data_lines.append(line)
        
        if not data_lines:
            return "无法解析数据表格"
        
        # 解析表头和数据
        header_found = False
        headers = []
        for line in lines:
            if '\t' in line and ('地市' in line or '月份' in line):
                headers = line.split('\t')
                header_found = True
                break
        
        if not header_found:
            return "无法找到表头"
        
        # 解析数据行，分别处理地市数据、全省数据和时间序列数据
        data = []
        province_data = None
        is_time_series = '月份' in headers[0] if headers else False
        
        for line in data_lines:
            parts = line.split('\t')
            if len(parts) >= len(headers):
                row = {}
                for i, header in enumerate(headers):
                    if i < len(parts):
                        value = parts[i].strip()
                        # 转换数值
                        if i > 0:  # 第一列是地市名或月份，后面是数值
                            try:
                                row[header] = float(value)
                            except:
                                row[header] = value
                        else:
                            row[header] = value
                
                # 对于时间序列数据，直接添加到data中
                if is_time_series:
                    data.append(row)
                else:
                    # 分别保存全省数据和地市数据
                    if '全省' in line:
                        province_data = row
                    else:
                        data.append(row)
        
        if not data:
            return "无法解析数据行"
        
        # 对每个数值指标进行排序
        sort_results = []
        
        for header in headers[1:]:  # 跳过第一列（地市或月份）
            if header.strip():
                if is_time_series:
                    # 时间序列数据按时间顺序排序（不是按数值大小）
                    sorted_data = sorted(data, key=lambda x: x.get(headers[0], ''), reverse=False)
                    
                    # 生成时间序列描述
                    time_items = []
                    for item in sorted_data:
                        time_period = item[headers[0]]
                        value = item[header]
                        # 根据指标名称确定单位
                        if '万元' in header or '收入' in header:
                            unit = '万元'
                        elif '占比' in header or '%' in header or 'rate' in header.lower() or '率' in header:
                            unit = '%'
                        else:
                            unit = ''
                        time_items.append(f"{time_period}:{value}{unit}")
                    
                    items_str = "，".join(time_items)
                    sort_info = f"{header}时间序列为：{items_str}"
                    sort_results.append(sort_info)
                else:
                    # 地市数据按该指标降序排序
                    sorted_data = sorted(data, key=lambda x: x.get(header, 0), reverse=True)
                    
                    # 计算总和（用于计算占比）
                    total_value = sum(item.get(header, 0) for item in data)
                    
                    # 生成完整排序描述
                    sorted_items = []
                    for item in sorted_data:
                        city = item['地市']
                        value = item[header]
                        # 根据指标名称确定单位
                        if '万元' in header:
                            unit = '万元'
                        elif '占比' in header or '%' in header or '%' in str(value):
                            unit = '%'
                        else:
                            unit = ''
                        
                        # 计算占比（对绝对指标计算占比，不对变化量和百分比指标计算占比）
                        # 包含万元、收入、户等绝对指标，排除变化、环比、增长等变化量指标和百分比指标
                        if (('万元' in header or '收入' in header or '户' in header) and 
                            '变化' not in header and '环比' not in header and '增长' not in header and 
                            '净增' not in header and '新增' not in header and '流出' not in header and '离网' not in header and
                            '占比' not in header and '%' not in header):
                            percentage = (value / total_value * 100) if total_value > 0 else 0
                            sorted_items.append(f"{city}{value}{unit}（占比{percentage:.1f}%）")
                        else:
                            sorted_items.append(f"{city}{value}{unit}")
                    
                    # 生成完整排序描述（显示全部）
                    items_str = "，".join(sorted_items)
                    
                    # 如果有全省数据，添加全省对比
                    if province_data and header in province_data:
                        province_value = province_data[header]
                        # 根据指标名称确定单位
                        if '万元' in header:
                            province_unit = '万元'
                        elif '占比' in header or '%' in header or '%' in str(province_value):
                            province_unit = '%'
                        else:
                            province_unit = ''
                        
                        # 计算全省占比（对绝对指标）
                        if (('万元' in header or '收入' in header or '户' in header) and 
                            '变化' not in header and '环比' not in header and '增长' not in header and 
                            '净增' not in header and '新增' not in header and '流出' not in header and '离网' not in header and
                            '占比' not in header and '%' not in header):
                            # 对于绝对指标，全省数据不显示占比
                            province_str = f"全省{province_value}{province_unit}"
                        else:
                            province_str = f"全省{province_value}{province_unit}"
                        
                        sort_info = f"{header}从高到低依次为：{items_str}，{province_str}"
                    else:
                        sort_info = f"{header}从高到低依次为：{items_str}"
                    
                    
                    # 添加正负值统计信息（对变化量指标）
                    if '变化' in header or '环比' in header or '增长' in header:
                        positive_count = sum(1 for item in sorted_data if item.get(header, 0) > 0)
                        negative_count = sum(1 for item in sorted_data if item.get(header, 0) < 0)
                        zero_count = sum(1 for item in sorted_data if item.get(header, 0) == 0)
                        
                        if positive_count > 0 or negative_count > 0:
                            stats_info = f"\n【{header}统计】正增长:{positive_count}个地市，负增长:{negative_count}个地市"
                            if zero_count > 0:
                                stats_info += f"，持平:{zero_count}个地市"
                            sort_info += stats_info
                    
                    sort_results.append(sort_info)
        
        return "\n".join(sort_results)
        
    except Exception as e:
        return f"数据解析错误：{str(e)}"

def analysis_data_text(api_key, user_input, conversation_uid, chart_obj):
    # 使用配置文件中的设置
    base_url = MODEL_CONFIG['base_url']
    # 处理不同API的URL格式
    if 'dashscope.aliyuncs.com' in base_url:
        # 阿里云API，base_url已经包含了路径
        url = f"{base_url}/chat/completions"
    elif base_url.endswith('/v1'):
        # base_url已经包含/v1路径，直接添加endpoint
        url = f"{base_url}/chat/completions"
    else:
        # 需要添加完整路径
        url = f"{base_url}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    # 首先解析和排序数据
    sort_results = parse_and_sort_data(chart_obj)
    
    # 解析结构化数据并计算统计信息
    try:
        structured_data, data_headers = parse_structured_data_for_stats(chart_obj)
        statistics = calculate_statistics(structured_data, data_headers)
        
        # 生成统计摘要
        stats_summary = build_statistics_summary(statistics)
    except Exception as e:
        print(f"统计计算错误: {e}")
        stats_summary = "无法计算统计信息"
    
    # 构造分析提示词
    chart_json = json.dumps(chart_obj, ensure_ascii=False)
    prompt = f"""请对以下数据进行专业深度分析，要求：
1. 直接给出分析结论，不要包含思考过程
2. 严格以【优质分析样例】格式输出，不要输出标题，仅输出分项总结、要点
3. 语言简洁明了，重点突出，注意标点符号
4. 只输出主要结论，不超过300字
5. 有些显而易见的内容没必要说，比如各市拍照收入占比均超过90%
6. 针对分层统计数据，避免逐项列举各层级的最值，应进行整体趋势分析和结构性洞察，重点关注分布特征、异常值和业务含义
7. 避免简单罗列地市名称，应进行深度分析：结合全省均值进行对比，识别整体趋势和异常情况，重点关注业务含义和改进建议，形成有价值的洞察结论

【关键分析原则】
1. 所有结论必须基于【准确的排序结果】，严禁自行推测或计算
2. 提及"唯一"、"最大"、"最小"、"最低"、"最高"等极值时，必须先核对排序结果确保准确
3. 描述正负增长地市数量时，必须参考统计信息，不可估算
4. 比较不同地市时，必须按照排序结果中的实际顺序
5. 禁止使用"除...外"的表述，除非确认所有例外情况
6. 针对分层统计数据，避免逐项列举各层级的最值，应进行整体趋势分析和结构性洞察，重点关注分布特征、异常值和业务含义
7. 避免简单罗列地市名称，应进行深度分析：结合全省均值进行对比，识别整体趋势和异常情况，重点关注业务含义和改进建议，形成有价值的洞察结论
8. 两级分化的结论一定要严格参考排序结果，不可自行推测

【数据验证要求】
- 声称某地市"唯一"时，必须确认排序结果中确实只有该地市满足条件
- 提及地市数量时，必须与统计信息一致
- 比较降幅大小时，必须按照排序结果的实际排名顺序

【样例如下】
XXX,XXX表现突出：XXX,XXX全球通客户收入环比增长 10.2%，是超过10%的地市，表现最为突出。
XXX收入最高：沈阳以 1.7亿元 的全球通客户收入位居全省第一，占全省总收入的 43.4%。
多数地市收入下降：除XX,XX外，其余XX个地市全球通客户收入均出现不同程度的环比下降，需重点关注。
XX收入下降幅度较大：XX全球通客户收入环比下降 XX%，是降幅最大的地市之一，需深入分析原因并采取措施。

【优质分析样例】（避免简单罗列，进行深度洞察）：
融合率整体偏低：辽宁省全球通客户固移融合率平均为63.2%，有效融合率为77.4%，整体融合水平有待提升。
铁岭和葫芦岛需重点关注：铁岭固移融合率仅57.2%，葫芦岛为55.6%，均低于全省平均水平，保有和融合能力较弱。
营口表现相对较好：营口固移融合率为67.4%，有效融合率为82.6%，均全省最高。
多数地市融合率接近均值：除铁岭、葫芦岛外，其余地市固移融合率均在62%以上，整体差距不大，但提升空间仍存。

【严格禁止事项】
- 禁止以markdown格式输出
- 禁止重复表达相同观点
- 禁止输出任何思考过程、<think>标签、分析推理步骤或中间计算过程
- 分析报告文字中禁止带有空格
- 禁止在同一份报告中出现逻辑矛盾的结论
- 禁止使用模糊或相互冲突的形容词描述同一现象
- 禁止忽略排序结果中的统计信息
- 禁止对变化量数据进行不准确的概括


【准确的排序结果】（请按照以下排序结果进行分析，确保准确性）：
{sort_results}

用户问题：{user_input}
原始数据：{chart_json}

请按照上述排序结果进行分析，不要自行排序。

【最后检查】在输出分析结论前，请严格核对：
1. 所说的"最高","最低"地市是否确实是排序第一位？
2. 所说的"高于"、"超过"是否数值确实更大？
3. 所有排名表述是否与排序结果完全一致？
4. 是否错误地将各地市占比相加（绝对禁止！）？
5. 均值和统计数量是否准确计算？
6. "紧随其后"的地市是否按正确的排序顺序列出？
7. 任何涉及均值的数值是否基于实际数据计算？
8. 同一地市是否只有一个数值，没有矛盾数据？
9. 是否将垫底地市错误说成了前3名？
10. 所有数值是否都来源于排序结果，没有编造？

重要提醒：绝对禁止输出任何思考过程、<think>标签或推理步骤，直接给出最终分析结论："""
    payload = {
        "model": MODEL_CONFIG['llm_model'],
        "messages": [
            {"role": "system", "content": "你是中国移动的专业数据分析师。严格要求：1)所有均值和统计数据必须使用提供的【准确统计信息】，禁止自行计算 2)所有排名必须基于排序结果，禁止编造 3)绝对禁止将各地市占比相加或说合计占比 4)禁止混淆不同指标概念 5)严格区分地市均值和全省数据，引用时必须准确 6)禁止捏造任何数字 7)同一地市只能有一个数值，不得出现矛盾数据  8)直接给出最终结论，禁止输出思考过程"},
            {"role": "user", "content": prompt}
        ],
        "temperature": MODEL_CONFIG.get('temperature', 0.3)
    }
    
    # 如果是Qwen3模型，添加enable_thinking参数到extra_body
    if 'enable_thinking' in MODEL_CONFIG:
        payload['extra_body'] = {"enable_thinking": MODEL_CONFIG['enable_thinking']}
    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=MODEL_CONFIG.get('timeout', 120)
        )
        
        response.raise_for_status()
        result = response.json()
        
        # 解析大模型返回内容
        if "choices" in result and result["choices"]:
            content = result["choices"][0]["message"]["content"]
            if content and content.strip():  # 检查返回内容是否有效
                return content
            else:
                # 内容为空，简化输出
                print("⚠️ API返回内容为空")
                return None
        return result
    except requests.exceptions.RequestException as e:
        # 简化错误输出
        print(f"❌ API请求失败: {type(e).__name__}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"错误状态码: {e.response.status_code}")
        return None
    except json.JSONDecodeError as e:
        # 简化错误输出
        print(f"❌ JSON解析错误: {str(e)[:100]}")
        return None
    except Exception as e:
        # 简化错误输出
        print(f"❌ API调用异常: {type(e).__name__}: {str(e)[:100]}")
        return None

def analysis_data_text_test(api_key, user_input, conversation_uid, chart_obj):
    # 使用配置文件中的设置（这个函数使用不同的API格式）
    url = f"{MODEL_CONFIG['base_url']}/api/generate"
    headers = {
        "Content-Type": "application/json"
    }
    # 首先解析和排序数据
    sort_results = parse_and_sort_data(chart_obj)
    
    # 构造分析提示词
    chart_json = json.dumps(chart_obj, ensure_ascii=False)
    prompt = f"""请对以下数据进行分析，要求：
1. 直接给出分析结论，不要包含思考过程
2. 使用规范的格式，包括标题、要点
3. 语言简洁明了，重点突出
4. 只输出主要结论，不超过300字
5. 有些显而易见的内容没必要说，比如各市拍照全球通收入占比普遍超过90%，保有类指标结论重点对保有率低于97%的地市进行分析。
6. 报告的地市请直接输出地市名称，如沈阳，不要输出沈阳市。
样例如下：

1. 整体收入稳定：2025年6月，辽宁全球通客户收入整体保持稳定，其中拍照全球通收入占比高达 97.11%，表明拍照全球通业务是主要收入来源。
2. 阜新表现突出：阜新全球通客户收入环比增长 10.20%，是唯一增长超过10%的地市，表现最为突出。
3. 沈阳收入最高：沈阳以 1.73亿元 的全球通客户收入位居全省第一，占全省总收入的 43.45%。
4. 多数地市收入下降：除朝阳和阜新外，其余12个地市全球通客户收入均出现不同程度的环比下降，需重点关注。
5. 营口收入下降幅度较大：营口全球通客户收入环比下降 3.45%，是降幅最大的地市之一，需深入分析原因并采取措施。


【准确的排序结果】（请严格按照以下排序结果进行分析，确保准确性）：
{sort_results}

用户问题：{user_input}
原始数据：{chart_json}

请严格按照上述排序结果进行分析，确保所有极值判断准确无误。重要提醒：绝对禁止输出任何思考过程、<think>标签或推理步骤，直接给出最终分析结论："""
    payload = {
        "model": MODEL_CONFIG['llm_model'],
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=MODEL_CONFIG.get('timeout', 120)
        )
        
        response.raise_for_status()
        result = response.json()
        
        # 解析大模型返回内容
        if "response" in result:
            content = result["response"]
            if content and content.strip():  # 检查返回内容是否有效
                return content
            else:
                # 内容为空，输出调试信息
                print("API返回内容为空，调试信息：")
                print(f"请求URL: {url}")
                print(f"请求头: {headers}")
                print(f"请求负载: {json.dumps(payload, ensure_ascii=False, indent=2)}")
                print(f"响应状态码: {response.status_code}")
                print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
                return None
        return result
    except requests.exceptions.RequestException as e:
        # 简化错误输出
        print(f"❌ API请求失败: {type(e).__name__}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"错误状态码: {e.response.status_code}")
        return None
    except json.JSONDecodeError as e:
        # 简化错误输出
        print(f"❌ JSON解析错误: {str(e)[:100]}")
        return None
    except Exception as e:
        # 简化错误输出
        print(f"❌ API调用异常: {type(e).__name__}: {str(e)[:100]}")
        return None

# 使用示例
if __name__ == "__main__":
    api_key = MODEL_CONFIG['api_key']
    user_input = "请分析以下数据，并给出主要结论"
    chart_obj = """
    全球通组家、宽带、集团、长机龄客户占比


地市	全球通组家客户占比	全球通宽带客户占比	全球通集团客户占比	全球通长机龄客户占比
辽阳	19.83 	50.24 	78.56 	29.55 
本溪	24.53 	56.18 	77.84 	29.43 
葫芦岛	24.58 	47.95 	77.62 	25.53 
盘锦	29.70 	54.36 	75.97 	26.65 
鞍山	21.20 	52.19 	75.71 	28.32 
丹东	25.77 	53.03 	73.93 	29.92 
阜新	24.91 	53.24 	70.87 	28.20 
大连	23.44 	56.50 	68.72 	29.62 
锦州	23.74 	54.47 	65.27 	27.15 
铁岭	24.22 	48.77 	65.02 	27.20 
营口	27.59 	56.12 	64.94 	28.24 
全省	23.19 	54.08 	63.81 	29.01 
朝阳	30.03 	55.77 	60.41 	29.07 
抚顺	25.16 	56.36 	55.37 	29.67 
沈阳	19.60 	53.27 	49.21 	29.71 

"""
    conversation_uid = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    result = analysis_data_text(api_key, user_input, conversation_uid, chart_obj)
    if result:
        print("大模型分析结论：", result)
    else:
        print("API调用失败，无法获取分析结果。请检查网络连接和API配置。") 