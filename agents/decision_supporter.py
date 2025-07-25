"""
Agente de apoio à decisão.

Este agente recebe dados de projeto e uma descrição de decisão estratégica
 e utiliza o modelo de linguagem configurado para avaliar prós, contras,
 riscos e fornecer recomendações.  Esta implementação inclui um método
 `analyze_trade_offs` que constrói um prompt rico em contexto e, em seguida,
 chama o `LLMRouter` para gerar a análise.  Caso o texto retornado esteja
 em JSON válido, ele será carregado em um dicionário; caso contrário, o
 texto bruto será retornado dentro de uma chave `raw_text`.

Nota: a integração real com diferentes modelos de linguagem é abstraída
 pela classe `BaseAgent` e pelo `LLMRouter`.  Durante a fase de
 desenvolvimento, utilize o parâmetro `dry_run=True` para evitar chamadas
 reais.
"""

from typing import Any, Dict
import json

from .base_agent import BaseAgent


class DecisionSupporter(BaseAgent):
    """Agente para analisar decisões estratégicas e oferecer recomendações."""

    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("decision_supporter", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any], decision: str) -> str:
        """
        Constrói um prompt que descreve o projeto e a decisão a ser analisada.

        O prompt final pede ao modelo que avalie prós, contras e riscos, e
        apresente uma recomendação em formato estruturado JSON para facilitar
        o pós-processamento.  Veja o método :meth:`analyze_trade_offs`.

        :param project_data: dicionário com dados do projeto (nome, tipo, país etc.).
        :param decision: descrição da decisão estratégica.
        :return: string de prompt.
        """
        name = project_data.get("name", "Projeto")
        project_type = project_data.get("project_type", "indefinido")
        country = project_data.get("country", "")

        return (
            "Você é um consultor de gestão de projetos experiente.\n"
            f"Projeto: {name}\n"
            f"Tipo: {project_type}\n"
            f"País: {country}\n"
            f"Decisão: {decision}\n\n"
            "Analise os prós, contras e riscos associados a esta decisão. "
            "Em seguida, forneça uma recomendação final que contemple os trade‑offs. "
            "Responda utilizando o seguinte formato JSON:\n"
            "{\n"
            "  \"pros\": [\"...\"],\n"
            "  \"cons\": [\"...\"],\n"
            "  \"risks\": [\"...\"],\n"
            "  \"recommendation\": \"...\"\n"
            "}\n"
        )

    def analyze_trade_offs(
        self,
        project_data: Dict[str, Any],
        decision: str,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """
        Executa a análise de trade‑offs para uma decisão estratégica.

        :param project_data: dicionário do projeto (name, project_type, country, etc.).
        :param decision: descrição da decisão a ser analisada.
        :param dry_run: se True, apenas exibe o prompt sem chamar o modelo.
        :return: um dicionário com os resultados (pros, cons, risks, recommendation).
        """
        prompt = self.build_prompt(project_data, decision)
        if dry_run:
            print(f"[DryRun] {self.name} → prompt gerado:\n{prompt}")
            return {}

        # Chama o modelo via LLMRouter. O router trata fallback de provedores.
        text = self.router.generate(self.model, prompt)
        try:
            return json.loads(text)
        except Exception:
            # Se o modelo não retornar JSON válido, retorna texto bruto em uma chave.
            return {"raw_text": text}
