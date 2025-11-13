import os
from dotenv import load_dotenv

load_dotenv()


llm_config={
            "temperature": 0,
            "config_list": [
                {
                    "model": os.getenv("AZURE_DEPLOYMENT_NAME"),  # This should match your deployment name
                    "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
                    "base_url": os.getenv("AZURE_OPENAI_ENDPOINT"),
                    "api_type": "azure",
                    "api_version": os.getenv("AZURE_API_VERSION")
                }
                ]
        }