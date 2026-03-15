import openai
import json

client = openai.OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

def parse_middleware_log(raw_log):
    response = client.chat.completions.create(
        model="qwen3:8b",
        # 1. System Message sets the "Rules"
        messages=[
            {
                "role": "system", 
                "content": "You are a log parsing engine. You output strictly valid JSON. No prose."
            },
            # 2. Few-Shot Examples set the "Pattern"
            {
                "role": "user", 
                "content": "Log: 2026-03-12 ERROR Code 2035 host 10.0.5.22"
            },
            {
                "role": "assistant", 
                "content": '{"timestamp": "2026-03-12", "level": "ERROR", "code": 2035, "ip": "10.0.5.22"}'
            },
            # 3. The Actual Task
            {
                "role": "user", 
                "content": f"Log: {raw_log}"
            }
        ],
        # Tell the model to stay in JSON mode
        response_format={"type": "json_object"}
    )
    
    # Now you can safely load it into a Python Dict
    return json.loads(response.choices[0].message.content)

# Test it
log_entry = "2026-03-13 14:22:10 SEVERE [mq-listener] Code 2009 on PROD_QM2"
parsed_data = parse_middleware_log(log_entry)

print(f"Parsed Successfully: {parsed_data}")