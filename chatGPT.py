from revChatGPT.V3 import Chatbot

proxies = {
  'http': 'http://127.0.0.1:7890',
  'https': 'http://127.0.0.1:7890',
}

if __name__ == '__main__':
    chatbot = Chatbot(api_key="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")
    chatbot.proxy = proxies
    for data in chatbot.ask_stream("你好，请帮我写一篇小学作文，题目叫：我的爸爸"):
        print(data, end="", flush=True)
