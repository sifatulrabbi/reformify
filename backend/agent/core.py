class AssistantAgent:
    prompt: object = ...

    def __init__(self, category: str, description: str):
        self.category = category
        self.description = description

        self._prepare_prompt()

    def _prepare_prompt(self): ...

    def _prepare_agent(self): ...

    def _execute_agent(self): ...
