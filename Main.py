from Chat import initialize_client, chat
from Recognize import analyze_single_frame
from Speak import speak
from Think import capture_and_generate_image
from Translate import translate
from OCR import recognize_text_from_image
from Heard import heard

history, client = initialize_client() #初始化Chat的聊天历史和客户端实例

def main(query = None) :
    print("告诉我你的问题吧!")
    speak("告诉我你的问题吧!")
    while True:
        try:
            query = None
            query = heard()
            if query is None :
                print("如果说话不方便就输入吧!")
                speak("如果说话不方便就输入吧!")
                query = input()

            if query == "退出" or query == "exit" or query == "退出。":
                print("再见啦!")
                speak("再见啦!")
                break
            elif query == "朗读" or query == "read" or query == "朗读。":
                speak(input("输入朗读的内容(字符或TXT文件地址):"))

            elif query == "看到了什么" or query == "what do you see" or query == "看到了什么。":
                #调用Recognize.py,描述当前看到的图片并保存
                analysis_result = analyze_single_frame()
                if isinstance(analysis_result, dict):
                    #print("Categories:", analysis_result["categories"])
                    #print("Description:", analysis_result["description"])
                    print(analysis_result["description"])
                    #调用Translate.py翻译成中文
                    description = translate(analysis_result["description"])
                    print(description)
                    speak(description)
                else:
                    print(analysis_result)

            elif query == '提取文字' or query =="提取文字。":
                #调用OCR.py将拍摄的图片进行文字提取
                txt_path = recognize_text_from_image()
                #speak(txt_path)
            elif query == "在想什么" or query == "what do you think" or query == "在想什么。":
                # 调用Think.py,根据当前图片和提示词生成图片(没有提示词则使用描述词)并保存
                captured_image_path, generated_image_path = capture_and_generate_image()

            else:
                # 调用Chat.py,进行多轮聊天
                response = chat(query, history, client)
                if response:
                    print(f"珊珊: {response}")
                    # 朗读响应
                    speak(response)

        except KeyboardInterrupt:
            print("退出程序")
            break

if __name__ == '__main__':
    main()