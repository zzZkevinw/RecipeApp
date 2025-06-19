import sqlite3

# 连接数据库
conn = sqlite3.connect('recipes.db')
cursor = conn.cursor()

try:
    # 查看表结构
    cursor.execute("PRAGMA table_info(recipes)")
    columns = cursor.fetchall()
    
    print('📋 数据库表结构:')
    print('=' * 50)
    for col in columns:
        print(f'列 {col[0]}: {col[1]} ({col[2]})')
    
    print('\n📋 数据内容:')
    print('=' * 50)
    cursor.execute('SELECT * FROM recipes')
    rows = cursor.fetchall()
    
    for row in rows:
        print(f'完整行数据: {row}')
        
except Exception as e:
    print(f'错误: {e}')
    
finally:
    conn.close()
