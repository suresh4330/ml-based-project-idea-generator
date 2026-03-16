"""
ML-Based Project Idea Generator — Advanced Production-Grade App
All 8 upgrade parts implemented.
"""

import random

import pandas as pd
import plotly.express as px
import streamlit as st

from learning_resources import RESOURCES, SKILL_LINKS, get_resource
from recommender import build_project_blueprint, data, recommend_projects
from similarity import similar_projects

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ML Project Idea Generator",
    page_icon="🤖",
    layout="wide",
)


@st.cache_data
def load_data():
    return pd.read_csv("dataset.csv")


dataset = load_data()


def build_filter_options(series):
    values = sorted({str(value).strip() for value in series.dropna() if str(value).strip()})
    return ["All"] + values

# ─────────────────────────────────────────────────────────────
# PART 6 — Advanced Dark / Futuristic CSS Theme
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">

    <style>
    /* ── Global ── */
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif !important;
    }
    .stApp {
        background: #0f1117;
        color: #e2e8f0;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 1260px;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #161b27 100%) !important;
        border-right: 1px solid rgba(99,102,241,0.15);
    }
    [data-testid="stSidebar"] * {
        color: #cbd5e1 !important;
    }
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stSelectbox label {
        color: #94a3b8 !important;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    /* ── Hero ── */
    .hero-shell {
        border-radius: 28px;
        padding: 2.2rem 2.4rem;
        background: linear-gradient(135deg, #0d1b2a 0%, #1a1040 60%, #0f1117 100%);
        border: 1px solid rgba(99,102,241,0.22);
        box-shadow: 0 0 60px rgba(99,102,241,0.08), 0 24px 60px rgba(0,0,0,0.35);
        margin-bottom: 1.4rem;
        overflow: hidden;
        position: relative;
    }
    .hero-shell::before {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 320px; height: 320px;
        background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-eyebrow {
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.78rem;
        font-weight: 700;
        color: #6366f1;
        margin-bottom: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
    }
    .hero-title {
        font-size: 2.6rem;
        line-height: 1.05;
        font-weight: 800;
        max-width: 800px;
        margin-bottom: 0.8rem;
        color: #f1f5f9;
    }
    .hero-title span { color: #6366f1; }
    .hero-copy {
        max-width: 800px;
        color: rgba(203,213,225,0.75);
        font-size: 1rem;
    }

    /* ── Cards ── */
    .card, .feature-card, .project-card, .soft-card {
        background: rgba(22, 27, 39, 0.9);
        border: 1px solid rgba(99,102,241,0.18);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.25);
        backdrop-filter: blur(12px);
        transition: all 0.2s ease;
    }
    .card, .soft-card { padding: 1.25rem; }
    .feature-card {
        padding: 1.3rem;
        min-height: 170px;
    }
    .project-card {
        padding: 1.15rem 1.2rem 0.6rem 1.2rem;
        margin-bottom: 1rem;
    }
    .project-card:hover {
        border-color: rgba(99,102,241,0.5);
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(99,102,241,0.12);
    }

    /* ── Typography ── */
    .section-label {
        color: #6366f1;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-size: 0.72rem;
        font-weight: 700;
        margin-bottom: 0.45rem;
        font-family: 'JetBrains Mono', monospace;
    }
    .section-title {
        color: #e2e8f0;
        font-size: 1.22rem;
        font-weight: 800;
        margin-bottom: 0.75rem;
    }
    .metric-title {
        font-size: 0.78rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-value {
        font-size: 2rem;
        color: #6366f1;
        font-weight: 800;
        margin-top: 0.2rem;
    }
    .mini-note {
        color: #64748b;
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }

    /* ── Tags ── */
    .tag {
        display: inline-block;
        margin: 0.22rem 0.3rem 0.22rem 0;
        padding: 0.28rem 0.75rem;
        border-radius: 999px;
        background: rgba(99,102,241,0.1);
        border: 1px solid rgba(99,102,241,0.3);
        color: #a5b4fc;
        font-size: 0.8rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }
    .tag-know {
        display: inline-block;
        margin: 0.22rem 0.3rem 0.22rem 0;
        padding: 0.28rem 0.75rem;
        border-radius: 999px;
        background: rgba(20,184,166,0.1);
        border: 1px solid rgba(20,184,166,0.35);
        color: #2dd4bf;
        font-size: 0.8rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }
    .tag-learn {
        display: inline-block;
        margin: 0.22rem 0.3rem 0.22rem 0;
        padding: 0.28rem 0.75rem;
        border-radius: 999px;
        background: rgba(245,158,11,0.1);
        border: 1px solid rgba(245,158,11,0.35);
        color: #fbbf24;
        font-size: 0.8rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }

    /* ── Architecture map ── */
    .map-step {
        border-left: 4px solid #6366f1;
        padding: 0.65rem 0 0.65rem 1rem;
        margin: 0.35rem 0;
        background: rgba(99,102,241,0.06);
        border-radius: 0 14px 14px 0;
        color: #cbd5e1;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    .map-step:hover {
        background: rgba(99,102,241,0.12);
    }

    /* ── Resource links ── */
    .resource-card {
        background: rgba(22, 27, 39, 0.85);
        border: 1px solid rgba(99,102,241,0.15);
        border-radius: 16px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.6rem;
        transition: all 0.2s ease;
    }
    .resource-card:hover {
        border-color: rgba(99,102,241,0.4);
    }
    .resource-tip {
        background: rgba(20,184,166,0.08);
        border: 1px solid rgba(20,184,166,0.2);
        border-radius: 12px;
        padding: 0.65rem 0.9rem;
        color: #2dd4bf;
        font-size: 0.88rem;
        margin-top: 0.6rem;
    }

    /* ── Progress bars override ── */
    .stProgress > div > div > div {
        border-radius: 999px;
    }

    /* ── Bookmark badge ── */
    .bm-badge {
        display: inline-block;
        background: #6366f1;
        color: #fff;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 0.1rem 0.5rem;
        border-radius: 999px;
        margin-left: 0.4rem;
        vertical-align: middle;
        font-family: 'JetBrains Mono', monospace;
    }

    /* ── Effort section ── */
    .effort-label {
        font-size: 0.8rem;
        color: #94a3b8;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 0.15rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────
if "bookmarks" not in st.session_state:
    st.session_state["bookmarks"] = []
if "random_project" not in st.session_state:
    st.session_state["random_project"] = None
if "nav_page" not in st.session_state:
    st.session_state["nav_page"] = "Overview"

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
st.sidebar.title("🤖 Project Lab")

# Bookmark badge count
bm_count = len(st.session_state["bookmarks"])
bm_label = f"Saved Ideas {'✦' if bm_count > 0 else ''} ({bm_count})"

# Page radio — handle override (from "Random Project" button)
nav_options = ["Overview", "Idea Studio", "Project Explorer", bm_label]
if st.session_state["nav_page"].startswith("Saved Ideas"):
    st.session_state["nav_page"] = bm_label
elif st.session_state["nav_page"] not in nav_options:
    st.session_state["nav_page"] = "Overview"

page = st.sidebar.radio(
    "Navigate",
    nav_options,
    key="nav_page",
)

# PART 2 — Skill Gap widget
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 My Skills")
ALL_SKILLS = [
    "Python", "Pandas", "Scikit-learn", "TensorFlow", "PyTorch",
    "SQL", "Docker", "FastAPI", "Transformers", "OpenCV",
    "Matplotlib", "Seaborn", "AWS", "Git", "Streamlit",
]
user_skills = st.sidebar.multiselect("Select skills you already know", ALL_SKILLS)

st.sidebar.markdown("---")
all_domains = build_filter_options(dataset["domain"])
all_difficulties = build_filter_options(dataset["difficulty"])
all_datasets = build_filter_options(dataset["dataset"])

# ─────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-shell">
        <div class="hero-eyebrow">// ML-Based Project Idea Generator for Developers</div>
        <div class="hero-title">Turn one idea into a <span>full project plan</span>,<br>build map &amp; advanced implementation path.</div>
        <div class="hero-copy">
            AI-powered project blueprints, skill gap analysis, effort estimation, and rich learning resources
            — everything you need to build portfolio-ready ML projects.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────
# ── OVERVIEW PAGE ────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────
if page == "Overview":
    # Metrics
    metric_cols = st.columns(4)
    metrics = [
        ("Projects", len(dataset)),
        ("Domains", dataset["domain"].nunique()),
        ("Tech Stacks", dataset["technologies"].nunique()),
        ("Learning Topics", dataset["learning_topics"].nunique()),
    ]
    for col, (label, value) in zip(metric_cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="card">
                    <div class="metric-title">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("")

    # Chart row 1
    left, right = st.columns([1.05, 0.95])
    with left:
        st.markdown('<div class="section-title">Popular Domains</div>', unsafe_allow_html=True)
        fig = px.pie(
            dataset,
            names="domain",
            hole=0.56,
            color_discrete_sequence=["#6366f1", "#14b8a6", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"],
        )
        fig.update_layout(
            margin=dict(l=8, r=8, t=8, b=8),
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#cbd5e1",
            legend=dict(font=dict(color="#94a3b8")),
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown('<div class="section-title">Most Used Technologies</div>', unsafe_allow_html=True)
        tech_counts = dataset["technologies"].value_counts().reset_index()
        tech_counts.columns = ["technology", "count"]
        fig2 = px.bar(
            tech_counts.head(8),
            x="count",
            y="technology",
            orientation="h",
            color="count",
            color_continuous_scale=["#1e1b4b", "#6366f1"],
        )
        fig2.update_layout(
            margin=dict(l=8, r=8, t=8, b=8),
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#cbd5e1",
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

    # PART 8 — Chart 3: Difficulty Distribution
    st.markdown('<div class="section-title">Difficulty Distribution by Domain</div>', unsafe_allow_html=True)
    diff_df = (
        dataset.groupby(["domain", "difficulty"])
        .size()
        .reset_index(name="count")
    )
    fig3 = px.bar(
        diff_df,
        x="domain",
        y="count",
        color="difficulty",
        barmode="group",
        color_discrete_map={
            "Beginner": "#14b8a6",
            "Intermediate": "#f59e0b",
            "Advanced": "#ef4444",
        },
    )
    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#cbd5e1",
        legend=dict(font=dict(color="#94a3b8")),
        margin=dict(l=8, r=8, t=8, b=8),
        height=360,
    )
    st.plotly_chart(fig3, use_container_width=True)

    # PART 8 — Chart 4: Learning Topics Heatmap
    st.markdown('<div class="section-title">Domain × Topic Density</div>', unsafe_allow_html=True)
    heat_df = pd.crosstab(dataset["domain"], dataset["learning_topics"])
    fig4 = px.imshow(
        heat_df,
        color_continuous_scale="Blues",
        title="",
        aspect="auto",
    )
    fig4.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#cbd5e1",
        margin=dict(l=8, r=8, t=8, b=8),
        height=380,
    )
    st.plotly_chart(fig4, use_container_width=True)

    # PART 8 — Random Project Button
    st.markdown("")
    if st.button("🎲 Random Project → Idea Studio", use_container_width=True):
        rand_row = dataset.sample(1).iloc[0]
        st.session_state["random_project"] = rand_row.to_dict()
        st.session_state["nav_page"] = "Idea Studio"
        st.rerun()

    # Feature cards
    st.markdown('<div class="section-title">Why This Generator Helps</div>', unsafe_allow_html=True)
    cards = st.columns(3)
    content = [
        ("⚡ AI-Powered Advantages", "Claude AI writes 4 sharp, career-focused project advantages tailored to your exact project — not generic bullet points."),
        ("🗺️ Full Blueprint", "Each idea gets a complete build roadmap, architecture map, workflow, and implementation steps — not just a project name."),
        ("📊 Skill Gap + Effort", "See which skills you already have vs. what to learn, with direct resource links and a realistic time estimate."),
    ]
    for col, (title, text) in zip(cards, content):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="section-label">Feature</div>
                    <div class="section-title">{title}</div>
                    <div style="color:#94a3b8;font-size:0.92rem;">{text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ─────────────────────────────────────────────────────────────
# ── IDEA STUDIO PAGE ─────────────────────────────────────────
# ─────────────────────────────────────────────────────────────
elif page == "Idea Studio":
    st.markdown('<div class="section-title">💡 Idea Studio</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="mini-note">Describe your goal and the app will generate a project idea, full blueprint, and how to build it.</div>',
        unsafe_allow_html=True,
    )

    # Pre-fill from random project or suggestion click
    if "goal_prefill" not in st.session_state:
        st.session_state["goal_prefill"] = ""
    if st.session_state.get("random_project"):
        rp = st.session_state["random_project"]
        st.session_state["goal_prefill"] = rp.get("project_name", "")

    input_col, control_col = st.columns([1.25, 0.75])
    with input_col:
        user_goal = st.text_area(
            "What kind of project do you want?",
            value=st.session_state["goal_prefill"],
            placeholder="Start typing: fraud, chatbot, medical, agriculture, vision…",
            height=110,
            key="user_goal_area",
        )

        # ── Live Suggestions ──────────────────────────────────────────────
        typed = (user_goal or "").strip().lower()
        if typed and len(typed) >= 2:
            # Score each project by how many typed words appear in its name/description
            all_names = dataset["project_name"].tolist()
            all_descs = dataset["description"].tolist()
            scored = []
            for nm, desc in zip(all_names, all_descs):
                combined = (nm + " " + desc).lower()
                score = sum(w in combined for w in typed.split())
                if score > 0:
                    scored.append((nm, score))
            # Deduplicate names, sort by score desc
            seen = set()
            suggestions = []
            for nm, sc in sorted(scored, key=lambda x: -x[1]):
                if nm not in seen:
                    seen.add(nm)
                    suggestions.append(nm)
                    if len(suggestions) == 8:
                        break

            if suggestions:
                st.markdown(
                    '<div style="font-size:0.78rem;color:#6366f1;font-family:\'JetBrains Mono\',monospace;'
                    'margin-bottom:0.25rem;">💡 Live Suggestions — click to use</div>',
                    unsafe_allow_html=True,
                )
                chosen = st.selectbox(
                    "Suggestions",
                    ["— pick a suggestion —"] + suggestions,
                    label_visibility="collapsed",
                    key="live_suggestion_box",
                )
                if chosen and chosen != "— pick a suggestion —":
                    st.session_state["goal_prefill"] = chosen
                    st.rerun()
        else:
            # Show popular topics when nothing typed yet
            st.markdown(
                '<div style="font-size:0.78rem;color:#64748b;margin-top:0.3rem;">'
                '🔍 Try typing: <em>fraud, medical, chatbot, agriculture, vision, stock, recommendation…</em></div>',
                unsafe_allow_html=True,
            )

    with control_col:
        advanced_mode = st.toggle("⚡ Build advanced version", value=False)
        result_count = st.slider("Number of ideas", min_value=3, max_value=10, value=5)
        selected_domain = st.selectbox("Preferred domain", all_domains, key="idea_domain")
        selected_difficulty = st.selectbox(
            "Difficulty level",
            ["All", "Beginner", "Intermediate", "Advanced"]
            if not advanced_mode
            else ["All", "Advanced", "Intermediate", "Beginner"],
            key="idea_difficulty",
        )
        selected_dataset = st.selectbox("Dataset type", all_datasets, key="idea_dataset")

    # Clear random project after use
    if st.session_state.get("random_project") and user_goal:
        st.session_state["random_project"] = None
        st.session_state["goal_prefill"] = user_goal

    default_prompt = "machine learning portfolio project"
    results = recommend_projects(
        user_goal or default_prompt,
        top_n=result_count,
        domain=selected_domain,
        difficulty=selected_difficulty,
        dataset_name=selected_dataset,
        advanced_mode=advanced_mode,
    )

    if results.empty:
        st.warning("No projects matched those filters. Try choosing `All` for one of the filters.")
    else:
        top_project = results.iloc[0]
        blueprint = build_project_blueprint(
            top_project,
            user_goal or top_project["project_name"],
            advanced_mode=advanced_mode,
            show_spinner=True,
        )
        resource = get_resource(top_project["learning_topics"])

        # ── Header cards ──────────────────────────────────────
        header_left, header_right = st.columns([1.2, 0.8])
        with header_left:
            st.markdown(
                f"""
                <div class="card">
                    <div class="section-label">Best Matched Project</div>
                    <div class="section-title">{blueprint['idea_name']}</div>
                    <div style="color:#94a3b8;">{blueprint['problem']}</div>
                    <div style="margin-top:0.85rem;">
                        <span class="tag">{blueprint['difficulty']}</span>
                        <span class="tag">{top_project['domain']}</span>
                        <span class="tag">{blueprint['dataset_plan']}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with header_right:
            # Render rich learning direction card
            resource_title = resource["title"] if isinstance(resource, dict) else "Learning Direction"
            resource_summary = resource.get("summary", "") if isinstance(resource, dict) else resource
            difficulty_tip = ""
            if isinstance(resource, dict):
                difficulty_tip = resource.get("difficulty_tip", {}).get(
                    blueprint["difficulty"],
                    resource.get("difficulty_tip", {}).get("Intermediate", ""),
                )
            github_url = resource.get("github", "") if isinstance(resource, dict) else ""

            st.markdown(
                f"""
                <div class="card">
                    <div class="section-label">Learning Direction</div>
                    <div class="section-title">{resource_title}</div>
                    <div style="color:#94a3b8;font-size:0.9rem;">{resource_summary}</div>
                    <div class="resource-tip">💡 {difficulty_tip}</div>
                    <div style="margin-top:0.7rem;"><strong style="color:#6366f1;">Tech:</strong> <span style="color:#cbd5e1;">{blueprint['core_stack']}</span></div>
                    <div style="margin-top:0.35rem;"><strong style="color:#6366f1;">Match:</strong> <span style="color:#cbd5e1;">{top_project['score']:.2f}</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Resource links
            if isinstance(resource, dict):
                for lnk in resource.get("links", []):
                    st.link_button(f"📖 {lnk['label']}", lnk["url"])
            if github_url:
                st.link_button("⭐ GitHub Repo", github_url)

        # ── PART 2: Skill Gap Analyzer ───────────────────────
        if user_skills:
            st.markdown("---")
            st.markdown('<div class="section-title">🎯 Skill Gap Analysis</div>', unsafe_allow_html=True)
            project_stack = [s.strip() for s in " ".join(blueprint["stack_parts"]).split(",")]
            project_stack = blueprint["stack_parts"]

            know_col, learn_col = st.columns(2)
            known = [s for s in project_stack if any(u.lower() in s.lower() or s.lower() in u.lower() for u in user_skills)]
            to_learn = [s for s in project_stack if s not in known]

            with know_col:
                st.markdown('<div class="section-label">✅ Already Know</div>', unsafe_allow_html=True)
                if known:
                    tags = " ".join([f'<span class="tag-know">{s}</span>' for s in known])
                    st.markdown(tags, unsafe_allow_html=True)
                else:
                    st.markdown('<span style="color:#64748b;font-size:0.88rem;">None from this stack yet.</span>', unsafe_allow_html=True)

            with learn_col:
                st.markdown('<div class="section-label">📚 Need to Learn</div>', unsafe_allow_html=True)
                if to_learn:
                    for skill in to_learn:
                        link = SKILL_LINKS.get(skill, "")
                        if link:
                            st.markdown(
                                f'<span class="tag-learn">{skill}</span> <a href="{link}" target="_blank" style="color:#6366f1;font-size:0.8rem;">→ Learn</a>',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(f'<span class="tag-learn">{skill}</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span style="color:#14b8a6;font-size:0.88rem;">🎉 You know the full stack!</span>', unsafe_allow_html=True)

        # ── PART 3: Effort Estimator ─────────────────────────
        st.markdown("---")
        st.markdown('<div class="section-title">⏱️ Effort Estimator</div>', unsafe_allow_html=True)
        eff_col1, eff_col2, eff_col3, eff_col4 = st.columns([1, 1, 1, 1])
        with eff_col1:
            st.markdown(
                f"""
                <div class="card" style="text-align:center;">
                    <div class="metric-title">Estimated Time</div>
                    <div class="metric-value" style="font-size:1.5rem;">{blueprint['effort_weeks']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with eff_col2:
            st.markdown('<div class="effort-label">📦 Dataset Work</div>', unsafe_allow_html=True)
            st.progress(blueprint["effort_dataset"])
        with eff_col3:
            st.markdown('<div class="effort-label">🧠 Model Building</div>', unsafe_allow_html=True)
            st.progress(blueprint["effort_model"])
        with eff_col4:
            st.markdown('<div class="effort-label">🖥️ UI + Deployment</div>', unsafe_allow_html=True)
            st.progress(blueprint["effort_ui"])

        # ── Tabs ─────────────────────────────────────────────
        tab_adv, tab_work, tab_build, tab_map, tab_related = st.tabs(
            ["✨ Advantages", "⚙️ How It Works", "🛠️ How To Build", "🗺️ Project Map", "🔗 Related Ideas"]
        )

        with tab_adv:
            adv_left, adv_right = st.columns([1, 1])
            with adv_left:
                st.markdown("### ✨ Project Advantages")
                for item in blueprint["advantages"]:
                    st.markdown(f"- {item}")
            with adv_right:
                st.markdown("### 🧰 Recommended Stack")
                for item in blueprint["stack_parts"]:
                    st.markdown(f'<span class="tag">{item}</span>', unsafe_allow_html=True)
                if blueprint["advanced_addons"]:
                    st.markdown("### ⚡ Advanced Add-ons")
                    for item in blueprint["advanced_addons"]:
                        st.markdown(f"- {item}")

        with tab_work:
            st.markdown("### ⚙️ How This Project Works")
            for index, step in enumerate(blueprint["workflow"], start=1):
                st.markdown(f"**{index}.** {step}")

        with tab_build:
            build_left, build_right = st.columns(2)
            with build_left:
                st.markdown("### 🗓️ Build Roadmap")
                for index, step in enumerate(blueprint["milestones"], start=1):
                    st.markdown(f"**{index}.** {step}")
            with build_right:
                st.markdown("### 🛠️ Implementation Steps")
                for index, step in enumerate(blueprint["build_steps"], start=1):
                    st.markdown(f"**{index}.** {step}")

        with tab_map:
            st.markdown("### 🗺️ Project Architecture Map")
            for step in blueprint["architecture_map"]:
                st.markdown(f'<div class="map-step">{step}</div>', unsafe_allow_html=True)

        with tab_related:
            source_index = data[data["project_name"] == top_project["project_name"]].index
            if len(source_index) > 0:
                related = similar_projects(source_index[0]).head(4)
                for rel_idx, (_, item) in enumerate(related.iterrows()):
                    col_r, col_btn = st.columns([5, 1])
                    with col_r:
                        st.markdown(
                            f"""
                            <div class="project-card">
                                <strong style="color:#e2e8f0;">{item['project_name']}</strong><br>
                                <span class="tag">{item['domain']}</span>
                                <span class="tag">{item['difficulty']}</span>
                                <div style="margin-top:0.55rem;color:#94a3b8;">{item['description']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    with col_btn:
                        if st.button("⭐ Save", key=f"save_rel_{rel_idx}_{item['project_name']}"):
                            if item.to_dict() not in st.session_state["bookmarks"]:
                                st.session_state["bookmarks"].append(item.to_dict())
                                st.success("Saved!")

        # ── PART 4: Download Blueprint as Markdown ───────────
        st.markdown("---")
        adv_md = "\n".join([f"{i+1}. {a}" for i, a in enumerate(blueprint["advantages"])])
        wf_md = "\n".join([f"{i+1}. {s}" for i, s in enumerate(blueprint["workflow"])])
        ms_md = "\n".join([f"{i+1}. {s}" for i, s in enumerate(blueprint["milestones"])])
        bs_md = "\n".join([f"{i+1}. {s}" for i, s in enumerate(blueprint["build_steps"])])
        arch_md = "\n".join([f"- {s}" for s in blueprint["architecture_map"]])

        md_string = f"""# {blueprint['idea_name']}

## Problem Statement
{blueprint['problem']}

## Tech Stack
{blueprint['core_stack']}

## Advantages
{adv_md}

## How It Works
{wf_md}

## Build Roadmap
{ms_md}

## Implementation Steps
{bs_md}

## Architecture
{arch_md}

---
*Generated by ML Project Idea Generator*
"""
        col_dl, col_bm = st.columns([1, 1])
        with col_dl:
            st.download_button(
                "📥 Download Blueprint (.md)",
                data=md_string,
                file_name=f"{blueprint['idea_name'].replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with col_bm:
            if st.button("⭐ Save Top Idea to Bookmarks", use_container_width=True):
                row_dict = top_project.to_dict()
                if row_dict not in st.session_state["bookmarks"]:
                    st.session_state["bookmarks"].append(row_dict)
                    st.success("Saved to bookmarks!")
                else:
                    st.info("Already in bookmarks.")

        # ── Generated Ideas List ─────────────────────────────
        st.markdown('<div class="section-title" style="margin-top:1.5rem;">Generated Project Ideas</div>', unsafe_allow_html=True)
        for idx, row in results.iterrows():
            card_col, btn_col = st.columns([6, 1])
            with card_col:
                st.markdown(
                    f"""
                    <div class="project-card">
                        <div class="section-label">Idea {idx + 1}</div>
                        <div class="section-title">{row['project_name']}</div>
                        <div style="color:#94a3b8;">{row['description']}</div>
                        <div style="margin-top:0.75rem;">
                            <span class="tag">{row['domain']}</span>
                            <span class="tag">{row['difficulty']}</span>
                            <span class="tag">{row['dataset']}</span>
                        </div>
                        <div style="margin-top:0.65rem;color:#64748b;font-size:0.88rem;">
                            <strong style="color:#6366f1;">Technologies:</strong> {row['technologies']}<br>
                            <strong style="color:#6366f1;">Learning topic:</strong> {row['learning_topics']}<br>
                            <strong style="color:#6366f1;">Match score:</strong> {row['score']:.2f}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with btn_col:
                if st.button("⭐ Save", key=f"save_idea_{idx}_{row['project_name']}"):
                    row_dict = row.to_dict()
                    if row_dict not in st.session_state["bookmarks"]:
                        st.session_state["bookmarks"].append(row_dict)
                        st.success("Saved!")
                    else:
                        st.info("Already saved.")

# ─────────────────────────────────────────────────────────────
# ── PROJECT EXPLORER PAGE ────────────────────────────────────
# ─────────────────────────────────────────────────────────────
elif page == "Project Explorer":
    st.markdown('<div class="section-title">🔍 Project Explorer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="mini-note">Browse all project ideas directly with filters before choosing one.</div>',
        unsafe_allow_html=True,
    )

    # Build keyword options from project names + learning topics
    keyword_options = ["All"] + sorted(
        set(dataset["project_name"].dropna().tolist())
        | set(dataset["learning_topics"].dropna().unique().tolist())
    )

    filter_cols = st.columns(4)
    explorer_domain = filter_cols[0].selectbox("Domain filter", all_domains, key="explorer_domain")
    explorer_difficulty = filter_cols[1].selectbox("Difficulty filter", all_difficulties, key="explorer_difficulty")
    explorer_dataset = filter_cols[2].selectbox("Dataset filter", all_datasets, key="explorer_dataset")
    search_term = filter_cols[3].selectbox("Keyword", keyword_options, key="explorer_keyword")

    filtered_data = dataset.copy()
    if explorer_domain != "All":
        filtered_data = filtered_data[filtered_data["domain"] == explorer_domain]
    if explorer_difficulty != "All":
        filtered_data = filtered_data[filtered_data["difficulty"] == explorer_difficulty]
    if explorer_dataset != "All":
        filtered_data = filtered_data[filtered_data["dataset"] == explorer_dataset]
    if search_term != "All":
        mask = filtered_data.apply(
            lambda row: search_term.lower() in " ".join(row.astype(str)).lower(), axis=1
        )
        filtered_data = filtered_data[mask]

    st.caption(f"Showing {len(filtered_data)} projects")
    st.dataframe(
        filtered_data[["project_name", "domain", "technologies", "difficulty", "dataset", "learning_topics"]],
        use_container_width=True,
        hide_index=True,
    )

# ─────────────────────────────────────────────────────────────
# ── PART 5: SAVED IDEAS PAGE ─────────────────────────────────
# ─────────────────────────────────────────────────────────────
else:
    bm_page_title = "⭐ Saved Ideas"
    st.markdown(f'<div class="section-title">{bm_page_title}</div>', unsafe_allow_html=True)

    bookmarks = st.session_state["bookmarks"]
    if not bookmarks:
        st.info("No saved ideas yet. Hit the ⭐ Save button next to any project in Idea Studio.")
    else:
        bm_df = pd.DataFrame(bookmarks)
        display_cols = [c for c in ["project_name", "domain", "difficulty", "technologies", "learning_topics"] if c in bm_df.columns]
        st.markdown(f"**{len(bookmarks)} saved project(s)**")

        # Show dataframe with selection
        st.dataframe(bm_df[display_cols], use_container_width=True, hide_index=True)

        # Compare two selected
        st.markdown("---")
        st.markdown("### 🆚 Compare Two Ideas")
        names = [b.get("project_name", f"Project {i}") for i, b in enumerate(bookmarks)]
        col_sel1, col_sel2 = st.columns(2)
        sel1 = col_sel1.selectbox("Pick idea A", names, key="cmp_a")
        sel2 = col_sel2.selectbox("Pick idea B", names, key="cmp_b", index=min(1, len(names) - 1))

        if st.button("🔍 Compare Selected", use_container_width=True) and sel1 and sel2:
            row_a = next((b for b in bookmarks if b.get("project_name") == sel1), None)
            row_b = next((b for b in bookmarks if b.get("project_name") == sel2), None)

            if row_a and row_b:
                compare_cols = st.columns(2)
                for i, (col, row) in enumerate(zip(compare_cols, [row_a, row_b])):
                    with col:
                        proj_series = pd.Series(row)
                        bp = build_project_blueprint(proj_series, proj_series.get("project_name", ""), advanced_mode=False, show_spinner=False)
                        st.markdown(
                            f"""
                            <div class="card">
                                <div class="section-label">{'Idea A' if i == 0 else 'Idea B'}</div>
                                <div class="section-title">{bp['idea_name']}</div>
                                <div style="color:#94a3b8;font-size:0.88rem;">{bp['problem']}</div>
                                <div style="margin-top:0.7rem;">
                                    <span class="tag">{bp['difficulty']}</span>
                                    <span class="tag">{row.get('domain','')}</span>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        st.markdown("**Advantages:**")
                        for adv in bp["advantages"]:
                            st.markdown(f"- {adv}")
                        st.markdown("**Stack:**")
                        tags = " ".join([f'<span class="tag">{s}</span>' for s in bp["stack_parts"]])
                        st.markdown(tags, unsafe_allow_html=True)
                        st.markdown(f"**Estimated Time:** {bp['effort_weeks']}")

        st.markdown("---")
        if st.button("🗑️ Clear All Saved Ideas", use_container_width=True):
            st.session_state["bookmarks"] = []
            st.success("All bookmarks cleared.")
            st.rerun()
