# python3
# Please install OpenAI SDK first：`pip3 install openai`
from openai import OpenAI

client = OpenAI(api_key="sk-edfc042235774b6c9ceae20842b4f7ab", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="step-1-128k",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    max_tokens=10000,
    stream=False
)

print(response.choices[0].message.content)