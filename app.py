import streamlit as st
import time

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
            time.sleep(1)
        st.session_state.ideas = [
            "Idea 1: Turn the transcript into a rap song.",
            "Idea 2: Create a parody of a famous movie scene.",
            "Idea 3: Make a tutorial on how to do something mentioned in the transcript.",
            "Idea 4: Create a documentary-style video about the topic.",
            "Idea 5: Turn the transcript into a series of short, funny skits.",
        ]

    # Step 3: Choose Your Idea
    if st.session_state.ideas:
        st.header("Step 2: Choose Your Idea")
        chosen_idea = st.radio(
            "Choose your idea:", st.session_state.ideas, key="chosen_idea"
        )

        # Step 4: Generate Script for This Idea
        if st.button("2. Generate Script for This Idea", key="generate_script"):
            with st.spinner("Generating script..."):
                time.sleep(1)
            st.session_state.script = f"""
            **Title:** {chosen_idea}

            **Opening Scene:**

            [SCENE START]

            **INT. YOUTUBE STUDIO - DAY**

            A young, energetic YOUTUBER stands in front of a green screen.

            **YOUTUBER**
            (to camera)
            What's up, everyone! Welcome back to my channel. Today, we're going to do something a little different. We're going to turn this boring transcript into a rap song!

            [SCENE END]
            """

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
                time.sleep(1)
            st.session_state.script += f"\n\n**Revision based on feedback:**\n{feedback}"
            st.experimental_rerun()


if __name__ == "__main__":
    main()
