#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试数据隔离问题
"""

print("🔍 调试数据隔离和任务混淆问题")
print("="*80)

print("🎯 可能的问题原因:")

print("\n1. 【API会话混淆】:")
print("   - 不同任务使用相同的conversation_uid？")
print("   - AI模型保持了上下文记忆？")
print("   - 需要检查conversation_uid的生成逻辑")

print("\n2. 【数据传递错误】:")
print("   - formatted_data是否正确传递？")
print("   - 是否有数据被缓存或重用？")
print("   - 需要检查每个任务的数据是否独立")

print("\n3. 【提示词污染】:")
print("   - 提示词中是否包含了其他任务的信息？")
print("   - AI是否从提示词中学习了错误的模式？")
print("   - 需要检查提示词的构造过程")

print("\n4. 【模型温度设置】:")
print("   - 温度0.3可能让AI产生了创造性的错误？")
print("   - AI可能基于模式匹配生成了不存在的内容？")
print("   - 需要验证是否与温度设置有关")

print("\n🔧 调试步骤:")
print("1. 检查conversation_uid是否唯一")
print("2. 验证每个任务的formatted_data是否正确")
print("3. 检查API调用是否独立")
print("4. 验证排序结果是否正确传递")

print("\n📊 从终端输出分析:")
print("任务12 (时间序列): 202501:88.37%, 202502:96.41%, ...")
print("任务13 (地市数据): 锦州105.1%, 盘锦104.8%, ...")
print("但分析一错误地包含了地市名称，说明数据传递有问题")

print("\n🚨 关键发现:")
print("- 任务12应该只有时间序列数据，不应该出现地市名称")
print("- 如果AI生成了地市名称，说明：")
print("  1. 数据被混淆了")
print("  2. 或者AI从其他地方学习了模式")
print("  3. 或者提示词中包含了错误信息")

print("\n💡 解决方向:")
print("1. 增加任务隔离验证")
print("2. 清理API会话状态")
print("3. 验证数据传递的完整性")
print("4. 可能需要降低模型温度")
