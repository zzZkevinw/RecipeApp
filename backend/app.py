from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
try:
    from email_config import EMAIL_CONFIG
except ImportError:
    # 如果没有配置文件，使用默认配置（邮件功能将不可用）
    EMAIL_CONFIG = {
        'smtp_server': 'smtp.qq.com',
        'smtp_port': 587,
        'sender_email': '',
        'sender_password': '',
        'recipient_email': '1522906545@qq.com'
    }

app = Flask(__name__)
CORS(app)
DB_NAME = 'recipes.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/recipes', methods=['GET'])
def get_recipes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.get_json()

    name = data.get('name')
    image = data.get('image', '')  # 默认空字符串
    sales = data.get('sales', 0)   # 默认 0

    # 简单校验
    if not name:
        return jsonify({'error': '菜名不能为空'}), 400

    # 写入数据库
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO recipes (name, image, sales) VALUES (?, ?, ?)",
        (name, image, sales)
    )
    conn.commit()
    conn.close()

    return jsonify({'message': '添加成功'}), 201

def send_order_email(order_data):
    """发送订单邮件"""
    try:
        # 检查邮件配置
        if not EMAIL_CONFIG['sender_email'] or not EMAIL_CONFIG['sender_password']:
            print("邮件配置不完整，跳过邮件发送")
            return False

        # 使用配置文件中的邮件设置
        smtp_server = EMAIL_CONFIG['smtp_server']
        smtp_port = EMAIL_CONFIG['smtp_port']
        sender_email = EMAIL_CONFIG['sender_email']
        sender_password = EMAIL_CONFIG['sender_password']
        recipient_email = EMAIL_CONFIG['recipient_email']

        # 创建邮件内容
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"蛋挞私厨新订单 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        # 构建邮件正文
        body = f"""
        <h2>🍽️ 蛋挞私厨新订单</h2>
        <p><strong>订单时间：</strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>订单详情：</strong></p>
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 8px;">菜品名称</th>
                <th style="padding: 8px;">数量</th>
            </tr>
        """

        total_items = 0
        for item in order_data:
            body += f"""
            <tr>
                <td style="padding: 8px;">{item['name']}</td>
                <td style="padding: 8px;">{item['quantity']}</td>
            </tr>
            """
            total_items += item['quantity']

        body += f"""
        </table>
        <p><strong>总数量：</strong>{total_items} 份</p>
        <p>请及时处理订单！</p>
        """

        msg.attach(MIMEText(body, 'html'))

        # 发送邮件
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()

        return True
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False

@app.route('/orders', methods=['POST'])
def place_order():
    """处理下单请求"""
    try:
        data = request.get_json()
        order_items = data.get('items', [])

        if not order_items:
            return jsonify({'error': '订单不能为空'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # 更新每个菜谱的销量
        for item in order_items:
            recipe_id = item.get('id')
            quantity = item.get('quantity', 0)

            # 获取当前销量
            cursor.execute("SELECT sales FROM recipes WHERE id = ?", (recipe_id,))
            result = cursor.fetchone()

            if result:
                current_sales = result[0] or 0
                new_sales = current_sales + quantity

                # 更新销量
                cursor.execute(
                    "UPDATE recipes SET sales = ? WHERE id = ?",
                    (new_sales, recipe_id)
                )

        conn.commit()
        conn.close()

        # 发送邮件通知
        email_sent = send_order_email(order_items)

        response_data = {
            'message': '下单成功！',
            'email_sent': email_sent
        }

        if not email_sent:
            response_data['warning'] = '邮件发送失败，但订单已成功处理'

        return jsonify(response_data), 201

    except Exception as e:
        return jsonify({'error': f'下单失败: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
