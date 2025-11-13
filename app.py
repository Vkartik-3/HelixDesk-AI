import streamlit as st
# Page config must be the first Streamlit command in the script
st.set_page_config(page_title="SupportX AI Assist", page_icon="🤖", layout="centered")

from group_chat import user, manager, notification_agent
import random
import string

# Ticket generator
def generate_ticket_id(prefix="TKT", length=6):
    """Generate a random alphanumeric ticket ID."""
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"{prefix}-{suffix}"

# Load custom CSS (relative to this file)
import os
HERE = os.path.dirname(__file__)
css_path = os.path.join(HERE, "style.css")
try:
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    # If the CSS file is missing, continue without crashing and show a small notice in the app
    st.warning("style.css not found — continuing without custom styles.")

# Title and subtitle block
st.markdown("""
<div class="title-container">
    <h1>🤖 SupportX AI Assist </h1>
</div>
<div class="subtitle">Your Personalized AI IT Support Assistant</div>
<div class="description"><em>Facing a tech issue? Describe it below and let SupportX AI Assist handle it for you.</em></div>
""", unsafe_allow_html=True)

# Session state setup
if "final_response" not in st.session_state:
    st.session_state.final_response = None
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "awaiting_feedback" not in st.session_state:
    st.session_state.awaiting_feedback = False
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False

# Input section
st.markdown('<div class="input-label">💬 <strong>Describe your IT issue:</strong></div>', unsafe_allow_html=True)
user_input = st.text_area("", value=st.session_state.user_input, height=150)

# Submit logic
if st.button("🚀 Resolve Now") and user_input.strip():
    with st.spinner("SupportX AI Assist is resolving your issue..."):
        st.session_state.user_input = user_input
        responses = []

        original_receive = user.receive

        def receive_and_capture(*args, **kwargs):
            if len(args) >= 2:
                message = args[0]
                if isinstance(message, dict):
                    content = message.get("content", "")
                    if content:
                        responses.append(content)
            return original_receive(*args, **kwargs)

        user.receive = receive_and_capture
        user.initiate_chat(recipient=manager, message=user_input)
        user.receive = original_receive

        if responses:
            final = responses[-1]
            st.session_state.final_response = final
            st.session_state.awaiting_feedback = True
            st.session_state.feedback_given = False
            st.success("✅ **AI Response:**")
            st.markdown(final)
        else:
            st.warning("⚠️ No response received from the agents.")

# Feedback section
if st.session_state.awaiting_feedback and st.session_state.final_response and not st.session_state.feedback_given:
    st.markdown("### 🙋 Was this solution helpful?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Yes, issue resolved"):
            st.session_state.feedback_given = True
            st.session_state.awaiting_feedback = False
            st.success("🎉 Great! We're glad your issue is resolved. Thank you!")

    with col2:
        if st.button("❌ No, not helpful"):
            st.session_state.feedback_given = True
            st.session_state.awaiting_feedback = False
            ticket_id = generate_ticket_id()
            st.warning(f"⚠️ We're escalating this issue to IT support.\n\n📄 **Ticket Created: `{ticket_id}`**")

            # Compose escalation message
            notification_message = (
                f"🚨 Unresolved IT Issue\n\n"
                f"User reported: '{st.session_state.user_input}'\n"
                f"📄 Ticket ID: {ticket_id}"
            )

            reply = notification_agent.generate_reply(
                messages=[{"role": "user", "content": notification_message}],
                sender=user
            )

            final_reply = reply.get("content") if isinstance(reply, dict) else str(reply)
            st.info(f"📨 **Notification Agent Response:**\n\n{final_reply}")
