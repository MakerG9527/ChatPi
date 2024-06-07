import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import time
from Tool import *

subscription_key = "9139d71254e742f0a36954014fbdad42"  # 替换为你的订阅密钥
endpoint = "https://cvpi.cognitiveservices.azure.com/"  # 替换为你的服务终结点

# 创建计算机视觉客户端
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# 传入要识别的图片的路径和txt文件所在的文件夹路径
#image_path = 'path_to_your_image.jpg'  # 替换为你的图片路径
output_folder_path = './text'  # 替换为你的输出文件夹路径

def get_filename_from_path(file_path):
    # 从文件路径中提取文件名
    base = os.path.basename(file_path)
    filename, _ = os.path.splitext(base)  # 分离文件名和扩展名
    return filename


def recognize_text_from_image(image_path=None, output_folder=output_folder_path):
    # 如果没有给image_path，则从用户那里获取输入
    while True:
        image_path = input("请输入图片地址(没有就填none):")

        if image_path.lower() == 'none':
            # 如果用户输入'none'，则调用Capture()从摄像头捕获图片并保存
            try:
                image_path = Capture()  # 确保Capture函数返回捕获图像的路径
                if image_path:
                    break
                else:
                    print("未能成功捕获图像，请重试。")
            except Exception as e:
                print(f"捕获图像时发生错误: {e}")

        # 尝试使用用户提供的图片路径
        try:
            # 确保image_path是有效的文件路径
            if os.path.isfile(image_path):
                break
            else:
                print(f"输入的图片地址不正确或文件不存在，请重试。")
        except Exception as e:
            print(f"检查图片路径时发生错误: {e}")

    # 以下是处理图片和保存文本的代码，与之前相同
    with open(image_path, "rb") as image_file:
        read_response = computervision_client.read_in_stream(image_file, raw=True)

    # 获取操作位置和操作ID
    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    # 等待操作完成
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    # 检查操作是否成功并打印结果
    if read_result.status == OperationStatusCodes.succeeded:
        # 确保输出文件夹存在
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 从图片路径中获取文件名（不含扩展名）
        base_filename = get_filename_from_path(image_path)
        # 定义TXT文件的完整路径，使用与图片相同的文件名，加上.txt扩展名
        output_file_path = os.path.join(output_folder, f"{base_filename}.txt")

        # 将识别的文本写入TXT文件
        with open(output_file_path, "w", encoding='utf-8') as text_file:
            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:
                    text_file.write(line.text + "\n")
            print(f"Text recognized and saved.")
            #返回识别结果路径
            return output_file_path
    else:
        print("Text recognition failed. Operation status:", read_result.status)
        return None
