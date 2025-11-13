# Quick Start Guide

Get HelixDesk AI running in **10 minutes**!

## Prerequisites Checklist

Before you begin, make sure you have:

- [x] **Python 3.13+** installed
- [x] **Azure Account** with OpenAI access
- [x] **Git** installed
- [x] **Gmail account** (for email escalation)
- [x] **Terminal/Command Prompt** access

---

## Step 1: Clone the Repository

=== "HTTPS"
    ```bash
    git clone https://github.com/Vkartik-3/HelixDesk-AI.git
    cd helixdesk-ai
    ```

=== "SSH"
    ```bash
    git clone git@github.com:kartikvadhawana/helixdesk-ai.git
    cd helixdesk-ai
    ```

=== "GitHub CLI"
    ```bash
    gh repo clone kartikvadhawana/helixdesk-ai
    cd helixdesk-ai
    ```

---

## Step 2: Create Virtual Environment

=== "macOS/Linux"
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

=== "Windows"
    ```bash
    python -m venv env
    env\Scripts\activate
    ```

You should see `(env)` in your terminal prompt.

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required packages (takes 2-3 minutes).

---

## Step 4: Configure Environment Variables

1. Open the `.env` file in the project root
2. Replace placeholders with your actual Azure credentials:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_DEPLOYMENT_NAME=gpt-4
AZURE_API_VERSION=2024-12-01-preview
AZURE_OPENAI_API_KEY=your-api-key-here

# Azure AI Search Configuration
AZURE_SEARCH_ENDPOINT=https://your-search.search.windows.net
AZURE_SEARCH_KEY=your-search-admin-key-here
AZURE_OPENAI_DEPLOYMENT=text-embedding-3-small
```

!!! warning "Don't Have Azure Credentials?"
    See the [Azure Setup Guide](../setup/azure-setup.md) for detailed instructions on creating Azure resources.

---

## Step 5: Create Search Index

Upload the knowledge base to Azure AI Search:

```bash
python create_and_upload_index.py
```

**Expected output:**
```
Creating index...
Index created successfully.
Loading knowledge base from data/knowledge_base.json...
Preparing documents with embeddings...
100%|████████████████████████| 20/20 [00:15<00:00,  1.30it/s]
Uploading documents in batches of 10...
Batch 1 uploaded successfully.
Batch 2 uploaded successfully.
All documents uploaded successfully.
```

⏱️ **Takes**: 15-30 seconds

---

## Step 6: Run the Application

Start the Streamlit web interface:

```bash
streamlit run app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.100:8501
```

🎉 **Success!** Open your browser and go to `http://localhost:8501`

---

## Step 7: Test It Out

### Test Case 1: Simple Issue

1. In the text area, enter: **"My VPN won't connect"**
2. Click **"Resolve Now"**
3. You should see:
   - **Classification**: Network Issue
   - **Solution**: VPN troubleshooting steps
   - **"Did this help?"** buttons

### Test Case 2: Known Issue

1. Enter: **"I forgot my password"**
2. Click **"Resolve Now"**
3. You should see:
   - **Classification**: Password Reset
   - **Solution**: Password reset instructions

### Test Case 3: Escalation

1. Enter: **"My coffee machine is broken"** (not in knowledge base)
2. Click **"Resolve Now"**
3. Wait for solution (might not be great)
4. Click **"No, not helpful"**
5. You should see:
   - **Ticket ID** generated (e.g., `TKT-A3F8D2`)
   - **Escalation confirmation** message
   - **Email sent** to IT support

---

## Common Issues

!!! bug "Connection Error"
    **Problem**: `openai.APIConnectionError`

    **Solution**: Check your `.env` file—ensure the Azure endpoint ends with `/` and the API key is correct.

!!! bug "Index Not Found"
    **Problem**: `Index 'it-ticket-solutions-index' not found`

    **Solution**: Run `python create_and_upload_index.py` to create the index.

!!! bug "Module Not Found"
    **Problem**: `ModuleNotFoundError: No module named 'streamlit'`

    **Solution**: Activate your virtual environment and run `pip install -r requirements.txt`

For more issues, see [Troubleshooting](../troubleshooting/common-issues.md).

---

## Next Steps

Now that you have HelixDesk AI running:

1. **[Customize the Knowledge Base](../customization/adding-solutions.md)** - Add your organization's solutions
2. **[Configure Email Settings](../setup/configuration.md#email-setup)** - Set up escalation emails
3. **[Understand the Architecture](../architecture/overview.md)** - Learn how it works
4. **[Create Custom Agents](../customization/creating-agents.md)** - Extend functionality

---

## Video Tutorial

!!! tip "Coming Soon"
    A video walkthrough of the quick start guide will be available soon!

---

## Need Help?

- 📖 **[Full Documentation](../index.md)**
- 💬 **[GitHub Discussions](https://github.com/Vkartik-3/HelixDesk-AI/discussions)**
- 🐛 **[Report Issues](https://github.com/Vkartik-3/HelixDesk-AI/issues)**
- 📧 **[Email Support](mailto:kartikvadhwana7@gmail.com)**
