// API配置
const config = {
  // 开发环境
  development: {
    API_BASE_URL: 'http://127.0.0.1:5000'
  },
  // 生产环境 - 部署后端后替换为实际URL
  production: {
    API_BASE_URL: 'https://recipe-app-backend-xxx.onrender.com' // 部署后端后替换为实际的后端地址
  }
}

// 根据环境选择配置
const currentConfig = config[import.meta.env.MODE] || config.development

export default currentConfig
