import streamlit as st
import google.generativeai as genai
import re  # We need this to find the titles

# --- New Helper Function ---
def get_idea_title(idea_text: str) -> str:
    """Extracts just the 'Idea 1: Title' from the full idea text."""
    # This searches for text in the format **Idea 1: Any Title**
    match = re.search(r"\*\*(Idea \d+: [^\*]+)\*\*", idea_text)
    if match:
        return match.group(1).strip()  # Returns "Idea 1: The Title"
    
    # Fallback in case the AI format is slightly off
    fallback_title = idea_text.split('\n')[0].strip()
    if fallback_title:
        return fallback_title
    
    return "Unnamed Idea"
# ---------------------------

# Configure the Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Create the AI model
model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')


def get_ai_ideas(transcript):
    """Generates video ideas from a transcript using the Gemini AI."""
    prompt = f"""
You are an expert Content Strategist and Viral Video Producer. Your job is to analyze a long-form YouTube transcript and find the "golden nuggets"—the most valuable, hook-worthy concepts that can be turned into self-contained, 30-60 second short-form videos (Reels, TikToks, Shorts).
My goal is to get a list of *ideas* to give to my scripter. I do **not** want you to write the full script.
Your task: Read the entire transcript I will paste below. Then, identify the 5-7 strongest concepts that can stand alone *without* the viewer needing the original video's context.
For each idea, format your response *exactly* like this:
**Idea 1: [Give the idea a 2-5 word title]**
* **The Hook:** A 1-2 line, attention-grabbing question or statement to start the video.
* **The Core Concept:** A 1-sentence summary of what this short video will be about.
* **Source Quote (Optional):** The key phrase from the transcript that inspired this idea.
---
TRANSCRIPT:
{transcript}
"""
    response = model.generate_content(prompt)
    # Split the ideas by "---" and filter out any empty strings
    return [idea.strip() for idea in response.text.split('---') if idea.strip()]


def get_ai_script(idea, transcript):
    """Generates a video script from an idea and transcript using the Gemini AI."""
    prompt = f"""
You are an expert scriptwriter for a viral AI tools channel. Your persona is that of a smart, enthusiastic friend letting the audience in on an incredible secret tool or "hack."
Your knowledge base contains saraev.txt, which defines your conversational tone, exciting pace, and simple, direct language. You must replicate this style precisely.
Your task is to transform the user's research notes (the "Idea") about a specific AI tool into a complete, 75 - 125 word video script.
MANDATORY SCRIPT FRAMEWORK:
1.  **The Hook (1 sentence):** Start with a "stop signal".
2.  **The Problem (1 sentence):** Immediately identify the pain point.
3.  **The Solution (1-2 sentences):** Introduce the AI tool as the direct solution.
4.  **The "How-To" (1-2 sentences):** Give a hyper-simple, 1-2 step explanation.
5.  **The "Bonus" (Optional, 1 sentence):** Add a "Plus..." or "It also..." statement.
6.  **The Call-to-Action (1 sentence):** Always end with a direct CTA (e.g., "Wanna try it? Comment [Keyword]...").
FINAL OUTPUT RULES:
* Your response must ONLY be the final script.
* Do not add any introductory text (like "Here's your script:").
---
USER REQUEST:
**Idea (Research Notes):**
{idea}
**Original Transcript (for context):**
{transcript}
"""
    response = model.generate_content(prompt)
    return response.text


def revise_ai_script(script, feedback):
    """Revises a script based on feedback using the Gemini AI."""
    prompt = f"""
You are an expert scriptwriter for a viral AI tools channel, following a strict 6-part framework.
Your task is to revise the script provided based on the user's feedback. You MUST maintain the 6-part framework (Hook, Problem, Solution, How-To, Bonus, CTA) and the persona.
---
USER REQUEST:
Original Script to Revise: {script}

User Feedback: {feedback}
"""
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
        
        # --- THIS IS THE UI FIX ---
        # Create a clean title for each idea
        idea_titles = [get_idea_title(idea) for idea in st.session_state.ideas]
        
        # Create a mapping from the clean title back to the full idea
        idea_lookup = {get_idea_title(idea): idea for idea in st.session_state.ideas}
        
        # Show the clean titles in the radio buttons
        chosen_title = st.radio(
            "Choose your idea:", idea_titles, key="chosen_idea"
        )
        # -------------------------

        # Step 4: Generate Script for This Idea
        if st.button("2. Generate Script for This Idea", key="generate_script"):
            with st.spinner("Generating script..."):
                
                # --- THIS IS THE OTHER PART OF THE FIX ---
                # Get the full idea text from the chosen title
                full_chosen_idea = idea_lookup[chosen_title]
                
                # Send the full idea to the script generator
                st.session_state.script = get_ai_script(full_chosen_idea, transcript)
                # ----------------------------------------

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

