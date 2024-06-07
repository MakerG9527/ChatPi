import cv2
import os
from datetime import datetime

import pyaudio
import wave
import numpy as np


capFolder = "./photos" #存放摄像头拍到的原始图片的文件夹名
audioFolder = "./audio" #存放麦克风录制的语音文件夹名

def CreateFolder(folder_name):
    #检查当前文件夹中是否有叫这个名字的文件夹，没有就创建，返回文件夹地址

    # 构建文件夹的完整路径
    folder_path = os.path.join(os.getcwd(), folder_name)

    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        # 如果文件夹不存在，则创建文件夹
        os.makedirs(folder_path)
    '''
        print(f"Folder '{folder_name}' created at {folder_path}")
    else:
        print(f"Folder '{folder_name}' already exists at {folder_path}")
    '''

    # 返回文件夹的完整路径
    return folder_path

# 使用示例
# folder_name = 'my_new_folder'  # 替换为你的文件夹名称
# folder_address = CreateFolder(folder_name)
# print(f"The folder has been created/exists at: {folder_address}")

def Capture(imwrite_folder_path=capFolder):
    #默认将摄像头拍到的原始图片保存到./photos文件夹中
    # 检查摄像头是否成功打开
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # 获取当前系统时间并格式化为字符串
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 构建文件名
    filename = f"{timestamp}.jpg"

    # 确保提供的文件夹存在
    if not os.path.exists(imwrite_folder_path):
        os.makedirs(imwrite_folder_path)

    # 构建完整的文件路径
    image_path = os.path.join(imwrite_folder_path, filename)

    # 捕获一帧图像
    ret, frame = cap.read()
    if not ret:
        raise IOError("Cannot get image from webcam")

    # 释放摄像头
    cap.release()

    # 保存捕获的图像
    cv2.imwrite(image_path, frame)

    # 返回图片的完整路径
    return image_path

# 使用示例
# folder_path = '/path/to/your/folder'  # 替换为你的文件夹路径
# image_path = Capture(folder_path)
# print(f"Image captured and saved to: {image_path}")

def read_txt_to_list(txt_file_path):
    """
    读取 TXT 文件的内容，并将其转换为列表。

    参数:
    txt_file_path (str): TXT 文件的路径。

    返回:
    list: 文件内容的列表形式。
    """
    try:
        # 读取文件内容
        with open(txt_file_path, 'r', encoding='utf-8') as file:
            # 使用 readlines() 方法读取所有行到一个列表中
            content_list = file.readlines()

        # 移除每行末尾的换行符并返回处理后的列表
        content_list = [line.strip() for line in content_list]
        return content_list
    except FileNotFoundError:
        print(f"文件 {txt_file_path} 未找到。")
        return []
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return []

'''
# 使用示例
# 假设 'output_folder_path' 是包含 TXT 文件的文件夹路径
# 'base_filename' 是从图片路径中获取的不含扩展名的文件名
txt_file_path = os.path.join(output_folder_path, f"{base_filename}.txt")
content_list = read_txt_to_list(txt_file_path)
'''

def record_audio(save_folder=audioFolder, silence_threshold=300, silence_duration=1):
    #阈值和无声结束时间
    CHUNK = 1024  # 录音缓冲区大小
    FORMAT = pyaudio.paInt16  # 数据流格式
    CHANNELS = 1  # 声道数
    RATE = 44100  # 采样率，单位Hz
    RECORD_SECONDS = 10  # 默认录音时长，这里设置为示例值

    # 确保保存文件夹存在
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # 初始化PyAudio
    audio = pyaudio.PyAudio()

    # 打开麦克风录音流
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("正在录音，检测到", silence_duration, "秒内无声音则自动结束...")

    # 存储录音数据
    frames = []
    silence_start_time = None

    try:
        for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
            np_data = np.frombuffer(data, dtype=np.int16)

            # 检测声音强度
            if np.abs(np_data).max() > silence_threshold:
                # 如果检测到声音，重置沉默计时器
                silence_start_time = None
            else:
                # 如果没有声音，检查是否达到沉默持续时间
                if silence_start_time is None:
                    silence_start_time = datetime.now()
                elif (datetime.now() - silence_start_time).seconds >= silence_duration:
                    #print("\n检测到", silence_duration, "秒内无声音，录音结束.")
                    break

    except KeyboardInterrupt:
        # 处理Ctrl+C中断
        print("\n录音结束.")
    finally:
        # 停止并关闭录音流
        stream.stop_stream()
        stream.close()
        audio.terminate()

    # 如果没有数据或者录音时间太短，不保存文件
    if len(frames) * CHUNK / RATE < 0.1:
        print("录音时间太短，不保存文件.")
        return

    # 生成基于当前系统时间的唯一文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(save_folder, f"{timestamp}.wav")

    #print(f"保存录音文件到 {filename}...")
    # 保存为WAV文件
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    #print("录音保存完成.")
    return filename
