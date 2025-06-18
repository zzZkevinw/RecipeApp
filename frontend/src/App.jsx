import { useState, useEffect } from 'react'
import config from './config.js'

function App() {
  const [recipes, setRecipes] = useState([])
  const [cart, setCart] = useState({}) // 购物车状态：{recipeId: quantity}
  const [showOrderPage, setShowOrderPage] = useState(false) // 是否显示订单页面
  const [showForm, setShowForm] = useState(false)
  const [recipeName, setRecipeName] = useState('')
  const [imageURL, setImageURL] = useState('')

  useEffect(() => {
    fetch(`${config.API_BASE_URL}/recipes`)
      .then(res => res.json())
      .then(data => setRecipes(data))
  }, [])

  // 添加菜谱到购物车
  const addToCart = (recipe) => {
    setCart(prevCart => ({
      ...prevCart,
      [recipe.id]: (prevCart[recipe.id] || 0) + 1
    }))
  }

  // 从购物车移除菜谱
  const removeFromCart = (recipeId) => {
    setCart(prevCart => {
      const newCart = { ...prevCart }
      if (newCart[recipeId] > 1) {
        newCart[recipeId] -= 1
      } else {
        delete newCart[recipeId]
      }
      return newCart
    })
  }

  // 获取购物车中的菜谱列表
  const getCartItems = () => {
    return Object.entries(cart).map(([recipeId, quantity]) => {
      const recipe = recipes.find(r => r.id === parseInt(recipeId))
      return { ...recipe, quantity }
    }).filter(item => item.id) // 过滤掉找不到的菜谱
  }

  // 计算购物车总数量
  const getTotalCartItems = () => {
    return Object.values(cart).reduce((total, quantity) => total + quantity, 0)
  }

  // 下单功能
  const handlePlaceOrder = async () => {
    const cartItems = getCartItems()

    if (cartItems.length === 0) {
      alert('购物车为空，请先选择菜谱！')
      return
    }

    try {
      const response = await fetch(`${config.API_BASE_URL}/orders`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          items: cartItems
        })
      })

      const result = await response.json()

      if (response.ok) {
        alert('下单成功！订单详情已发送到邮箱。')
        setCart({})
        setShowOrderPage(false)
        fetch(`${config.API_BASE_URL}/recipes`)
          .then(res => res.json())
          .then(data => setRecipes(data))
      } else {
        alert('下单失败: ' + result.error)
      }
    } catch (err) {
      alert('网络错误，请检查后端是否启动')
    }
  }

  // 添加菜谱功能
  const handleAddRecipe = async () => {
    if (!recipeName.trim()) {
      alert('菜名不能为空')
      return
    }

    try {
      const response = await fetch(`${config.API_BASE_URL}/recipes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: recipeName,
          image: imageURL,
          sales: 0
        })
      })

      if (response.ok) {
        alert('添加成功！')
        setShowForm(false)
        setRecipeName('')
        setImageURL('')
        fetch(`${config.API_BASE_URL}/recipes`)
          .then(res => res.json())
          .then(data => setRecipes(data))
      } else {
        const errorData = await response.json()
        alert('添加失败: ' + errorData.error)
      }
    } catch (err) {
      alert('网络错误，请检查后端是否启动')
    }
  }

  // 如果显示订单页面
  if (showOrderPage) {
    const cartItems = getCartItems()
    const totalItems = getTotalCartItems()

    return (
      <div className="app-container order-page">
        <header className="header">
          <h1>🛒 我的订单</h1>
          <button className="btn btn-secondary" onClick={() => setShowOrderPage(false)}>
            ← 返回菜单
          </button>
        </header>

        <main className="main-content">
          {cartItems.length === 0 ? (
            <div className="empty-cart">
              <h3>🍽️ 订单为空</h3>
              <p>快去选择一些美味的菜谱吧！</p>
            </div>
          ) : (
            <>
              <div className="order-summary">
                <h3>📋 已选择的菜谱 (共 {totalItems} 份)</h3>
                {cartItems.map(item => (
                  <div key={item.id} className="order-item">
                    <img
                      src={item.image || 'https://dummyimage.com/60x60/ffffff/cccccc.png&text=+'}
                      alt={item.name}
                      className="recipe-image"
                    />
                    <div className="order-item-info">
                      <div className="order-item-name">{item.name}</div>
                      <div className="order-item-quantity">
                        数量: {item.quantity} 份
                      </div>
                    </div>
                    <div className="quantity-controls">
                      <button
                        onClick={() => removeFromCart(item.id)}
                        className="quantity-btn minus"
                      >
                        -
                      </button>
                      <span className="quantity-display">{item.quantity}</span>
                      <button
                        onClick={() => addToCart(item)}
                        className="quantity-btn plus"
                      >
                        +
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              <div className="checkout-section">
                <h3>🎯 确认下单</h3>
                <p>总共 {totalItems} 份美味菜品</p>
                <button
                  onClick={handlePlaceOrder}
                  className="checkout-btn"
                >
                  🚀 确认下单
                </button>
                <p className="checkout-note">
                  下单后订单详情将发送到邮箱 📧
                </p>
              </div>
            </>
          )}
        </main>
      </div>
    )
  }

  return (
    <div className="app-container">
      <header className="header">
        <h1>🍳 蛋挞私厨</h1>
        <button
          onClick={() => setShowOrderPage(true)}
          className="btn btn-primary"
          style={{ position: 'relative' }}
        >
          🛒 查看订单
          {getTotalCartItems() > 0 && (
            <span className="cart-badge">
              {getTotalCartItems()}
            </span>
          )}
        </button>
      </header>

      <main className="main-content">
        <div className="section-header">
          <h2>🍽️ 精选菜单</h2>
          <button
            onClick={() => setShowForm(true)}
            className="btn btn-success"
          >
            ➕ 添加菜谱
          </button>
        </div>

        <div className="recipe-grid">
          {recipes.map(recipe => (
            <div key={recipe.id} className="recipe-card">
              <img
                  src={recipe.image || 'https://dummyimage.com/80x80/ffffff/cccccc.png&text=+'}
                  alt={recipe.name}
                  className="recipe-image"
                />
              <div className="recipe-info">
                <div className="recipe-name">{recipe.name}</div>
                <div className="recipe-sales">
                  📊 销量 {recipe.sales || 0} 份
                </div>
              </div>
              <button
                onClick={() => addToCart(recipe)}
                className={`add-btn ${cart[recipe.id] ? 'has-items' : 'empty'}`}
              >
                {cart[recipe.id] ? cart[recipe.id] : '+'}
              </button>
            </div>
          ))}
        </div>
      </main>

      {showForm && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>🍳 添加新菜谱</h3>
            </div>

            <div className="form-group">
              <input
                type="text"
                placeholder="请输入菜名"
                value={recipeName}
                onChange={(e) => setRecipeName(e.target.value)}
                className="form-input"
              />
            </div>

            <div className="form-group">
              <div
                onDrop={(e) => {
                  e.preventDefault();
                  const file = e.dataTransfer.files[0];
                  const reader = new FileReader();
                  reader.onloadend = () => setImageURL(reader.result);
                  reader.readAsDataURL(file);
                }}
                onDragOver={(e) => e.preventDefault()}
                className={`upload-area ${imageURL ? 'has-image' : ''}`}
                onClick={() => document.getElementById('fileInput').click()}
              >
                {imageURL ? (
                  <img src={imageURL} alt="预览" className="upload-preview" />
                ) : (
                  <div>
                    <div style={{ fontSize: '2rem', marginBottom: '10px' }}>📸</div>
                    <div>拖动图片到这里或点击上传</div>
                  </div>
                )}
                <input
                  id="fileInput"
                  type="file"
                  style={{ display: 'none' }}
                  onChange={(e) => {
                    const file = e.target.files[0];
                    const reader = new FileReader();
                    reader.onloadend = () => setImageURL(reader.result);
                    reader.readAsDataURL(file);
                  }}
                />
              </div>
            </div>

            <div className="modal-actions">
              <button onClick={handleAddRecipe} className="btn btn-success">
                ✅ 确认添加
              </button>
              <button onClick={() => setShowForm(false)} className="btn btn-secondary">
                ❌ 取消
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App