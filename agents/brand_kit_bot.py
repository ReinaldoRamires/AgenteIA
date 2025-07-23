# agents/brand_kit_bot.py
import google.generativeai as genai
from rich.console import Console
import json
from src import models

console = Console()

class BrandKitBot:
    """
    Usa IA para gerar uma identidade de marca básica para um projeto.
    """
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        console.print("✅ [Brand Kit Bot] Inicializado.")

    def generate_kit(self, project: models.Project) -> dict:
        """
        Gera um kit de marca com slogan, missão e paleta de cores.
        """
        console.print(f"🎨 [Brand Kit Bot] Criando identidade de marca para: [bold green]{project.name}[/bold green]...")

        prompt = f"""
            Aja como um Estrategista de Marca (Brand Strategist).
            Para um novo projeto chamado "{project.name}", que é do tipo "{project.project_type}", 
            crie uma identidade de marca inicial.

            Forneça os seguintes elementos:
            - "slogan": Um slogan curto e impactante.
            - "mission_statement": Uma declaração de missão de uma frase.
            - "color_palette": Uma lista de 4 códigos de cor hexadecimais (HEX) que representem a marca, junto com o nome da cor (ex: "#FFFFFF (Branco Gelo)").

            Responda APENAS com um objeto JSON válido, sem nenhum texto adicional.
            O formato deve ser:
            {{
              "slogan": "...",
              "mission_statement": "...",
              "color_palette": ["...", "...", "...", "..."]
            }}
        """

        try:
            with console.status("[bold yellow]Aguardando IA criar a marca...[/bold yellow]"):
                response = self.model.generate_content(prompt)

            cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
            brand_kit = json.loads(cleaned_response)

            console.print("🎨 [Brand Kit Bot] Kit de marca gerado com sucesso!")
            return brand_kit
        except Exception as e:
            console.print(f"[bold red]ERRO ao gerar o kit de marca:[/bold red] {e}")
            return {}