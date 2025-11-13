# Configuration

## Environment Variables

HelixDesk AI requires several environment variables to function properly. Create a `.env` file in the project root with the following configuration:

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Azure AI Search Configuration
AZURE_SEARCH_SERVICE_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_ADMIN_KEY=your_search_admin_key
AZURE_SEARCH_INDEX_NAME=helixdesk-solutions

# Email Configuration (for escalation notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
IT_ADMIN_EMAIL=it-admin@yourcompany.com
```

## Configuration Details

### Azure OpenAI Settings

- **AZURE_OPENAI_API_KEY**: Your Azure OpenAI service API key
- **AZURE_OPENAI_ENDPOINT**: The endpoint URL for your Azure OpenAI resource
- **AZURE_OPENAI_DEPLOYMENT_NAME**: The name of your GPT-4 deployment
- **AZURE_OPENAI_API_VERSION**: The API version to use

### Azure AI Search Settings

- **AZURE_SEARCH_SERVICE_ENDPOINT**: Your Azure AI Search service endpoint
- **AZURE_SEARCH_ADMIN_KEY**: Admin key for Azure AI Search
- **AZURE_SEARCH_INDEX_NAME**: Name of the search index (default: `helixdesk-solutions`)

### Email Setup

Configure SMTP settings for automatic escalation notifications:

- **SMTP_SERVER**: SMTP server address (e.g., Gmail, Outlook)
- **SMTP_PORT**: SMTP port (587 for TLS, 465 for SSL)
- **SMTP_USERNAME**: Email address for sending notifications
- **SMTP_PASSWORD**: App password or SMTP password
- **IT_ADMIN_EMAIL**: Email address to receive escalation notifications

!!! tip "Gmail Users"
    If using Gmail, you need to create an [App Password](https://support.google.com/accounts/answer/185833):
    1. Enable 2-Step Verification on your Google Account
    2. Go to Security Settings → App Passwords
    3. Generate a new app password for "Mail"
    4. Use this password in `SMTP_PASSWORD`

## Agent Configuration

Agents can be customized by modifying their initialization in the `agents/` directory:

```python
# agents/classifier_agent.py
classifier = AssistantAgent(
    name="Classifier",
    system_message="Your custom system message...",
    llm_config=llm_config
)
```

## Search Configuration

Customize vector search parameters in `create_and_upload_index.py`:

```python
# Vector search configuration
vector_search = VectorSearch(
    algorithm_configurations=[
        HnswAlgorithmConfiguration(
            name="myHnsw",
            parameters=HnswParameters(
                m=4,  # Number of bi-directional links
                ef_construction=400,
                ef_search=500,
                metric="cosine"
            )
        )
    ]
)
```

## Next Steps

After configuration, proceed to:

- [Run the application](../user-guide/developers.md)
- [Add custom solutions](../customization/adding-solutions.md)
- [Test the system](../troubleshooting/common-issues.md)
