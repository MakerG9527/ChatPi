from Tool import *
import azure.cognitiveservices.speech as speechsdk

# Azure订阅密钥和服务区域
speech_key = "af2f4a85d7974aa9ba45e730d29a8c7a"
service_region = "eastasia"

# 确保环境变量 "SPEECH_KEY" 和 "SPEECH_REGION" 被设置
speech_config = speechsdk.SpeechConfig(
    subscription=speech_key,
    region=service_region
)
speech_config.speech_recognition_language="zh-CN"  # 设置为中文

def heard(wav_file_path=None):
    # 如果没有提供wav文件路径，则录制音频
    if wav_file_path is None:
        wav_file_path = record_audio()

    # 从文件加载音频输入
    audio_config = speechsdk.audio.AudioConfig(filename=wav_file_path)

    # 创建语音识别器
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Recognizing speech from the file...")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    # 打印识别结果
    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

    return None