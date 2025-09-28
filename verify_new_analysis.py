#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证新生成的分析内容
"""

def verify_new_analysis():
    # 原始数据
    data = {
        '全省': [57491.0, 54002.0, -410, -691],
        '沈阳': [16761.0, 16094.0, -111, -137],
        '大连': [13841.0, 12964.0, -100, -135],
        '盘锦': [1860.0, 1720.0, -70, -78],
        '营口': [3671.0, 3390.0, -35, -56],
        '鞍山': [3680.0, 3518.0, -35, -47],
        '铁岭': [1535.0, 1411.0, -33, -43],
        '抚顺': [1578.0, 1452.0, -23, -31],
        '锦州': [2348.0, 2133.0, -22, -45],
        '本溪': [1545.0, 1458.0, -15, -31],
        '葫芦岛': [1704.0, 1562.0, -2, -19],
        '丹东': [3414.0, 3245.0, -2, -13],
        '朝阳': [2297.0, 2132.0, 5, -24],
        '阜新': [1567.0, 1421.0, 11, -18],
        '辽阳': [1684.0, 1496.0, 23, -11]
    }
    
    province_total = data['全省'][0]
    province_photo_total = data['全省'][1]
    
    print('=== 验证新生成的分析内容 ===')
    
    # 1. 验证占比计算
    shenyang_pct = (data['沈阳'][0] / province_total) * 100
    dalian_pct = (data['大连'][0] / province_total) * 100
    combined_pct = shenyang_pct + dalian_pct
    
    print(f'1. 占比验证:')
    print(f'   沈阳占比: {shenyang_pct:.1f}% (分析说29.2%)')
    print(f'   大连占比: {dalian_pct:.1f}% (分析说24.1%)')
    print(f'   合计占比: {combined_pct:.1f}% (分析说超53%)')
    
    # 2. 验证收入变化统计
    city_data = {k: v for k, v in data.items() if k != '全省'}
    declining_cities = [city for city, info in city_data.items() if info[2] < 0]
    positive_cities = [city for city, info in city_data.items() if info[2] > 0]
    
    print(f'\n2. 收入变化验证:')
    print(f'   负增长地市: {len(declining_cities)}个 (分析说11个)')
    print(f'   正增长地市: {len(positive_cities)}个')
    print(f'   正增长地市: {positive_cities}')
    
    # 3. 验证拍照收入占比
    print(f'\n3. 拍照收入占比验证:')
    anshan_photo_pct = (data['鞍山'][1] / data['鞍山'][0]) * 100
    yingkou_photo_pct = (data['营口'][1] / data['营口'][0]) * 100
    tieling_photo_pct = (data['铁岭'][1] / data['铁岭'][0]) * 100
    huludao_photo_pct = (data['葫芦岛'][1] / data['葫芦岛'][0]) * 100
    province_photo_pct = (province_photo_total / province_total) * 100
    
    print(f'   鞍山拍照占比: {anshan_photo_pct:.1f}% (分析说95.7%)')
    print(f'   营口拍照占比: {yingkou_photo_pct:.1f}% (分析说92.3%)')
    print(f'   铁岭拍照占比: {tieling_photo_pct:.1f}% (分析说91.9%)')
    print(f'   葫芦岛拍照占比: {huludao_photo_pct:.1f}% (分析说91.7%)')
    print(f'   全省均值: {province_photo_pct:.1f}% (分析说93.9%)')
    
    # 4. 验证降幅排序
    print(f'\n4. 降幅排序验证:')
    changes = [(city, info[2]) for city, info in city_data.items()]
    sorted_changes = sorted(changes, key=lambda x: x[1])
    
    print(f'   降幅最大前3名: {sorted_changes[:3]}')
    print(f'   分析说: 大连(-100)、沈阳(-111)')
    
    # 5. 验证拍照收入变化
    print(f'\n5. 拍照收入变化验证:')
    photo_changes = [(city, info[3]) for city, info in city_data.items()]
    sorted_photo_changes = sorted(photo_changes, key=lambda x: x[1])
    
    print(f'   拍照降幅最大前3名: {sorted_photo_changes[:3]}')
    print(f'   分析说: 沈阳(-137)、大连(-135)')
    
    # 6. 检查业务结构表述
    print(f'\n6. 业务结构验证:')
    liaoyang_global = data['辽阳'][2]  # +23
    liaoyang_photo = data['辽阳'][3]   # -11
    print(f'   辽阳全球通变化: {liaoyang_global}万元 (分析说+23万元)')
    print(f'   辽阳拍照变化: {liaoyang_photo}万元 (分析说-11万元)')
    
    # 总结错误
    print('\n=== 发现的问题 ===')
    errors = []
    
    if abs(anshan_photo_pct - 95.7) > 0.5:
        errors.append(f'鞍山拍照占比错误: 实际{anshan_photo_pct:.1f}%，分析说95.7%')
    
    if abs(yingkou_photo_pct - 92.3) > 0.5:
        errors.append(f'营口拍照占比错误: 实际{yingkou_photo_pct:.1f}%，分析说92.3%')
        
    if abs(tieling_photo_pct - 91.9) > 0.5:
        errors.append(f'铁岭拍照占比错误: 实际{tieling_photo_pct:.1f}%，分析说91.9%')
        
    if abs(huludao_photo_pct - 91.7) > 0.5:
        errors.append(f'葫芦岛拍照占比错误: 实际{huludao_photo_pct:.1f}%，分析说91.7%')
    
    if abs(province_photo_pct - 93.9) > 0.5:
        errors.append(f'全省均值错误: 实际{province_photo_pct:.1f}%，分析说93.9%')
    
    # 检查分析中的数字格式问题
    analysis_text = """全球通客户收入集中度高：沈阳大连双城主导全省格局沈阳以16761万元全球通客户收入位居全省第一占比292大连13841万元占比241两市合计占比超53全省收入分布呈现明显头部效应"""
    
    if '292' in analysis_text and '29.2' not in analysis_text:
        errors.append('占比格式错误: 29.2%被显示为292')
    if '241' in analysis_text and '24.1' not in analysis_text:
        errors.append('占比格式错误: 24.1%被显示为241')
    
    # 检查是否缺少标点符号
    if '。' not in analysis_text[:100]:
        errors.append('格式问题: 缺少标点符号，文本难以阅读')
    
    if errors:
        print('发现的问题:')
        for i, error in enumerate(errors, 1):
            print(f'{i}. {error}')
    else:
        print('✅ 所有数据验证通过！')
    
    # 计算实际的拍照占比
    print('\n=== 实际拍照占比计算 ===')
    for city, info in [('鞍山', data['鞍山']), ('营口', data['营口']), 
                       ('铁岭', data['铁岭']), ('葫芦岛', data['葫芦岛'])]:
        actual_pct = (info[1] / info[0]) * 100
        print(f'{city}: {actual_pct:.1f}%')

if __name__ == "__main__":
    verify_new_analysis()
