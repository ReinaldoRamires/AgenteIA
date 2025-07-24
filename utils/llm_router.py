import os
import openai
import google.generativeai as genai
from anthropic import Client as AnthropicClient
from huggingface_hub import InferenceClient
import cohere

class LLMRouter:
    def __init__(self, config: dict):
        # ordem de fallback (Gemini primeiro)
        self.fallback = config.get(
            "fallback_chain",
            ["gemini", "openai", "anthropic", "mistral", "cohere"]
        )

        # OpenAI
        openai.api_key = config.get("openai_key")
        self.openai = openai

        # Gemini (Google Generative AI)
        gem_key = config.get("gemini_key")
        if gem_key:
            genai.configure(api_key=gem_key)
            self.gemini = genai
        else:
            self.gemini = None

        # Anthropic
        ant_key = config.get("anthropic_key")
        if ant_key:
            self.anthropic = AnthropicClient(ant_key)
        else:
            self.anthropic = None

        # Mistral / HF Inference
        hf_token = config.get("mistral_key") or os.getenv("HF_API_TOKEN")
        if hf_token:
            self.hf = InferenceClient(token=hf_token)
        else:
            self.hf = None

        # Cohere
        co_key = config.get("cohere_key")
        if co_key:
            self.cohere = cohere.Client(co_key)
        else:
            self.cohere = None

    def generate(self, prompt: str, model: str, agent_name: str) -> str:
        errors = []

        for provider in self.fallback:
            try:
                if provider == "gemini" and self.gemini:
                    # Atenção: dependendo da versão do google.generativeai, o método correto pode ser:
                    #   genai.chat.completions.create(...) ou genai.generate_text(...)
                    resp = self.gemini.generate_text(model=model, prompt=prompt)
                    return resp.text

                if provider == "openai" and self.openai:
                    resp = self.openai.ChatCompletion.create(
                        model=model,
                        messages=[{"role": "user", "content": prompt}],
                    )
                    return resp.choices[0].message.content

                if provider == "anthropic" and self.anthropic:
                    resp = self.anthropic.completions.create(
                        model=model,
                        prompt=prompt,
                    )
                    return resp["completions"][0]["data"]["text"]

                if provider == "mistral" and self.hf:
                    out = self.hf.text_generation(model=model, inputs=prompt)
                    return out.generations[0].text

                if provider == "cohere" and self.cohere:
                    resp = self.cohere.generate(model=model, prompt=prompt)
                    return resp.generations[0].text

            except Exception as e:
                errors.append(f"{provider}: {e}")

        detail = "; ".join(errors)
        raise RuntimeError(
            f"Nenhum provedor LLM conseguiu gerar a resposta. Detalhes: {detail}"
        )
