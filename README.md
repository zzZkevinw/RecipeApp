# 🍳 蛋挞私厨 - Recipe Management System

一个现代化的菜谱管理系统，支持菜谱展示、购物车、订单管理和邮件通知。

## ✨ 功能特性

- 🍽️ 菜谱展示和管理
- 🛒 购物车功能
- 📋 订单管理系统
- 📧 邮件通知
- 🎨 现代化UI设计
- 📱 响应式布局

## 🚀 在线演示

- **前端**: [GitHub Pages链接](https://your-username.github.io/RecipeApp)
- **后端**: [Render部署链接](https://your-backend-url.onrender.com)

## 🛠️ 技术栈

### 前端
- React 19
- Vite
- CSS3 (渐变、动画、响应式)

### 后端
- Python Flask
- SQLite数据库
- SMTP邮件服务

## 📦 本地开发

### 前端启动
```bash
cd frontend
npm install
npm run dev
```

### 后端启动
```bash
cd backend
python app.py
```

## 🌐 部署指南

### 1. GitHub Pages部署前端

1. Fork这个仓库
2. 在GitHub仓库设置中启用GitHub Pages
3. 选择GitHub Actions作为部署源
4. 推送代码到main分支，自动部署

### 2. Render部署后端

1. 注册[Render](https://render.com)账号
2. 连接GitHub仓库
3. 创建新的Web Service
4. 设置构建命令：`pip install -r backend/requirements.txt`
5. 设置启动命令：`cd backend && gunicorn app:app`
6. 部署完成后获取URL

### 3. 配置API地址

部署后端后，更新 `frontend/src/config.js` 中的生产环境API地址：

```javascript
production: {
  API_BASE_URL: 'https://your-actual-backend-url.onrender.com'
}
```

## 📧 邮件配置

如需启用邮件功能，请配置 `backend/email_config.py`：

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.qq.com',
    'smtp_port': 587,
    'sender_email': 'your_email@qq.com',
    'sender_password': 'your_app_password',
    'recipient_email': '1522906545@qq.com'
}
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！
