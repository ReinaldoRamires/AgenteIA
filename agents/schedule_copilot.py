# agents/schedule_copilot.py
class ScheduleCopilot:
    """Gera a estrutura de trabalho (WBS) e o cronograma de um projeto."""

    def generate_schedule(self, project_type: str) -> list[dict]:
        """
        Gera uma lista de tarefas padrão para um tipo de projeto.
        No futuro, isso pode ler templates ou usar IA.
        """
        print("🤖 [Schedule Copilot] Gerando cronograma de tarefas padrão...")

        if project_type == "Software":
            return [
                {"name": "Fase 1: Discovery e Planejamento", "dor": "Briefing do projeto aprovado.", "dod": "Escopo e WBS definidos e validados.", "estimate": 8},
                {"name": "Fase 2: Design (UX/UI)", "dor": "WBS definida.", "dod": "Protótipos de alta fidelidade aprovados.", "estimate": 12},
                {"name": "Fase 3: Desenvolvimento", "dor": "Protótipos aprovados.", "dod": "Funcionalidades core implementadas e testadas.", "estimate": 40},
                {"name": "Fase 4: Lançamento", "dor": "Build de release aprovado.", "dod": "Produto em produção e monitorado.", "estimate": 4},
            ]
        else: # Padrão
            return [
                {"name": "Análise de Requisitos", "dor": "Ideia inicial apresentada.", "dod": "Documento de requisitos finalizado.", "estimate": 4},
                {"name": "Execução da Tarefa Principal", "dor": "Requisitos aprovados.", "dod": "Entrega principal concluída.", "estimate": 16},
                {"name": "Revisão e Validação", "dor": "Entrega principal concluída.", "dod": "Entrega validada pelo stakeholder.", "estimate": 2},
            ]