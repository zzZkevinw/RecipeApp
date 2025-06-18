import sqlite3

# 连接数据库
conn = sqlite3.connect('recipes.db')
cursor = conn.cursor()

# 1. 将所有销量设为0
cursor.execute("UPDATE recipes SET sales = 0")

# 2. 更换宫保鸡丁的图片（使用一个更可靠的图片URL）
new_image_url = 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400&h=300&fit=crop&crop=center'
cursor.execute("UPDATE recipes SET image = ? WHERE name = '宫保鸡丁'", (new_image_url,))

conn.commit()

# 验证更新结果
cursor.execute("SELECT * FROM recipes")
rows = cursor.fetchall()

print("更新后的菜谱数据：")
for row in rows:
    print(f"ID: {row[0]}, 名称: {row[1]}, 销量: {row[2]}, 图片: {row[3][:50]}...")

conn.close()
print("\n✅ 数据更新完成！")
