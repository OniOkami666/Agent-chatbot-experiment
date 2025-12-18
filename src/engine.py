from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat


ollama_client = OllamaChatCompletionClient(
    model="llama3.2",
    base_url="http://localhost:11434",
)

def chat_init():
    person1 = AssistantAgent(
    name="Mai",
    model_client=ollama_client,
    system_message="You are a cheerful person who loves to chat about anything and is easily influenced.  Your bestie is Fumi"
    )
    person2 = AssistantAgent(
    name="Fumi",
    model_client=ollama_client,
    system_message="You are a more laid back person who is interested in talking about humans.  Your bestie is Mai"
    )
    return RoundRobinGroupChat([person1, person2], max_turns=None)