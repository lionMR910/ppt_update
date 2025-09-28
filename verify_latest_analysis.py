#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证最新的分析结论
"""

def verify_latest_analysis():
    # 原始数据
    data = {
        '全省': [57491.0, 54002.0, -410, -691],
        '沈阳': [16761.0, 16094.0, -111, -137],
        '大连': [13841.0, 12964.0, -100, -135],
        '鞍山': [3680.0, 3518.0, -35, -47],
        '营口': [3671.0, 3390.0, -35, -56],
        '丹东': [3414.0, 3245.0, -2, -13],
        '锦州': [2348.0, 2133.0, -22, -45],
        '朝阳': [2297.0, 2132.0, 5, -24],
        '盘锦': [1860.0, 1720.0, -70, -78],
        '葫芦岛': [1704.0, 1562.0, -2, -19],
        '辽阳': [1684.0, 1496.0, 23, -11],
        '抚顺': [1578.0, 1452.0, -23, -31],
        '阜新': [1567.0, 1421.0, 11, -18],
        '本溪': [1545.0, 1458.0, -15, -31],
        '铁岭': [1535.0, 1411.0, -33, -43]
    }
    
    province_total = data['全省'][0]
    province_photo_total = data['全省'][1]
    
    print('=== 验证最新分析结论 ===')
    
    # 1. 验证沈阳大连合计占比
    shenyang_pct = (data['沈阳'][0] / province_total) * 100
    dalian_pct = (data['大连'][0] / province_total) * 100
    combined_pct = shenyang_pct + dalian_pct
    
    print(f'1. 沈阳大连合计占比验证:')
    print(f'   沈阳: {shenyang_pct:.1f}%')
    print(f'   大连: {dalian_pct:.1f}%')
    print(f'   合计: {combined_pct:.1f}% (分析说53.3%)')
    
    # 2. 验证全省均值计算
    city_data = {k: v for k, v in data.items() if k != '全省'}
    city_count = len(city_data)
    avg_income = province_total / city_count
    
    print(f'\n2. 全省均值验证:')
    print(f'   全省总收入: {province_total}万元')
    print(f'   地市数量: {city_count}个')
    print(f'   计算均值: {avg_income:.0f}万元 (分析说3833万元)')
    
    # 3. 验证鞍山营口丹东是否均超3400万元
    print(f'\n3. 三地收入验证:')
    for city in ['鞍山', '营口', '丹东']:
        income = data[city][0]
        print(f'   {city}: {income}万元 ({"超过" if income > 3400 else "未超过"}3400万元)')
    
    # 4. 验证拍照收入占比
    shenyang_photo_pct = (data['沈阳'][1] / province_photo_total) * 100
    dalian_photo_pct = (data['大连'][1] / province_photo_total) * 100
    combined_photo_pct = shenyang_photo_pct + dalian_photo_pct
    
    print(f'\n4. 拍照收入占比验证:')
    print(f'   沈阳拍照占比: {shenyang_photo_pct:.1f}%')
    print(f'   大连拍照占比: {dalian_photo_pct:.1f}%')
    print(f'   合计: {combined_photo_pct:.1f}% (分析说53.8%)')
    
    # 5. 验证鞍山拍照业务占比对比
    anshan_global_pct = (data['鞍山'][0] / province_total) * 100
    anshan_photo_pct = (data['鞍山'][1] / province_photo_total) * 100
    
    print(f'\n5. 鞍山占比对比验证:')
    print(f'   鞍山全球通占比: {anshan_global_pct:.1f}% (分析说6.4%)')
    print(f'   鞍山拍照占比: {anshan_photo_pct:.1f}% (分析说6.5%)')
    
    # 6. 验证降幅前3位
    changes = [(city, info[2]) for city, info in city_data.items()]
    sorted_changes = sorted(changes, key=lambda x: x[1])
    top3_decline = sorted_changes[:3]
    
    print(f'\n6. 降幅前3位验证:')
    print(f'   实际前3位: {top3_decline}')
    print(f'   分析说: 沈阳-111万元、大连-100万元、盘锦-70万元')
    
    # 检查是否都超70万元
    print(f'   降幅均超70万元？')
    for city, change in top3_decline:
        print(f'     {city}: {change}万元 ({"超过" if abs(change) > 70 else "未超过"}70万元)')
    
    # 7. 验证拍照收入降幅前3位
    photo_changes = [(city, info[3]) for city, info in city_data.items()]
    sorted_photo_changes = sorted(photo_changes, key=lambda x: x[1])
    photo_top3 = sorted_photo_changes[:3]
    
    print(f'\n7. 拍照降幅前3位验证:')
    print(f'   实际前3位: {photo_top3}')
    print(f'   分析说: 沈阳-137万元、大连-135万元、盘锦-78万元')
    
    # 8. 验证正增长地市
    positive_cities = [city for city, info in city_data.items() if info[2] > 0]
    positive_values = [(city, data[city][2]) for city in positive_cities]
    
    print(f'\n8. 正增长地市验证:')
    print(f'   正增长地市: {positive_cities} (分析说辽阳、阜新、朝阳)')
    print(f'   具体数值: {positive_values}')
    print(f'   辽阳增长: {data["辽阳"][2]}万元 (分析说23万元)')
    
    # 9. 验证特定降幅数据
    print(f'\n9. 特定降幅验证:')
    target_cities = ['鞍山', '营口', '盘锦']
    for city in target_cities:
        global_change = data[city][2]
        photo_change = data[city][3]
        print(f'   {city}: 全球通{global_change}万元, 拍照{photo_change}万元')
    
    # 检查鞍山、营口、盘锦是否都是-35万元
    anshan_yingkou_changes = [data['鞍山'][2], data['营口'][2]]
    print(f'   鞍山、营口降幅均为-35万元? {all(x == -35 for x in anshan_yingkou_changes)}')
    print(f'   盘锦降幅: {data["盘锦"][2]}万元 (分析说也是-35万元)')
    
    # 总结错误
    print('\n=== 发现的问题 ===')
    errors = []
    
    # 检查均值计算
    if abs(avg_income - 3833) > 50:
        errors.append(f'全省均值错误: 实际{avg_income:.0f}万元，分析说3833万元')
    
    # 检查降幅超70万元的说法
    decline_over_70 = [abs(change) > 70 for _, change in top3_decline]
    if not all(decline_over_70):
        errors.append(f'降幅均超70万元错误: 实际{[abs(x[1]) for x in top3_decline]}')
    
    # 检查盘锦是否也是-35万元
    if data['盘锦'][2] != -35:
        errors.append(f'盘锦降幅错误: 实际{data["盘锦"][2]}万元，分析说-35万元')
    
    if errors:
        print('发现的错误:')
        for i, error in enumerate(errors, 1):
            print(f'{i}. {error}')
    else:
        print('✅ 所有数据验证通过！')

if __name__ == "__main__":
    verify_latest_analysis()
