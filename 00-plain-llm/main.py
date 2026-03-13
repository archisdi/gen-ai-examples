import openai

# If using a local model like Ollama, point to your local host
# Otherwise, use your OpenAI API Key
client = openai.OpenAI(
    base_url="http://localhost:11434/v1", # Default for Ollama
    api_key="ollama", # Required but ignored by local providers
)

# Just change the model name here
model_to_use = "qwen3:8b" # or "deepseek-coder-v2"

def get_ai_analysis(temp):
    response = client.chat.completions.create(
        model=model_to_use, 
        messages=[
            {"role": "system", "content": "You are a DevOps expert. Think step-by-step."},
            {"role": "user", "content": "Explain why my IBM MQ Reason Code 2035 is happening."}
        ],
        temperature=temp
    )
    return response.choices[0].message.content

print(get_ai_analysis(temp=0.1))