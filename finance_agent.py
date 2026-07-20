import platform
from gaia.agents.base.agent import Agent

class FinanceAgent(Agent):
    def _get_system_prompt(self) -> str:
        return """A simple agent that reads news headlines and responds with 'good', 'neutral', or 'bad', depending on the conotation of the headline."""

agent = FinanceAgent()
result = agent.process_query("The company reported record profits.")
print(result.get("result"))

