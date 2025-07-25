from abc import ABC, abstractmethod

from utils.llm_router import LLMRouter


class BaseAgent(ABC):
    def __init__(self, name: str, config: dict, model_mapping: dict):
        self.name = name
        self.config = config
        self.model = model_mapping.get(name)
        self.router = LLMRouter(config)

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
            response = self.router.generate(
                prompt, model=self.model, agent_name=self.name
            )
            print(response)
        except Exception as e:
            print(f"❌ Erro em '{self.name}': {e}")
