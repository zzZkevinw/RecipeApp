import sqlite3

# 连接数据库
conn = sqlite3.connect('recipes.db')
cursor = conn.cursor()

# 更换咖喱饭的图片（使用一个咖喱饭的图片URL）
new_curry_image_url = 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400&h=300&fit=crop&crop=center'
cursor.execute("UPDATE recipes SET image = ? WHERE name = '咖喱饭'", (new_curry_image_url,))

conn.commit()

# 验证更新结果
cursor.execute("SELECT id, name, image FROM recipes WHERE name = '咖喱饭'")
row = cursor.fetchone()

if row:
    print(f"✅ 咖喱饭图片已更新!")
    print(f"ID: {row[0]}, 名称: {row[1]}")
    print(f"新图片URL: {row[2]}")
else:
    print("❌ 未找到咖喱饭记录")

conn.close()
print("\n🍛 咖喱饭图片修复完成！")
