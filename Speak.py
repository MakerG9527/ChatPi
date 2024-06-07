import azure.cognitiveservices.speech as speechsdk
import os
from Tool import read_txt_to_list
# 从环境变量中获取订阅密钥和区域
speech_key = "af2f4a85d7974aa9ba45e730d29a8c7a"
service_region = "eastasia"

# 创建SpeechConfig对象
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# 设置支持中文的语音名称
speech_config.speech_synthesis_voice_name = 'zh-CN-XiaoxiaoNeural'  # 选择一个支持中文的语音

# 创建AudioConfig对象，指定输出到默认扬声器
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# 创建SpeechSynthesizer对象（只需要创建一次）
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

def speak(text, speed=100, pitch=50):
    # 如果text是文件路径，则读取文件内容为列表
    if os.path.isfile(text):
        # 调用read_txt_to_list函数将txt转化为list
        texts_to_speak = read_txt_to_list(text)
    else:
        # 如果text不是文件路径，则假定它是一个字符串，并创建一个包含该字符串的列表
        texts_to_speak = [text]

    # 设置语速和音调
    speech_config.speech_synthesis_speech_rate_percent = speed
    speech_config.speech_synthesis_voice_pitch = pitch

    # 合成文本并输出到扬声器
    for text_to_speak in texts_to_speak:
        speech_synthesis_result = speech_synthesizer.speak_text_async(text_to_speak).get()

        # 检查合成结果
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            #print("Speech synthesized for text: {}".format(text_to_speak))
            pass
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")

# 使用示例
#speak("hello world")  # 直接朗读字符串
#speak("path_to_your_text_file.txt")  # 朗读TXT文件中的所有文本