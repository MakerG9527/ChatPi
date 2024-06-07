from openai import OpenAI

kimi_key = "sk-1WngzVlKjJ6ItzrKGQoHPTxWDTXB1arNtrpBnzvVvJtovtCf"
kimi_url = "https://api.moonshot.cn/v1"

def initialize_client(key = kimi_key, url = kimi_url):
    # 请替换成您自己的 API 密钥和 base_url
    api_key = key
    base_url = url

    # 创建 OpenAI 客户端实例
    client = OpenAI(api_key=api_key, base_url=base_url)
    history = []

    return history, client

def chat(query, history, client):
    history.append({"role": "user", "content": query})
    try:
        completion = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=history,
            temperature=0.3,#越高多样性越大
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"请求失败: {e}")
        return None
