import requests
import uuid

# 请替换为你的翻译器API密钥和资源位置
key = "3ad31b9809f14551bcd919d901db9a14"
location = "eastasia"

endpoint = "https://api.cognitive.microsofttranslator.com"
path = '/translate'
constructed_url = endpoint + path

def translate(text, from_lang='en', to_lang='zh-Hans'):
    try:
        # 设置请求头
        headers = {
            'Ocp-Apim-Subscription-Key': key,
            'Ocp-Apim-Subscription-Region': location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        # 设置请求参数
        params = {
            'api-version': '3.0',
            'from': from_lang,
            'to': [to_lang]  # 注意：这里应该是列表形式 ['zh-Hans']
        }

        # 设置请求体
        body = [{
            'text': text
        }]

        # 发送请求
        response = requests.post(constructed_url, params=params, headers=headers, json=body)
        response.raise_for_status()  # 如果请求返回了失败的HTTP状态码，将抛出异常

        # 解析翻译结果
        translated_text = response.json()[0]["translations"][0]["text"]

        # 返回翻译后的文本
        return translated_text

    except requests.exceptions.RequestException as e:
        # 处理请求异常，例如网络问题或无效响应
        print(f"请求异常: {e}")
    except (KeyError, IndexError) as e:
        # 处理解析响应时可能出现的键错误或索引错误
        print(f"解析响应时发生错误: {e}")
    except Exception as e:
        # 处理其他可能的异常
        print(f"发生未预料的错误: {e}")

    return None  # 如果发生异常，返回None或适当的错误信息

'''
# 使用示例
translated_text = translate("Hello, how are you?", from_lang='en', to_lang='zh-Hans')
print(translated_text)
'''