import openai

client = openai.OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

stream = client.chat.completions.create(
    model="qwen3:8b", 
    messages=[
        {"role": "system", "content": "You are a DevOps expert. Think step-by-step."},
        {"role": "user", "content": "Explain why my IBM MQ Reason Code 2035 is happening."}
    ],
    temperature=0.1,
    stream=True
)

for chunk in stream:
    # We check if there is actual text in the 'delta' (the change)
    if chunk.choices[0].delta.content is not None:
        content = chunk.choices[0].delta.content
        print(content, end="", flush=True)
