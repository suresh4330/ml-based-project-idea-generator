import json
import os

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load env vars (optional – only needed for AI advantages)
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

try:
    import streamlit as st
except ImportError:
    st = None

data = pd.read_csv("dataset.csv")
data["content"] = (
    data["project_name"].fillna("") + " "
    + data["domain"].fillna("") + " "
    + data["description"].fillna("") + " "
    + data["technologies"].fillna("") + " "
    + data["learning_topics"].fillna("")
)

vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(data["content"])


def _apply_filters(frame, domain=None, difficulty=None, dataset_name=None):
    filtered = frame
    if domain and domain != "All":
        filtered = filtered[filtered["domain"] == domain]
    if difficulty and difficulty != "All":
        filtered = filtered[filtered["difficulty"] == difficulty]
    if dataset_name and dataset_name != "All":
        filtered = filtered[filtered["dataset"] == dataset_name]
    return filtered


def recommend_projects(
    user_input,
    top_n=5,
    domain=None,
    difficulty=None,
    dataset_name=None,
    advanced_mode=False,
):
    filtered = _apply_filters(data, domain, difficulty, dataset_name).copy()
    if filtered.empty:
        return filtered

    if user_input and user_input.strip():
        user_vec = vectorizer.transform([user_input])
        filtered_matrix = vectorizer.transform(filtered["content"])
        scores = cosine_similarity(user_vec, filtered_matrix)[0]
    else:
        scores = pd.Series([1.0] * len(filtered))

    filtered = filtered.assign(score=scores)

    if advanced_mode:
        difficulty_rank = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
        filtered["difficulty_boost"] = filtered["difficulty"].map(difficulty_rank).fillna(0)
        filtered["score"] = filtered["score"] + (filtered["difficulty_boost"] * 0.08)

    filtered = filtered.sort_values(by=["score", "project_name"], ascending=[False, True])
    return filtered.head(top_n).reset_index(drop=True)


def _split_stack(stack_text):
    parts = [part.strip() for part in stack_text.split() if part.strip()]
    return parts[:5] if parts else ["Python", "Pandas", "Scikit-learn"]


# ─────────────────────────────────────────────────────────────
# PART 1 — AI-Powered Advantage Generator (Claude claude-haiku-3)
# ─────────────────────────────────────────────────────────────

def _static_advantages(project_row, advanced_mode):
    """Fallback static advantages list."""
    adv = [
        f"Demonstrates strong portfolio value by combining {project_row['domain']} domain knowledge with an end-to-end production-grade build.",
        f"Proves interview-ready skills in {project_row['learning_topics'].lower()} — a topic actively sought by hiring teams.",
        f"Signals real-world impact through practical stack exposure with {project_row['technologies']}, aligning with industry workflows.",
    ]
    if advanced_mode:
        adv.append(
            "Production-grade advanced mode showcases deployment, monitoring, and retraining strategy — distinguishing your portfolio from basic tutorials."
        )
    else:
        adv.append(
            "Industry-aligned project structure demonstrates end-to-end thinking from data ingestion to model serving."
        )
    return adv


def _get_ai_advantages(project_name, domain, technologies, learning_topics, difficulty, advanced_mode):
    """Call Claude claude-haiku-3 to generate 4 compelling advantages. Returns list or None on failure."""
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key and st is not None:
        try:
            api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        except Exception:
            api_key = ""
    if not api_key:
        return None

    try:
        import anthropic  # noqa: PLC0415

        client = anthropic.Anthropic(api_key=api_key)
        prompt = f"""You are a senior ML engineer and tech career coach writing for a developer portfolio app.

Project details:
- Name: {project_name}
- Domain: {domain}
- Tech Stack: {technologies}
- Learning Topic: {learning_topics}
- Difficulty: {difficulty}
- Advanced Mode: {advanced_mode}

Write exactly 4 compelling project advantages. Each advantage MUST:
1. Be 1-2 sentences, sharp and confident in tone
2. Speak to career value, portfolio impact, or real-world industry use
3. Use power words: "demonstrates", "proves", "signals", "production-grade", "interview-ready", "end-to-end", "industry-aligned", "real-world impact"
4. Mention specific technical skill or industry application
5. If advanced_mode=True, focus on production, deployment, monitoring

Return ONLY a valid JSON array of 4 strings. No preamble. No markdown code blocks.
Example: ["Advantage one here.", "Advantage two here.", "...", "..."]"""

        message = client.messages.create(
            model="claude-haiku-3-5",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text.strip()
        return json.loads(raw)
    except Exception:
        return None


@st.cache_data(ttl=3600)
def _cached_ai_advantages(project_name, domain, technologies, learning_topics, difficulty, advanced_mode):
    return _get_ai_advantages(project_name, domain, technologies, learning_topics, difficulty, advanced_mode)


# ─────────────────────────────────────────────────────────────
# PART 3 — Effort Estimator helpers
# ─────────────────────────────────────────────────────────────

EFFORT_MAP = {
    "Beginner": {
        "weeks": "1–2 weeks",
        "dataset": 0.30,
        "model": 0.40,
        "ui": 0.25,
        "color": "#14b8a6",
    },
    "Intermediate": {
        "weeks": "2–4 weeks",
        "dataset": 0.55,
        "model": 0.65,
        "ui": 0.50,
        "color": "#f59e0b",
    },
    "Advanced": {
        "weeks": "4–8 weeks",
        "dataset": 0.85,
        "model": 0.90,
        "ui": 0.80,
        "color": "#ef4444",
    },
}


def compute_effort_score(difficulty, advanced_mode, stack_parts):
    rank = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
    score = rank.get(difficulty, 1) + (1 if advanced_mode else 0) + len(stack_parts) * 0.5
    return min(max(score, 1), 5)


def build_project_blueprint(project_row, user_goal, advanced_mode=False, show_spinner=True):
    goal = user_goal.strip() if user_goal and user_goal.strip() else project_row["project_name"]
    stack_parts = _split_stack(project_row["technologies"])
    first_stack = stack_parts[0]

    milestones = [
        "Define the target user, business problem, and the metric that proves the model is useful.",
        f"Collect a {project_row['dataset'].lower()} and prepare a clean training pipeline with validation splits.",
        f"Build a baseline using {first_stack} tools, then compare it with an improved model using stronger features.",
        "Create a simple interface for predictions, explainability, and demo-ready outputs.",
    ]

    if advanced_mode:
        milestones.extend([
            "Add experiment tracking, error analysis, and model comparison across multiple runs.",
            "Package the pipeline for deployment with monitoring, feedback loops, and retraining strategy.",
        ])

    workflow = [
        "Input data enters the preprocessing pipeline for cleaning, labeling, and feature creation.",
        "A training module builds the model and evaluates it on held-out validation data.",
        "Prediction results are served inside an app or dashboard so users can test real scenarios.",
        "Feedback from users or errors is used to improve the model in later versions.",
    ]

    build_steps = [
        "Set up the environment and install the core libraries for the selected stack.",
        "Create the dataset loader, data-cleaning notebook, and first baseline training script.",
        "Measure accuracy or relevant metrics, then improve the pipeline feature by feature.",
        "Build the final UI, write a short README, and prepare screenshots for your portfolio.",
    ]

    advanced_addons = [
        "Add authentication or role-based access if the project serves multiple users.",
        "Store prediction logs for monitoring and future retraining.",
        "Use Docker or cloud deployment so the project can be demonstrated live.",
        "Add explainability views such as feature importance or confidence scores.",
    ]

    architecture_map = [
        "User Input → Data Validation",
        "Data Validation → Feature Engineering",
        "Feature Engineering → Model Training / Inference",
        "Model Output → Dashboard or API Response",
        "Dashboard or API Response → Monitoring and Feedback",
    ]

    # ── PART 1: AI Advantages ──────────────────────────────────
    difficulty_label = "Advanced" if advanced_mode else project_row["difficulty"]
    ai_adv = None
    if show_spinner:
        with st.spinner("✨ Generating AI-powered advantages..."):
            ai_adv = _cached_ai_advantages(
                project_row["project_name"],
                project_row["domain"],
                project_row["technologies"],
                project_row["learning_topics"],
                difficulty_label,
                advanced_mode,
            )
    else:
        ai_adv = _cached_ai_advantages(
            project_row["project_name"],
            project_row["domain"],
            project_row["technologies"],
            project_row["learning_topics"],
            difficulty_label,
            advanced_mode,
        )

    advantages = ai_adv if (isinstance(ai_adv, list) and len(ai_adv) == 4) else _static_advantages(project_row, advanced_mode)

    # ── PART 3: Effort ────────────────────────────────────────
    effort_score = compute_effort_score(difficulty_label, advanced_mode, stack_parts)
    effort_data = EFFORT_MAP.get(difficulty_label, EFFORT_MAP["Intermediate"])

    return {
        "idea_name": f"{goal.title()} Accelerator",
        "problem": (
            f"Build a practical {project_row['domain'].lower()} project inspired by "
            f"{project_row['project_name']} for developers who want a stronger real-world portfolio piece."
        ),
        "core_stack": project_row["technologies"],
        "stack_parts": stack_parts,
        "dataset_plan": project_row["dataset"],
        "learning_focus": project_row["learning_topics"],
        "difficulty": difficulty_label,
        "advantages": advantages,
        "workflow": workflow,
        "build_steps": build_steps,
        "milestones": milestones,
        "advanced_addons": advanced_addons if advanced_mode else [],
        "architecture_map": architecture_map,
        # effort
        "effort_score": effort_score,
        "effort_weeks": effort_data["weeks"],
        "effort_dataset": effort_data["dataset"],
        "effort_model": effort_data["model"],
        "effort_ui": effort_data["ui"],
        "effort_color": effort_data["color"],
    }
