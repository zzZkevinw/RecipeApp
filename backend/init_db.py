import sqlite3

conn = sqlite3.connect('recipes.db')
c = conn.cursor()

# 创建表（只在第一次运行时生效）
c.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        sales INTEGER DEFAULT 0,
        image TEXT DEFAULT ''
    )
''')

conn.commit()
conn.close()
print("数据库初始化成功！")
