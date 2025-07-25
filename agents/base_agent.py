from abc import ABC, abstractmethod

from utils.llm_router import LLMRouter


class BaseAgent(ABC):
    def __init__(self, name: str, config: dict, model_mapping: dict):
        self.name = name
        self.config = config
        self.model = model_mapping.get(name)
        # Pass both config and model_mapping to LLMRouter so it can route based on model mapping
        self.router = LLMRouter(config, model_mapping)

    @abstractmethod
    def build_prompt(self, project_data: dict) -> str:
        """Deve retornar o prompt a ser enviado ao LLM."""
        ...

    def run(self, project_data: dict, dry_run: bool = False):
        prompt = self.build_prompt(project_data)
        if dry_run:
            print(f"[DryRun] Etapa → {self.name}  (agente: {self.name})")
            print(
                f"[DryRun] {self.name} → chamaria modelo '{self.model}' com prompt:\n\n{prompt}\n"
            )
            return

        print(f"🤖  Enviando prompt ao modelo '{self.model}'...")
        try:
            # Generate using the selected model; LLMRouter expects (model, prompt)
            response = self.router.generate(self.model, prompt)
            print(response)
            return response
        except Exception as e:
            print(f"❌ Erro em '{self.name}': {e}")
            raise
