from autogen import AssistantAgent
from tools.knowledge_base_tool import search_similar_solution
from utility.llm_config import llm_config


def get_knowledge_base_agent():
    
    knowledge_agent = AssistantAgent(
        name="KnowledgeBaseAgent",
        system_message=(
            "You are an IT support assistant that retrieves solutions to user issues. "
            "Always call the 'search_similar_solution' tool with the query to get a matching solution. "
            "After calling, summarize the top solution and respond with TERMINATE."
         
        ),
        llm_config=llm_config,  # Required for tool registration
        code_execution_config={"use_docker": False},
    )

    # Register tool with LLM and executor
    # 1. LLm knows when to call the tool
    knowledge_agent.register_for_llm(
        name="search_similar_solution",
        description="Searches for top IT solutions from a knowledge base using a vector similarity search. Accepts query and top_k."
    )(search_similar_solution)

    # 2. Executed the tool
    knowledge_agent.register_for_execution(
        name="search_similar_solution"
    )(search_similar_solution)

    return knowledge_agent





