import os
from openai import AzureOpenAI
import json
import requests
from datetime import datetime

# 初始化客户端
client = AzureOpenAI(
    api_version="2024-02-01",
    azure_endpoint="https://chatgptpi.openai.azure.com",
    api_key="4b85f7e90983424cac6fd77dc2d5e02f",
)

def draw(prompt):

    # 确保图片文件夹存在
    pictures_folder = 'pictures'
    if not os.path.exists(pictures_folder):
        os.makedirs(pictures_folder)

    # 调用API生成图像
    result = client.images.generate(
        model="Dalle3",
        prompt=prompt,
        n=1 #绘制的数量
    )

    # 假设API返回的是JSON格式的数据
    try:
        image_data = json.loads(result.model_dump_json())
        image_url = image_data['data'][0]['url']
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error processing the image generation: {e}")
        return None

    # 获取当前系统时间并格式化为字符串
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 下载并保存图片
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            # 使用当前时间作为文件名
            file_name = os.path.join(pictures_folder, f"{timestamp}.png")
            with open(file_name, 'wb') as f:
                f.write(response.content)
            print(f"Pictures saved to: {file_name}")
            return file_name
        else:
            print(f"Failed to download image: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error downloading the image: {e}")
        return None

# 使用函数示例
# user_prompt = input()
# image_path = draw(user_prompt)
# if image_path:
#     print(f"Image saved to: {image_path}")
# else:
#     print("Failed to save image.")
