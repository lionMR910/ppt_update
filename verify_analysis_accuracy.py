#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证分析内容的准确性
"""

def verify_analysis():
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
    province_change = data['全省'][2]
    province_photo_change = data['全省'][3]
    
    print('=== 验证分析内容的准确性 ===')
    
    # 1. 验证占比计算
    shenyang_pct = (data['沈阳'][0] / province_total) * 100
    dalian_pct = (data['大连'][0] / province_total) * 100
    combined_pct = shenyang_pct + dalian_pct
    
    print(f'1. 占比验证:')
    print(f'   沈阳占比: {shenyang_pct:.1f}% (分析说29.2%)')
    print(f'   大连占比: {dalian_pct:.1f}% (分析说24.1%)')
    print(f'   合计占比: {combined_pct:.1f}% (分析说53.3%)')
    
    # 2. 验证鞍山与沈阳收入比例
    anshan_ratio = (data['鞍山'][0] / data['沈阳'][0]) * 100
    print(f'\n2. 收入比例验证:')
    print(f'   鞍山收入是沈阳的: {anshan_ratio:.0f}% (分析说22%)')
    
    # 3. 验证降幅前3名合计
    changes = [(city, info[2]) for city, info in data.items() if city != '全省']
    sorted_changes = sorted(changes, key=lambda x: x[1])
    top3_decline = sorted_changes[:3]
    top3_total = sum(abs(change[1]) for change in top3_decline)
    top3_pct = (top3_total / abs(province_change)) * 100
    
    print(f'\n3. 全球通收入降幅前3名验证:')
    print(f'   前3名: {[f"{city}({change})" for city, change in top3_decline]}')
    print(f'   合计降幅: {top3_total}万元 (分析说281万元)')
    print(f'   占全省比例: {top3_pct:.1f}% (分析说68.5%)')
    
    # 4. 验证拍照收入降幅前3名
    photo_changes = [(city, info[3]) for city, info in data.items() if city != '全省']
    sorted_photo_changes = sorted(photo_changes, key=lambda x: x[1])
    photo_top3 = sorted_photo_changes[:3]
    photo_top3_total = sum(abs(change[1]) for change in photo_top3)
    photo_top3_pct = (photo_top3_total / abs(province_photo_change)) * 100
    
    print(f'\n4. 拍照收入降幅前3名验证:')
    print(f'   前3名: {[f"{city}({change})" for city, change in photo_top3]}')
    print(f'   合计降幅: {photo_top3_total}万元 (分析说270万元)')
    print(f'   占全省比例: {photo_top3_pct:.1f}% (分析说39.1%)')
    
    # 5. 验证沈阳收入差额
    shenyang_diff = data['沈阳'][0] - data['沈阳'][1]
    print(f'\n5. 沈阳收入差额验证:')
    print(f'   全球通与拍照收入差额: {shenyang_diff}万元 (分析说667万元)')
    
    # 6. 检查其他地市差额超500万元的情况
    print(f'\n6. 收入差额超500万元的地市:')
    large_diff_cities = []
    for city, info in data.items():
        if city != '全省':
            diff = info[0] - info[1]
            if diff > 500:
                large_diff_cities.append((city, diff))
                print(f'   {city}: {diff}万元')
    
    if not large_diff_cities:
        print('   无地市收入差额超过500万元')
    elif len(large_diff_cities) == 1:
        print(f'   确实只有{large_diff_cities[0][0]}一个地市差额超过500万元')
    
    # 7. 检查14个地市全部下降的说法
    declining_cities = [city for city, info in data.items() if city != '全省' and info[2] < 0]
    total_cities = len([city for city in data.keys() if city != '全省'])
    
    print(f'\n7. 收入变化统计验证:')
    print(f'   总地市数: {total_cities}个')
    print(f'   下降地市数: {len(declining_cities)}个')
    print(f'   分析说"14个地市全部下降"是否正确: {"是" if len(declining_cities) == 14 else "否"}')
    
    if len(declining_cities) != 14:
        positive_cities = [city for city, info in data.items() if city != '全省' and info[2] > 0]
        print(f'   实际正增长地市: {positive_cities}')
    
    print('\n=== 验证结果汇总 ===')
    errors = []
    
    if abs(shenyang_pct - 29.2) > 0.1:
        errors.append(f'沈阳占比错误: 实际{shenyang_pct:.1f}%，分析说29.2%')
    if abs(dalian_pct - 24.1) > 0.1:
        errors.append(f'大连占比错误: 实际{dalian_pct:.1f}%，分析说24.1%')
    if abs(combined_pct - 53.3) > 0.1:
        errors.append(f'合计占比错误: 实际{combined_pct:.1f}%，分析说53.3%')
    if abs(anshan_ratio - 22) > 1:
        errors.append(f'鞍山/沈阳比例错误: 实际{anshan_ratio:.0f}%，分析说22%')
    if abs(top3_total - 281) > 1:
        errors.append(f'降幅前3名合计错误: 实际{top3_total}万元，分析说281万元')
    if abs(photo_top3_total - 270) > 1:
        errors.append(f'拍照降幅前3名合计错误: 实际{photo_top3_total}万元，分析说270万元')
    if abs(shenyang_diff - 667) > 1:
        errors.append(f'沈阳收入差额错误: 实际{shenyang_diff}万元，分析说667万元')
    if len(declining_cities) != 14:
        errors.append(f'下降地市数量错误: 实际{len(declining_cities)}个，分析说14个全部下降')
    
    if errors:
        print('发现的错误:')
        for i, error in enumerate(errors, 1):
            print(f'{i}. {error}')
    else:
        print('✅ 所有数据验证通过，分析内容准确无误！')

if __name__ == "__main__":
    verify_analysis()
