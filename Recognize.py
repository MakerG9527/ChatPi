from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from io import BytesIO
from Tool import *

# 订阅密钥和终结点
subscription_key = "9139d71254e742f0a36954014fbdad42"
endpoint = "https://cvpi.cognitiveservices.azure.com/"

# 创建计算机视觉客户端
credentials = CognitiveServicesCredentials(subscription_key)
client = ComputerVisionClient(endpoint, credentials)

def analyze_single_frame(image_path=None):
    # 如果没有传入image_path，则调用Capture()从摄像头捕获图片并保存
    if image_path is None:
        image_path = Capture()  # 确保Capture函数返回捕获图像的路径

    # 读取图像文件并转换为字节流
    with open(image_path, 'rb') as image_file:
        image_stream = BytesIO(image_file.read())

    # 调用API进行图像分析
    try:
        analysis = client.analyze_image_in_stream(image_stream,
                                                   visual_features=[
                                                       VisualFeatureTypes.categories,
                                                       VisualFeatureTypes.description
                                                   ])
        # 准备返回的分析结果
        result = {
            "categories": [category.name for category in analysis.categories],
            "description": analysis.description.captions[0].text if analysis.description.captions else "No description available."
        }
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

'''
# 调用函数进行测试
analysis_result = analyze_single_frame()
if analysis_result:
    print("Analysis Result:", analysis_result)
'''