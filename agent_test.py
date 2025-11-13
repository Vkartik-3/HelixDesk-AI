from autogen import UserProxyAgent
from agents.classifier_agent import get_classifier_agent

from agents.knowledge_base_agent import get_knowledge_base_agent
from tools.knowledge_base_tool import search_similar_solution




sample_tickets = [
    "The VPN isn't connecting since morning.",

]

def get_user_agent():
    user = UserProxyAgent(
        name="User", 
        human_input_mode="NEVER",
        code_execution_config=False,
    )
    return user

# 1. First agent testing
def run_test():

    user = get_user_agent()
    classifier = get_classifier_agent()

    for ticket in sample_tickets:
        print(f"\n🎟 Ticket: {ticket}")
        user.initiate_chat(
            recipient=classifier,
            message=f"Classify this ticket: {ticket}",
            max_turns=1
        )



# 2. Second agent testing
def run_kb_test():

    user = get_user_agent()

    # ✅ Register tool for execution with *this* user instance
    user.register_for_execution(
        name="search_similar_solution"
    )(search_similar_solution)

    knowledge_agent = get_knowledge_base_agent()

    user.initiate_chat(
        recipient=knowledge_agent,
        message="Use the tool search_similar_solution to find the fix for: My Outlook crashes every time I open it. Category is Software Bug",
        max_turns=2
    )


if __name__ == "__main__":
    # 1. test the classify agent
    # run_test()

    # 2. test the KB agent
    run_kb_test()
