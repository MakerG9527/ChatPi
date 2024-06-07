import azure.cognitiveservices.speech as speechsdk
import time
from Main import main

# Azure订阅密钥和服务区域
speech_key = "af2f4a85d7974aa9ba45e730d29a8c7a"
service_region = "eastasia"

# 关键词识别模型文件路径
model_file_path = "models/key_word/hey_berry.table"
# 触发识别的关键词
keyword = "hey berry"

# 创建语音配置
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# 创建关键词识别模型
model = speechsdk.KeywordRecognitionModel(model_file_path)

# 创建语音识别器
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

def recognized_cb(evt):
    # 关键词识别回调函数
    if evt.result.reason == speechsdk.ResultReason.RecognizedKeyword:
        print("RECOGNIZED KEYWORD: {}".format(evt.result.text))
        # 停止关键词识别
        speech_recognizer.stop_keyword_recognition()

        main()  # 调用 main 函数

# 连接回调函数
speech_recognizer.recognized.connect(recognized_cb)

# 启动关键词识别
speech_recognizer.start_keyword_recognition(model)
print('Listening for keyword "{}"...'.format(keyword))

# 等待直到检测到关键词或者用户决定停止程序
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Stopping keyword recognition.")
    speech_recognizer.stop_keyword_recognition()