from autogen import AssistantAgent
from utility.llm_config import llm_config


def get_notification_agent():
    return AssistantAgent(
        name="NotificationAgent",
        system_message="You are an IT notification agent that sends alerts or escalates unresolved tickets.",
        llm_config=llm_config
    )

