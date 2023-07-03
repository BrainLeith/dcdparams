import datetime
import requests
import tiktoken
from revChatGPT.V3 import Chatbot

proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}


def get_key(apikey):
    subscription_url = "https://api.openai.com/v1/dashboard/billing/subscription"
    headers = {"Authorization": "Bearer " + apikey,
               "Content-Type": "application/json"}
    subscription_response = requests.get(subscription_url, headers=headers)
    if subscription_response.status_code == 200:
        data = subscription_response.json()
        total = data.get("hard_limit_usd")
    else:
        return subscription_response.text
    # start_date设置为今天日期前99天
    start_date = (datetime.datetime.now() - datetime.timedelta(days=99)).strftime("%Y-%m-%d")
    # end_date设置为今天日期+1
    end_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    billing_url = f"https://api.openai.com/v1/dashboard/billing/usage?start_date={start_date}&end_date={end_date}"
    billing_response = requests.get(billing_url, headers=headers)
    if billing_response.status_code == 200:
        data = billing_response.json()
        total_usage = data.get("total_usage") / 100
        daily_costs = data.get("daily_costs")
        # 这个10就是指10天，可以自己调整～
        days = min(30, len(daily_costs))
        recent = f"##### 最近{days}天使用情况  \n"
        for i in range(days):
            cur = daily_costs[-i - 1]
            date = datetime.datetime.fromtimestamp(cur.get("timestamp")).strftime("%Y-%m-%d")
            line_items = cur.get("line_items")
            cost = 0
            for item in line_items:
                cost += item.get("cost")
            recent += f"\t{date}\t{(cost / 100):.2f} \n"
    else:
        return billing_response.text

    return f"\n#### 监控key为：{apikey[:-25] + '*' * 25}\n" \
           f"#### 总额:\t{total:.2f}  \n" \
           f"#### 已用:\t{total_usage:.2f}  \n" \
           f"#### 剩余:\t{total - total_usage:.2f}  \n" \
           f"\n" + recent


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


if __name__ == '__main__':
    # chatbot = Chatbot(api_key="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")
    # chatbot.proxy = proxies
    # for data in chatbot.ask_stream("你好，请帮我写一篇500字左右的关于电影《诺曼底登陆》的剧情介绍"):
    #     print(data, end="", flush=True)
    # 查询key的余额
    print(get_key(apikey="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"))
    # 查询多少个token 2种编码方式 cl100k_base text-embedding-ada-002
    # print(num_tokens_from_string("你好，请问你几岁啊!", "cl100k_base"))
