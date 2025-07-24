import os

keys = [
    "OPENAI_API_KEY",
    "GEMINI_API_KEY",
    "ANTHROPIC_API_KEY",
    "MISTRAL_API_KEY",
    "COHERE_API_KEY",
    "GROQ_API_KEY",
    "HUGGINGFACEHUB_API_TOKEN",
    "NOTION_TOKEN",
]

for key in keys:
    print(f"{key} loaded? {bool(os.getenv(key))}")
