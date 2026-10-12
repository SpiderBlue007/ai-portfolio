# W4 命令行学科问答机器人（API 版）
# 依赖：pip install openai python-dotenv
# 运行：python week4_api_bot.py "把字句的教学难点有哪些"
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath  # noqa: E402  加载 .env

weekpath.load_env()

import openai  # noqa: E402

BASE_URL = "https://api.deepseek.com/v1"          # 通义：https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL = "deepseek-chat"                            # 通义：qwen-plus

_client = None


def get_client():
    """按需创建客户端：这样"没配密钥"能在 __main__ 里被友好提示，
    而不是在 import 阶段就抛出看不懂的 OpenAIError。"""
    global _client
    if _client is None:
        key = os.getenv("DEEPSEEK_API_KEY")
        if not key:
            raise RuntimeError("未配置 DEEPSEEK_API_KEY")
        _client = openai.OpenAI(base_url=BASE_URL, api_key=key)  # 密钥必须来自环境变量
    return _client


def ask(question, temperature=0.7, max_tokens=800):
    r = get_client().chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": question}],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return r.choices[0].message.content


if __name__ == "__main__":
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("错误：未设置 DEEPSEEK_API_KEY。")
        print("  处理：复制 .env.example 为 .env 并填入密钥，重启终端后重试。")
        sys.exit(1)
    q = " ".join(sys.argv[1:]) or "把字句的教学难点有哪些"
    try:
        ans = ask(q)
    except openai.APITimeoutError:
        print("错误：请求超时，请检查网络或调大 timeout。")
        sys.exit(1)
    print(ans)
    # 日志固定写代码包根目录（.gitignore 已排除），避免随手建在工作目录里被误提交
    with open(weekpath.root_path("chat_log.txt"), "a", encoding="utf-8") as f:
        f.write("Q: %s\nA: %s\n\n" % (q, ans))
