import sqlite3

# 连接数据库
conn = sqlite3.connect('recipes.db')
cursor = conn.cursor()

# 添加示例菜谱数据
sample_recipes = [
    {
        'name': '宫保鸡丁',
        'image': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop&crop=center',
        'sales': 156
    },
    {
        'name': '麻婆豆腐', 
        'image': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400&h=300&fit=crop&crop=center',
        'sales': 89
    },
    {
        'name': '红烧肉',
        'image': 'https://images.unsplash.com/photo-1544025162-d76694265947?w=400&h=300&fit=crop&crop=center', 
        'sales': 203
    }
]

# 插入数据
for recipe in sample_recipes:
    cursor.execute(
        "INSERT INTO recipes (name, image, sales) VALUES (?, ?, ?)",
        (recipe['name'], recipe['image'], recipe['sales'])
    )

conn.commit()
conn.close()

print("成功添加示例菜谱数据！")
print("已添加：")
for recipe in sample_recipes:
    print(f"- {recipe['name']} (销量: {recipe['sales']})")
