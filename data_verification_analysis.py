#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据验证分析脚本
用于验证AI分析结论的准确性
"""

def verify_analysis():
    """验证分析结论的准确性"""
    
    # 原始数据
    data = [
        ["锦州", 2348.0, 2133.0, -22, -45],
        ["抚顺", 1578.0, 1452.0, -23, -31],
        ["辽阳", 1684.0, 1496.0, 23, -11],
        ["阜新", 1567.0, 1421.0, 11, -18],
        ["铁岭", 1535.0, 1411.0, -33, -43],
        ["营口", 3671.0, 3390.0, -35, -56],
        ["葫芦岛", 1704.0, 1562.0, -2, -19],
        ["大连", 13841.0, 12964.0, -100, -135],
        ["沈阳", 16761.0, 16094.0, -111, -137],
        ["盘锦", 1860.0, 1720.0, -70, -78],
        ["朝阳", 2297.0, 2132.0, 5, -24],
        ["丹东", 3414.0, 3245.0, -2, -13],
        ["全省", 57491.0, 54002.0, -410, -691],
        ["本溪", 1545.0, 1458.0, -15, -31],
        ["鞍山", 3680.0, 3518.0, -35, -47]
    ]
    
    # 转换为字典格式便于处理
    city_data = {}
    province_data = None
    
    for row in data:
        city_name = row[0]
        if city_name == "全省":
            province_data = {
                "全球通客户收入": row[1],
                "拍照全球通客户收入": row[2],
                "全球通收入变化": row[3],
                "拍照收入变化": row[4]
            }
        else:
            city_data[city_name] = {
                "全球通客户收入": row[1],
                "拍照全球通客户收入": row[2],
                "全球通收入变化": row[3],
                "拍照收入变化": row[4]
            }
    
    province_total = province_data["全球通客户收入"]
    province_photo_total = province_data["拍照全球通客户收入"]
    
    print("=" * 80)
    print("数据验证分析报告")
    print("=" * 80)
    
    # 1. 验证占比计算
    print("\n1. 占比计算验证:")
    print("-" * 40)
    
    # 沈阳占比
    shenyang_pct = (16761.0 / province_total) * 100
    print(f"沈阳占比: {shenyang_pct:.1f}% (分析中说29.2%)")
    
    # 大连占比
    dalian_pct = (13841.0 / province_total) * 100
    print(f"大连占比: {dalian_pct:.1f}% (分析中说24.1%)")
    
    # 沈阳+大连合计占比
    combined_pct = shenyang_pct + dalian_pct
    print(f"沈阳+大连合计占比: {combined_pct:.1f}% (分析中说53.3%)")
    
    # 鞍山、营口、丹东三地占比
    anshan_pct = (3680.0 / province_total) * 100
    yingkou_pct = (3671.0 / province_total) * 100
    dandong_pct = (3414.0 / province_total) * 100
    three_cities_pct = anshan_pct + yingkou_pct + dandong_pct
    print(f"鞍山、营口、丹东三地合计占比: {three_cities_pct:.1f}% (分析中说不足19%)")
    
    # 2. 验证排序
    print("\n2. 排序验证:")
    print("-" * 40)
    
    # 全球通客户收入排序
    sorted_cities = sorted(city_data.items(), key=lambda x: x[1]["全球通客户收入"], reverse=True)
    print("全球通客户收入排序前5名:")
    for i, (city_name, city_info) in enumerate(sorted_cities[:5]):
        pct = (city_info["全球通客户收入"] / province_total) * 100
        print(f"  {city_name}: {city_info['全球通客户收入']}万元 ({pct:.1f}%)")
    
    # 3. 验证环比变化统计
    print("\n3. 环比变化统计验证:")
    print("-" * 40)
    
    # 全球通收入变化统计
    positive_cities = [city for city, info in city_data.items() if info["全球通收入变化"] > 0]
    negative_cities = [city for city, info in city_data.items() if info["全球通收入变化"] < 0]
    print(f"全球通收入正增长地市数: {len(positive_cities)}个")
    print(f"全球通收入负增长地市数: {len(negative_cities)}个")
    print("正增长地市:", positive_cities)
    
    # 拍照收入变化统计
    photo_positive = [city for city, info in city_data.items() if info["拍照收入变化"] > 0]
    photo_negative = [city for city, info in city_data.items() if info["拍照收入变化"] < 0]
    print(f"拍照收入正增长地市数: {len(photo_positive)}个")
    print(f"拍照收入负增长地市数: {len(photo_negative)}个")
    
    # 4. 验证拍照收入占比
    print("\n4. 拍照收入占比验证:")
    print("-" * 40)
    
    # 沈阳拍照占比
    shenyang_photo_pct = (16094.0 / 16761.0) * 100
    print(f"沈阳拍照收入占比: {shenyang_photo_pct:.1f}% (分析中说95.6%)")
    
    # 大连拍照占比
    dalian_photo_pct = (12964.0 / 13841.0) * 100
    print(f"大连拍照收入占比: {dalian_photo_pct:.1f}% (分析中说93.7%)")
    
    # 全省拍照占比
    province_photo_pct = (province_photo_total / province_total) * 100
    print(f"全省拍照收入占比: {province_photo_pct:.1f}% (分析中说94.0%)")
    
    # 5. 验证降幅分析
    print("\n5. 降幅分析验证:")
    print("-" * 40)
    
    # 降幅超过50万元的地市
    large_decline = [(city, info) for city, info in city_data.items() if info["全球通收入变化"] <= -50]
    print(f"降幅超过50万元的地市: {len(large_decline)}个")
    print("具体地市及降幅:")
    for city, info in large_decline:
        print(f"  {city}: {info['全球通收入变化']}万元")
    
    # 6. 验证特定地市收入规模
    print("\n6. 特定地市收入规模验证:")
    print("-" * 40)
    
    # 铁岭、阜新、辽阳三地收入
    tieling = city_data["铁岭"]["全球通客户收入"]
    fuxin = city_data["阜新"]["全球通客户收入"]
    liaoyang = city_data["辽阳"]["全球通客户收入"]
    
    print(f"铁岭收入: {tieling}万元")
    print(f"阜新收入: {fuxin}万元") 
    print(f"辽阳收入: {liaoyang}万元")
    print(f"收入范围: {min(tieling, fuxin, liaoyang)}-{max(tieling, fuxin, liaoyang)}万元 (分析中说1535-1684万元)")
    
    # 7. 检查是否有逻辑错误
    print("\n7. 逻辑错误检查:")
    print("-" * 40)
    
    # 检查"鞍山营口丹东三地收入均超3400万元"
    anshan_income = city_data["鞍山"]["全球通客户收入"]
    yingkou_income = city_data["营口"]["全球通客户收入"]
    dandong_income = city_data["丹东"]["全球通客户收入"]
    
    print(f"鞍山收入: {anshan_income}万元 ({'超过' if anshan_income > 3400 else '未超过'}3400万元)")
    print(f"营口收入: {yingkou_income}万元 ({'超过' if yingkou_income > 3400 else '未超过'}3400万元)")
    print(f"丹东收入: {dandong_income}万元 ({'超过' if dandong_income > 3400 else '未超过'}3400万元)")
    
    # 检查其余地市是否均低于3000万元
    top5_cities = {"沈阳", "大连", "鞍山", "营口", "丹东"}
    other_cities = [(city, info) for city, info in city_data.items() if city not in top5_cities]
    cities_above_3000 = [(city, info) for city, info in other_cities if info["全球通客户收入"] >= 3000]
    print(f"除前5名外，收入>=3000万元的地市: {len(cities_above_3000)}个")
    if len(cities_above_3000) > 0:
        print("具体地市:")
        for city, info in cities_above_3000:
            print(f"  {city}: {info['全球通客户收入']}万元")
    
    print("\n" + "=" * 80)
    print("验证完成")
    print("=" * 80)

if __name__ == "__main__":
    verify_analysis()
