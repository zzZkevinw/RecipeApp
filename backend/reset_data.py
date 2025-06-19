import sqlite3

# 连接数据库
conn = sqlite3.connect('recipes.db')
cursor = conn.cursor()

# 1. 重置所有销量为0
cursor.execute("UPDATE recipes SET sales = 0")

# 2. 更新所有菜谱的图片为正确的URL
recipes_data = [
    {
        'name': '咖喱饭',
        'image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400&h=300&fit=crop&crop=center'
    },
    {
        'name': '宫保鸡丁', 
        'image': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400&h=300&fit=crop&crop=center'
    },
    {
        'name': '麻婆豆腐',
        'image': 'https://images.unsplash.com/photo-1581833971358-2c8b550f87b3?w=400&h=300&fit=crop&crop=center'
    },
    {
        'name': '红烧肉',
        'image': 'https://images.unsplash.com/photo-1574484284002-952d92456975?w=400&h=300&fit=crop&crop=center'
    },
    {
        'name': '蛋挞',
        'image': 'https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=400&h=300&fit=crop&crop=center'
    }
]

# 更新每个菜谱的图片
for recipe in recipes_data:
    cursor.execute(
        "UPDATE recipes SET image = ? WHERE name = ?",
        (recipe['image'], recipe['name'])
    )

conn.commit()

# 验证更新结果
cursor.execute("SELECT * FROM recipes")
rows = cursor.fetchall()

print("🔄 数据重置完成！")
print("\n📋 当前菜谱数据：")
for row in rows:
    print(f"ID: {row[0]}, 名称: {row[1]}, 销量: {row[2]}")
    print(f"图片: {row[3][:60]}...")
    print("-" * 50)

conn.close()
print("\n✅ 所有数据已重置！销量归零，图片已更新为正确链接。")
