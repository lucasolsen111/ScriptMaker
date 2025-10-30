import streamlit as st
import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Create the AI model
model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')


def get_ai_ideas(transcript):
    """Generates video ideas from a transcript using the Gemini AI."""
    prompt = f"You are a viral video expert. Based on this transcript, generate 5 short-form video ideas, each on a new line:\n\n{transcript}"
    response = model.generate_content(prompt)
    return response.text.split('\n')


def get_ai_script(idea, transcript):
    """Generates a video script from an idea and transcript using the Gemini AI."""
    prompt = f"You are a professional scriptwriter. Write a short, punchy, 60-second video script based on this idea: {idea}\n\nHere is the original transcript for context:\n{transcript}"
    response = model.generate_content(prompt)
    return response.text


def revise_ai_script(script, feedback):
    """Revises a script based on feedback using the Gemini AI."""
    prompt = f"You are a script editor. Revise this script: {script}\n\nBased on this feedback: {feedback}"
    response = model.generate_content(prompt)
    return response.text


st.set_page_config(layout="wide")

# Initialize session state
if "ideas" not in st.session_state:
    st.session_state.ideas = []
if "script" not in st.session_state:
    st.session_state.script = ""


def main():
    st.title("YouTube Transcript-to-Script Workflow")

    # Step 1: Paste Your Transcript
    st.header("Step 1: Paste Your Transcript")
    transcript = st.text_area(
        "Paste your transcript here...", height=200, key="transcript"
    )

    # Step 2: Generate Ideas
    if st.button("1. Generate Ideas", key="generate_ideas"):
        with st.spinner("Generating ideas..."):
            st.session_state.ideas = get_ai_ideas(transcript)

    # Step 3: Choose Your Idea
    if st.session_state.ideas:
        st.header("Step 2: Choose Your Idea")
        chosen_idea = st.radio(
            "Choose your idea:", st.session_state.ideas, key="chosen_idea"
        )

        # Step 4: Generate Script for This Idea
        if st.button("2. Generate Script for This Idea", key="generate_script"):
            with st.spinner("Generating script..."):
                st.session_state.script = get_ai_script(chosen_idea, transcript)

    # Step 5: Your Generated Script
    if st.session_state.script:
        st.header("Step 3: Your Generated Script")
        st.text_area(
            "Your generated script:",
            value=st.session_state.script,
            height=400,
            key="script_output",
        )

        # Step 6: (Optional) Revise with Feedback
        st.header("Step 4: (Optional) Revise with Feedback")
        feedback = st.text_area(
            "Enter your feedback here...", height=150, key="feedback"
        )
        if st.button("3. Revise Script", key="revise_script"):
            with st.spinner("Revising script..."):
                st.session_state.script = revise_ai_script(
                    st.session_state.script, feedback
                )
            st.experimental_rerun()


if __name__ == "__main__":
    main()
