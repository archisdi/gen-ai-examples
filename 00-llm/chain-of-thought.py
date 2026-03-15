import openai
import json

client = openai.OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

def diagnose_with_cot(raw_log):
    response = client.chat.completions.create(
        model="qwen3:8b", # Using the 'coding' model we talked about
        messages=[
            {
                "role": "system", 
                "content": """You are an SRE specialist. You must follow this JSON structure:
                {
                    "step_by_step_analysis": "Your internal logic here",
                    "root_cause": "The single most likely issue",
                    "fix_command": "A bash or mqsc command to fix it",
                    "confidence_score": 0.0-1.0
                }
                Always think through the error codes before providing the fix."""
            },
            {
                "role": "user", 
                "content": f"Analyze this IBM MQ log: {raw_log}"
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.2 # Low temperature for precision
    )
    
    return json.loads(response.choices[0].message.content)

# A more complex "mystery" log
mystery_log = "AMQ9508: Program cannot extend the queue manager log. Log Path: /var/mqm/log/QM1/active/."

result = diagnose_with_cot(mystery_log)

print(f"THOUGHT PROCESS: {result['step_by_step_analysis']}")
print(f"FIX: {result['fix_command']}")
print(result)