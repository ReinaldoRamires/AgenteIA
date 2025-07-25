# agents/brand_kit_bot.py

import json

from agents.base_agent import BaseAgent


class BrandKitBot(BaseAgent):
    """
    Gera um kit de identidade de marca inicial (slogan, missão, paleta de cores, etc.).
    Usa o modelo definido no model_mapping (GPT ou Gemini).
    """

    def __init__(self, config: dict, model_mapping: dict):
        super().__init__("brand_kit_bot", config, model_mapping)

    def build_prompt(self, project_data: dict) -> str:
        name = project_data.get("name", "Projeto Sem Nome")
        project_type = project_data.get("project_type", "Padrão")
        return (
            "Você é um estrategista de marca. Gere um Brand Kit inicial para o projeto.\n"
            f"Nome do projeto: {name}\n"
            f"Tipo de projeto: {project_type}\n\n"
            "Responda em JSON com o formato:\n"
            "{\n"
            '  "slogan": "...",\n'
            '  "mission_statement": "...",\n'
            '  "tone_of_voice": "...",\n'
            '  "color_palette": ["#RRGGBB - descrição", "...", "..."],\n'
            '  "typography": {"primary": "...", "secondary": "..."},\n'
            '  "logo_ideas": ["...", "..."]\n'
            "}\n"
        )

    def run(self, project_data: dict) -> dict:
        prompt = self.build_prompt(project_data)
        text = (
            self._call_openai(prompt)
            if self.model.startswith("gpt")
            else self._call_gemini(prompt)
        )

        try:
            data = json.loads(text)
        except Exception:
            data = {"raw_text": text}

        return {
            "agent": self.name,
            "model": self.model,
            "result": data,
        }
