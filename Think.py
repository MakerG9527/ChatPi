import requests
from Recognize import analyze_single_frame
from Speak import speak
from Tool import *

# 使用函数
key = "sk-ALnXHASXKvyLw6HpQdQ24kA4tdM7KQhpwYly74lNfgNz48LZ"  # 替换为你的API密钥
url = "https://api.stability.ai/v2beta/stable-image/control/sketch"
strength = 0.6
out_format = "webp"

def capture_and_generate_image(api_key=key, api_url=url, control_strength=strength, output_format=out_format, image_path=None):
    # 确保generate文件夹存在
    generate_folder = 'generate'
    if not os.path.exists(generate_folder):
        os.makedirs(generate_folder)

    # 如果没有传入image_path，则调用Capture()从摄像头捕获图片并保存
    if image_path is None:
        image_path = Capture()

    # 请求用户输入提示词
    user_prompt = input("Please enter the prompt word in English(没有就填none):")

    # 如果用户输入的是"none"，则使用analyze_single_frame函数分析image_path图片并获取描述
    if user_prompt.lower() == "none":
        analysis_result = analyze_single_frame(image_path)
        if isinstance(analysis_result, dict):
            # print("Categories:", analysis_result["categories"])
            print("Description:", analysis_result["description"])
            speak(analysis_result["description"])
        else:
            print(analysis_result)
        prompt = analysis_result["description"]
    else:
        prompt = user_prompt
    # 获取当前系统时间并格式化为字符串
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 准备API请求的headers
    headers = {
        "authorization": f"Bearer {api_key}",
        "accept": "image/*"
    }

    # 尝试发送POST请求，并捕获可能发生的异常
    try:
        with open(image_path, 'rb') as image_file:
            response = requests.post(
                api_url, headers=headers, files={'image': image_file}, data={
                    "prompt": prompt,
                    "control_strength": control_strength,
                    "output_format": output_format
                }
            )

        # 检查API响应
        if response.status_code == 200:
            # 保存生成的图片
            generated_image_filename = f"{timestamp}_gen.{out_format}"
            generated_image_path = os.path.join(generate_folder, generated_image_filename)
            with open(generated_image_path, 'wb') as file:
                file.write(response.content)
            print(f"Generated image saved successfully to {generated_image_path}")
            return image_path, generated_image_path
        else:
            # 打印错误信息，但不中断程序
            print(f"Error: {response.status_code}, {response.json()}")
            # 可以选择在这里返回None或者特定的错误信息
            return None, None

    except requests.exceptions.RequestException as e:
        # 打印请求相关的错误信息，但不中断程序
        #print(f"Error: {response.status_code}, {response.json()}")
        return None, None

'''
# 调用函数
try:
    captured_image_path, generated_image_path = capture_and_generate_image()
    print(f"Captured image saved as: {captured_image_path}")
except Exception as e:
    print(str(e))
'''