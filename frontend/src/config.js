// API配置
const config = {
  // 开发环境
  development: {
    API_BASE_URL: 'http://127.0.0.1:5000'
  },
  // 生产环境 - 已部署的后端地址
  production: {
    API_BASE_URL: 'https://recipeapp-127a.onrender.com'
  }
}

// 根据环境选择配置
const currentConfig = config[import.meta.env.MODE] || config.development

export default currentConfig
