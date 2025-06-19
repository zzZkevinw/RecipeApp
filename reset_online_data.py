import requests
import json

# 线上API地址
API_BASE_URL = "https://recipeapp-127a.onrender.com"

def reset_online_data():
    """重置线上数据库的销量和图片"""
    
    # 首先获取当前所有菜谱
    try:
        response = requests.get(f"{API_BASE_URL}/recipes")
        if response.status_code == 200:
            recipes = response.json()
            print("📋 当前线上菜谱数据：")
            for recipe in recipes:
                print(f"ID: {recipe['id']}, 名称: {recipe['name']}, 销量: {recipe['sales']}")
        else:
            print("❌ 无法获取菜谱数据")
            return
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return

    # 正确的图片URL映射
    correct_images = {
        '咖喱饭': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400&h=300&fit=crop&crop=center',
        '宫保鸡丁': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400&h=300&fit=crop&crop=center',
        '麻婆豆腐': 'https://images.unsplash.com/photo-1581833971358-2c8b550f87b3?w=400&h=300&fit=crop&crop=center',
        '红烧肉': 'https://images.unsplash.com/photo-1574484284002-952d92456975?w=400&h=300&fit=crop&crop=center',
        '蛋挞': 'https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=400&h=300&fit=crop&crop=center'
    }

    print("\n🔄 开始重置数据...")

    # 调用重置API端点
    try:
        reset_response = requests.post(f"{API_BASE_URL}/reset-data")
        if reset_response.status_code == 200:
            result = reset_response.json()
            print(f"✅ {result['message']}")
            print(f"📊 重置了 {result['reset_count']} 个菜谱")
        else:
            print(f"❌ 重置失败: {reset_response.text}")
            return
    except Exception as e:
        print(f"❌ 重置请求失败: {e}")
        return

    # 验证重置结果
    try:
        response = requests.get(f"{API_BASE_URL}/recipes")
        if response.status_code == 200:
            updated_recipes = response.json()
            print("\n📋 重置后的菜谱数据：")
            for recipe in updated_recipes:
                print(f"ID: {recipe['id']}, 名称: {recipe['name']}, 销量: {recipe['sales']}")
                print(f"图片: {recipe['image'][:60]}...")
                print("-" * 50)
        else:
            print("❌ 无法验证重置结果")
    except Exception as e:
        print(f"❌ 验证失败: {e}")

    return recipes, correct_images

if __name__ == "__main__":
    reset_online_data()
