from tinydb import TinyDB
from datetime import datetime

db = TinyDB("research_memory.json")

def save_research_session(
    research_question,
    citations,
    notes,
    hypothesis,
    draft_text,
    literature_review,
    hypothesis_feedback,
    polished_draft,
    progress_note="Initial research session"
):
    db.insert({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "research_question": research_question,
        "citations": citations,
        "notes": notes,
        "hypothesis": hypothesis,
        "draft_text": draft_text,
        "literature_review": literature_review,
        "hypothesis_feedback": hypothesis_feedback,
        "polished_draft": polished_draft,
        "progress_note": progress_note
    })

def get_all_sessions():
    return db.all()