from Chat import initialize_client, chat
from Recognize import analyze_single_frame
from Speak import speak
from Think import capture_and_generate_image
from Translate import translate
from OCR import recognize_text_from_image
from Heard import heard
from Draw import draw

history, client = initialize_client() #初始化Chat的聊天历史和客户端实例

def say(message) :
    #打印并朗读内容
    print(message)
    speak(message)

def get_input() :
    InPut = None
    InPut = heard()
    if InPut is None :
        say("如果说话不方便就用键盘输入吧!")
        InPut = input()
    return InPut

def main(query = None) :
    say("告诉我你的问题吧!")
    while True:
        try:
            query = get_input() #获取输入,语音或键盘

            if query == "退出" or query == "exit" or query == "退出。":
                say("再见啦!")
                break
            elif query == "朗读" or query == "read" or query == "朗读。":
                message = get_input()
                speak(message)

            elif query == "看到了什么" or query == "what do you see" or query == "看到了什么。":
                #调用Recognize.py,描述当前看到的图片并保存
                analysis_result = analyze_single_frame()
                if isinstance(analysis_result, dict):
                    #print("Categories:", analysis_result["categories"])
                    #print("Description:", analysis_result["description"])
                    print(analysis_result["description"])
                    #调用Translate.py翻译成中文
                    description = translate(analysis_result["description"])
                    say(description)
                else:
                    print(analysis_result)

            elif query == '提取文字' or query =="提取文字。":
                #调用OCR.py将拍摄的图片进行文字提取
                txt_path = recognize_text_from_image()
                #speak(txt_path)

            elif query == "在想什么" or query == "what do you think" or query == "在想什么。":
                # 调用Think.py,根据当前图片和提示词生成图片(没有提示词则使用描述词)并保存
                captured_image_path, generated_image_path = capture_and_generate_image()

            elif query == "画一幅画" or query == "draw a picture" or query == "画一幅画。" :
                #调用Draw.py,根据提示词绘制图片并保存
                say("请描述一下您想象的画面:")
                prompt = get_input()
                draw(prompt)
                say("我画好啦!")

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
