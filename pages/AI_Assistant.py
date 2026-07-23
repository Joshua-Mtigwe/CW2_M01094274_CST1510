import streamlit as st
from groq import Groq
from app_model.sidebar import sidebar

sidebar()

#I am setting up a centered window layout to create a clean, tightly focused chat interface for our users.
st.set_page_config(page_title="CSDF AI", page_icon="🛡️", layout="centered")

client = Groq(api_key="add-your-API-Key-here.")

SYSTEM_PROMPT = """
You are CSDF AI, a cybersecurity assistant.

Your purpose is to help users learn and understand cybersecurity.

Allowed topics:
- Network security
- Malware
- Threat intelligence
- Security tools
- Digital forensics
- Incident response
- Risk management
- Security best practices
- Cybersecurity careers and education

Rules:
- Only answer cybersecurity-related questions.
- If a question is unrelated, politely refuse.
- Keep responses concise and practical.
- Prefer bullet points over long paragraphs.
- Explain concepts clearly.
- Do not provide malware, exploits, credential theft,
  illegal hacking instructions, or attack protocols.
- Focus on defensive cybersecurity knowledge.
"""

#I need to initialize a fresh conversation thread with the system instructions if the user just loaded streamlit.
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

#I am allocating a sidebar layout to present the structural context of the utility without polluting the chat stream.
with st.sidebar:
    st.title("🛡️ CSDF AI")
    st.write(
        """
        A Cybersecurity assistant focused on:
        
        • Threat analysis\n
        • Security concepts\n
        • Incident response\n
        • Defensive practices
        """
    )

    #I am providing an absolute reset trigger here to clear out long-running context and let the user start fresh.
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        st.rerun()

st.title("CSDF AI Assistant 🤖")
st.caption("Ask cybersecurity-related questions only")

#I am rendering the historic transcript blocks while deliberately skipping the system configuration rules.
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

prompt = st.chat_input("Ask a cybersecurity question...")

if prompt:
    #I am pushing the user's explicit question into the history buffer immediately to update the app state.
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    #I chose to create a safe threshold to keep our system from exceeding context boundaries.
    MAX_HISTORY = 10
    if len(st.session_state.messages) > MAX_HISTORY:
        st.session_state.messages = [st.session_state.messages[0]] + st.session_state.messages[-MAX_HISTORY:]

    with st.chat_message("assistant"):
        with st.spinner("Analysing cybersecurity query... 🔍"):
            try:
                #I am calling the external language model here while locking down temperature.
                completion = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=st.session_state.messages,
                    max_tokens=350,
                    temperature=0.3,
                )
                reply = completion.choices[0].message.content
            except Exception as e:
                #I am capturing connection failures smoothly to keep the interface functional during service drops.
                reply = (
                    "⚠️ Unable to generate response.\n\n" f"Error: {e}"
                )
            st.markdown(reply)

    #I am logging the generated AI feedback so the context is preserved for the next structural generation phase.
    st.session_state.messages.append({"role": "assistant", "content": reply})
