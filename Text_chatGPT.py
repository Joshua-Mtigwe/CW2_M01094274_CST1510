from openai import OpenAI
client = OpenAI(api_key="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")

prompt = "Hi how are you?"

completion = client.chat.completions.create(
  model="gpt-5.4-mini",
  messages=[
    {"role": "user", "content": prompt}
  ]
)

print(completion.choices[0].message.content)
