# utils/llm_router.py
import openai
import google.generativeai as genai

# Imports opcionais com fallback silencioso se não estiverem instalados
try:
    from anthropic import Client as AnthropicClient
except ImportError:
    AnthropicClient = None

try:
    from huggingface_hub import InferenceClient
except ImportError:
    InferenceClient = None

try:
    import cohere
except ImportError:
    cohere = None


class LLMRouter:
    """
    Faz fallback entre múltiplos provedores de LLM
    conforme configurado em config['fallback_chain'].
    """

    def __init__(self, config: dict, model_mapping: dict):
        self.config = config
        self.chain = config.get("fallback_chain", [])
        self.mapping = model_mapping

        # Configura clientes somente se as libs estiverem disponíveis
        self.clients = {}
        if "openai" in self.chain:
            openai.api_key = config.get("openai_key")
            self.clients["openai"] = openai
        if "gemini" in self.chain:
            genai.configure(api_key=config.get("gemini_key"))
            self.clients["gemini"] = genai
        if "anthropic" in self.chain and AnthropicClient:
            self.clients["anthropic"] = AnthropicClient(config.get("anthropic_key"))
        if "mistral" in self.chain and InferenceClient:
            self.clients["mistral"] = InferenceClient(token=config.get("mistral_key"))
        if "cohere" in self.chain and cohere:
            self.clients["cohere"] = cohere.Client(config.get("cohere_key"))

    def generate(self, model: str, prompt: str) -> str:
        """
        Tenta cada provedor na ordem do fallback_chain até obter resposta.
        """
        for provider in self.chain:
            client = self.clients.get(provider)
            if not client:
                continue
            try:
                if provider == "openai":
                    resp = client.ChatCompletion.create(
                        model=model,
                        messages=[{"role": "user", "content": prompt}],
                    )
                    return resp.choices[0].message.content
                if provider == "gemini":
                    resp = client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": prompt}],
                    )
                    return resp.choices[0].message.content
                if provider == "anthropic":
                    resp = client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": prompt}],
                    )
                    return resp.choices[0].message.content
                if provider == "mistral":
                    out = client.text_generation(model=model, inputs=prompt)
                    return out[0].generated_text
                if provider == "cohere":
                    out = client.generate(model=model, prompt=prompt)
                    return out.generations[0].text
            except Exception:
                continue
        raise RuntimeError("Nenhum provedor retornou resposta.")
