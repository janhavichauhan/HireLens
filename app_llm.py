import streamlit as st
from llm_evaluator import LLMEvaluator
from interview_conversation import InterviewConversation
import json

@st.cache_resource
def load_evaluator():
    return LLMEvaluator()

def main():
    st.set_page_config(page_title="HireLens", page_icon="🤖", layout="wide")

    st.title("🤖 HireLens")
    st.markdown("""
        An intelligent interview system powered by Local LLM (Ollama).
        Experience adaptive, multi-turn interviews with intelligent feedback.
    """)

    # Check Ollama connection
    evaluator = load_evaluator()
    if not evaluator.check_connection():
        st.error("""
        ❌ **Ollama is not running!**

        1. Download Ollama: https://ollama.ai
        2. Install and run: `ollama serve`
        3. In another terminal, pull a model: `ollama pull mistral`
        4. Refresh this page
        """)
        return

    st.success("✓ Connected to Ollama LLM")

    # Initialize session state
    if 'interview_session' not in st.session_state:
        st.session_state.interview_session = None
    if 'interview_history' not in st.session_state:
        st.session_state.interview_history = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = ""
    if 'turn_count' not in st.session_state:
        st.session_state.turn_count = 0

    # Sidebar: Setup
    st.sidebar.header("📋 Interview Setup")

    topics = [
        "Machine Learning",
        "Python Programming",
        "Data Science",
        "Web Development",
        "Database Design",
        "System Design",
        "Custom Topic"
    ]

    selected_topic = st.sidebar.selectbox("Select Interview Topic:", topics)

    if selected_topic == "Custom Topic":
        topic = st.sidebar.text_input("Enter custom topic:")
    else:
        topic = selected_topic

    keywords_input = st.sidebar.text_area(
        "Enter expected keywords/concepts (one per line, optional):",
        height=100
    )
    keywords = [kw.strip() for kw in keywords_input.split('\n') if kw.strip()]

    num_turns = st.sidebar.slider("Number of questions in interview:", 1, 5, 3)

    # Start Interview Button
    if st.sidebar.button("🚀 Start Interview", key="start_interview"):
        st.session_state.interview_session = InterviewConversation(topic, keywords)
        st.session_state.current_question = st.session_state.interview_session.start_interview()
        st.session_state.turn_count = 1
        st.session_state.interview_history = []
        st.rerun()

    # Main Content
    if st.session_state.interview_session is None:
        st.info("👈 Configure interview settings and click 'Start Interview' to begin")
        return

    interview = st.session_state.interview_session

    # Display progress
    st.progress(st.session_state.turn_count / num_turns)
    st.write(f"**Question {st.session_state.turn_count} of {num_turns}**")

    # Current Question
    st.subheader("📝 Current Question")
    st.write(f"> {st.session_state.current_question}")

    # Answer Input
    st.subheader("Your Answer")
    answer = st.text_area("Type your answer here:", height=150, key=f"answer_{st.session_state.turn_count}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Submit Answer", key="submit"):
            if not answer.strip():
                st.warning("Please enter an answer before submitting.")
            else:
                with st.spinner("🤔 Evaluating your answer..."):
                    # Process answer
                    result = interview.process_answer(st.session_state.current_question, answer)
                    st.session_state.interview_history.append({
                        "question": st.session_state.current_question,
                        "answer": answer,
                        "evaluation": result["evaluation"]
                    })

                    # Display Evaluation
                    st.subheader("📊 Evaluation Results")

                    col_score, col_accuracy = st.columns(2)
                    with col_score:
                        score = result["evaluation"].get("score", 5)
                        st.metric("Score", f"{score}/10", delta=None)

                    with col_accuracy:
                        st.metric("Status", result["evaluation"].get("accuracy", "Evaluated"))

                    # Feedback
                    col_strength, col_improve = st.columns(2)

                    with col_strength:
                        st.markdown("### 💪 Strengths")
                        strengths = result["evaluation"].get("strengths", [])
                        for s in strengths:
                            st.write(f"✓ {s}")

                    with col_improve:
                        st.markdown("### 📈 Areas to Improve")
                        improvements = result["evaluation"].get("areas_for_improvement", [])
                        for imp in improvements:
                            st.write(f"→ {imp}")

                    # Overall Feedback
                    st.markdown("### 💬 Feedback")
                    st.write(result["evaluation"].get("overall_feedback", ""))

                    # Proceed to next question or finish
                    if st.session_state.turn_count < num_turns:
                        if st.button("➡️ Next Question"):
                            with st.spinner("Generating next question..."):
                                st.session_state.current_question = interview.get_next_question(
                                    answer,
                                    num_questions=1
                                )
                                st.session_state.turn_count += 1
                                st.rerun()
                    else:
                        if st.button("🏁 Finish Interview"):
                            st.session_state.show_summary = True
                            st.rerun()

    with col2:
        if st.button("🎯 Generate Follow-up Questions"):
            with st.spinner("Generating follow-up questions..."):
                followups = interview.evaluator.generate_followup_questions(
                    st.session_state.current_question,
                    answer,
                    num_questions=3
                )
                st.markdown("### 🎯 Suggested Follow-ups")
                for i, q in enumerate(followups, 1):
                    st.write(f"{i}. {q}")

    # Show Summary if Interview Complete
    if st.session_state.turn_count >= num_turns:
        st.divider()
        st.subheader("📋 Interview Summary")

        summary = interview.get_interview_summary()

        col_summary_score, col_summary_level = st.columns(2)
        with col_summary_score:
            st.metric("Average Score", f"{summary['average_score']}/10")
        with col_summary_level:
            scores = summary['scores']
            trend = "📈 Improving" if scores[-1] > scores[0] else "📉 Declining" if scores[-1] < scores[0] else "➡️ Stable"
            st.metric("Trend", trend)

        st.markdown("### 📊 Performance Summary")
        st.write(summary['summary'])

        # All Q&A History
        st.markdown("### 📚 Full Interview Transcript")
        for item in st.session_state.interview_history:
            with st.expander(f"Q: {item['question'][:60]}..."):
                st.write(f"**Question:** {item['question']}")
                st.write(f"**Your Answer:** {item['answer']}")
                st.write(f"**Score:** {item['evaluation'].get('score', 0)}/10")
                st.write(f"**Feedback:** {item['evaluation'].get('overall_feedback', '')}")

        # Export Results
        if st.button("📥 Export Results as JSON"):
            export_data = interview.export_results()
            st.download_button(
                label="Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name="interview_results.json",
                mime="application/json"
            )

        if st.button("🔄 Start New Interview"):
            st.session_state.interview_session = None
            st.session_state.interview_history = []
            st.rerun()

if __name__ == "__main__":
    main()
