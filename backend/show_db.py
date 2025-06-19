import sqlite3

# 连接数据库
conn = sqlite3.connect('recipes.db')
cursor = conn.cursor()

try:
    cursor.execute('SELECT * FROM recipes')
    rows = cursor.fetchall()
    
    print('📋 本地数据库中的菜谱:')
    print('=' * 80)
    
    for row in rows:
        print(f'ID: {row[0]}')
        print(f'名称: {row[1]}')
        print(f'图片: {row[2]}')
        print(f'销量: {row[3]}')
        print('=' * 80)
        
except Exception as e:
    print(f'错误: {e}')
    
finally:
    conn.close()
