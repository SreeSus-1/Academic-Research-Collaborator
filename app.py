import streamlit as st
import pandas as pd

from agents.literature_review_agent import LiteratureReviewAgent
from agents.hypothesis_validator_agent import HypothesisValidatorAgent
from agents.draft_polisher_agent import DraftPolisherAgent
from memory.research_db import save_research_session, get_all_sessions

st.set_page_config(page_title="Academic Research Collaborator", layout="wide")

literature_agent = LiteratureReviewAgent()
hypothesis_agent = HypothesisValidatorAgent()
draft_agent = DraftPolisherAgent()

st.title("Academic Research Collaborator")
st.subheader("Multi-Agent Research Assistant for Scholars")

menu = st.sidebar.selectbox(
    "Choose Option",
    ["New Research Session", "Research Memory", "About"]
)

if menu == "New Research Session":
    st.header("Enter Research Inputs")

    research_question = st.text_input(
        "Research Question",
        "How does retrieval-augmented generation improve factual accuracy in domain-specific question answering?"
    )

    citations = st.text_area(
        "Citations / References",
        """Lewis et al. (2020) Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.
Gao et al. (2023) Retrieval-Augmented Generation for Large Language Models: A Survey.
Shuster et al. (2021) Retrieval Augmentation Reduces Hallucination in Dialogue Systems."""
    )

    notes = st.text_area(
        "Research Notes",
        "Prior work suggests retrieval improves factual grounding, but performance depends on retrieval quality, chunking strategy, and domain relevance."
    )

    hypothesis = st.text_area(
        "Hypothesis",
        "Retrieval-augmented generation improves factual accuracy in domain-specific QA when retrieval quality and document grounding are strong."
    )

    draft_text = st.text_area(
        "Draft Section",
        "Retrieval-augmented generation has emerged as a promising approach for improving factual correctness in language model outputs. By incorporating external knowledge at inference time, RAG systems can reduce hallucination and improve domain adaptation."
    )

    progress_note = st.text_area(
        "Progress Note",
        "Initial draft focused on factual grounding and domain-specific retrieval."
    )

    if st.button("Run Research Collaboration"):
        with st.spinner("Generating literature review..."):
            literature_review = literature_agent.run(research_question, citations, notes)

        if literature_review.startswith("ERROR:"):
            st.error(f"Literature Review Agent failed: {literature_review}")
        else:
            with st.spinner("Validating hypothesis..."):
                hypothesis_feedback = hypothesis_agent.run(research_question, hypothesis, citations, notes)

            if hypothesis_feedback.startswith("ERROR:"):
                st.warning("Literature review generated, but hypothesis validation timed out.")
                st.subheader("Literature Review")
                st.write(literature_review)
            else:
                with st.spinner("Polishing draft..."):
                    polished_draft = draft_agent.run(research_question, draft_text)

                if polished_draft.startswith("ERROR:"):
                    st.warning("Literature review and hypothesis feedback generated, but draft polishing timed out.")
                    st.subheader("Literature Review")
                    st.write(literature_review)
                    st.subheader("Hypothesis Feedback")
                    st.write(hypothesis_feedback)
                else:
                    save_research_session(
                        research_question,
                        citations,
                        notes,
                        hypothesis,
                        draft_text,
                        literature_review,
                        hypothesis_feedback,
                        polished_draft,
                        progress_note
                    )

                    st.success("Research session completed and saved.")

                    st.subheader("Literature Review")
                    st.write(literature_review)

                    st.subheader("Hypothesis Validation")
                    st.write(hypothesis_feedback)

                    st.subheader("Polished Draft")
                    st.write(polished_draft)

elif menu == "Research Memory":
    st.header("Saved Research Sessions")

    sessions = get_all_sessions()

    if sessions:
        df = pd.DataFrame(sessions)
        st.dataframe(
            df[["timestamp", "research_question", "progress_note"]],
            use_container_width=True
        )

        selected_index = st.number_input(
            "Select research session index",
            min_value=0,
            max_value=len(sessions) - 1,
            step=1
        )

        session = sessions[selected_index]

        st.subheader("Research Question")
        st.write(session["research_question"])

        st.write(f"Saved on: {session['timestamp']}")
        st.write(f"Progress Note: {session['progress_note']}")

        st.markdown("### Citations")
        st.write(session["citations"])

        st.markdown("### Notes")
        st.write(session["notes"])

        st.markdown("### Hypothesis")
        st.write(session["hypothesis"])

        st.markdown("### Original Draft")
        st.write(session["draft_text"])

        st.markdown("### Literature Review")
        st.write(session["literature_review"])

        st.markdown("### Hypothesis Feedback")
        st.write(session["hypothesis_feedback"])

        st.markdown("### Polished Draft")
        st.write(session["polished_draft"])
    else:
        st.info("No research sessions found yet.")

else:
    st.header("About")
    st.markdown("""
This application supports academic writing using three specialized AI agents:
- Literature Review Agent
- Hypothesis Validator Agent
- Draft Polisher Agent

It stores research sessions, evolving drafts, and progress notes over time.
""")