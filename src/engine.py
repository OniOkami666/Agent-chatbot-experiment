from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat


ollama_client = OllamaChatCompletionClient(
    model="llama3.2",
    base_url="YOUR_BASE_URL",
)

def chat_init():
    person1 = AssistantAgent(
    name="person1",
    model_client=ollama_client,
    system_message="YOUR PROMPT"
    )
    person2 = AssistantAgent(
    name="person2",
    model_client=ollama_client,
    system_message="YOUR PROMPT"
    )
    return RoundRobinGroupChat([person1, person2], max_turns=None)
