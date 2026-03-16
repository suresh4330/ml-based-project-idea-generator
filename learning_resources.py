
# ─────────────────────────────────────────────────────────────
# PART 7 — Enriched Learning Resources
# ─────────────────────────────────────────────────────────────

RESOURCES = {
    "NLP": {
        "title": "Natural Language Processing",
        "summary": "Master text processing, transformers, and language models for real-world NLP tasks.",
        "links": [
            {"label": "HuggingFace NLP Course", "url": "https://huggingface.co/learn/nlp-course"},
            {"label": "Stanford CS224N", "url": "https://web.stanford.edu/class/cs224n/"},
            {"label": "FastAI NLP", "url": "https://www.fast.ai/"},
        ],
        "github": "https://github.com/huggingface/transformers",
        "difficulty_tip": {
            "Beginner": "Start with spaCy basics and simple text classification.",
            "Intermediate": "Fine-tune BERT on your specific task with HuggingFace Trainer.",
            "Advanced": "Build custom transformer architectures and train on domain-specific corpora.",
        },
    },
    "Computer Vision": {
        "title": "Computer Vision",
        "summary": "Build image understanding systems with CNNs, object detection, and segmentation.",
        "links": [
            {"label": "PyTorch Vision Tutorials", "url": "https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html"},
            {"label": "OpenCV Documentation", "url": "https://docs.opencv.org/"},
            {"label": "FastAI Vision", "url": "https://docs.fast.ai/tutorial.vision.html"},
        ],
        "github": "https://github.com/ultralytics/ultralytics",
        "difficulty_tip": {
            "Beginner": "Start with image classification using a pre-trained ResNet model.",
            "Intermediate": "Implement object detection using YOLOv8 on a custom dataset.",
            "Advanced": "Build end-to-end real-time video analysis pipelines with model optimization.",
        },
    },
    "Deep Learning": {
        "title": "Deep Learning",
        "summary": "Design neural networks that solve complex vision, language, and tabular problems.",
        "links": [
            {"label": "Deep Learning Specialization (Coursera)", "url": "https://www.coursera.org/specializations/deep-learning"},
            {"label": "PyTorch Docs", "url": "https://pytorch.org/docs/stable/index.html"},
            {"label": "fast.ai Practical DL", "url": "https://course.fast.ai/"},
        ],
        "github": "https://github.com/pytorch/pytorch",
        "difficulty_tip": {
            "Beginner": "Learn feedforward networks and backpropagation with PyTorch basics.",
            "Intermediate": "Train CNNs and RNNs with custom loss functions and callbacks.",
            "Advanced": "Implement attention mechanisms, custom training loops, and distributed training.",
        },
    },
    "Regression": {
        "title": "Regression Modeling",
        "summary": "Predict continuous outcomes using statistical and ML regression techniques.",
        "links": [
            {"label": "Scikit-learn User Guide", "url": "https://scikit-learn.org/stable/supervised_learning.html"},
            {"label": "StatQuest Regression Series", "url": "https://statquest.org/"},
            {"label": "Kaggle Regression Tutorials", "url": "https://www.kaggle.com/learn/intermediate-machine-learning"},
        ],
        "github": "https://github.com/scikit-learn/scikit-learn",
        "difficulty_tip": {
            "Beginner": "Start with Linear Regression and understand bias-variance tradeoff.",
            "Intermediate": "Apply Ridge, Lasso, and ElasticNet with hyperparameter tuning.",
            "Advanced": "Stack regressors and do feature engineering with automated pipelines.",
        },
    },
    "Classification": {
        "title": "Classification",
        "summary": "Build models that classify data into categories for diagnosis, fraud, sentiment, and more.",
        "links": [
            {"label": "Scikit-learn Classification", "url": "https://scikit-learn.org/stable/supervised_learning.html#supervised-learning"},
            {"label": "Google ML Crash Course", "url": "https://developers.google.com/machine-learning/crash-course"},
            {"label": "Kaggle Learn", "url": "https://www.kaggle.com/learn"},
        ],
        "github": "https://github.com/scikit-learn/scikit-learn",
        "difficulty_tip": {
            "Beginner": "Use Decision Trees and Logistic Regression, understand confusion matrices.",
            "Intermediate": "Implement Random Forest and XGBoost with cross-validation.",
            "Advanced": "Build ensemble stacking pipelines with SHAP explainability.",
        },
    },
    "Recommendation Systems": {
        "title": "Recommendation Systems",
        "summary": "Design collaborative, content-based, or hybrid recommenders like Netflix and Spotify.",
        "links": [
            {"label": "Google RecSys Course", "url": "https://developers.google.com/machine-learning/recommendation"},
            {"label": "Surprise Library", "url": "https://surpriselib.com/"},
            {"label": "LightFM Docs", "url": "https://making.lyst.com/lightfm/docs/home.html"},
        ],
        "github": "https://github.com/NicolasHug/Surprise",
        "difficulty_tip": {
            "Beginner": "Build a simple movie recommender with cosine similarity on ratings.",
            "Intermediate": "Implement matrix factorization (SVD) with Surprise library.",
            "Advanced": "Deploy a real-time hybrid recommender with user embeddings and A/B testing.",
        },
    },
    "Time Series": {
        "title": "Time Series Analysis",
        "summary": "Forecast future values in financial, IoT, and business data using temporal models.",
        "links": [
            {"label": "Prophet by Meta", "url": "https://facebook.github.io/prophet/"},
            {"label": "Nixtla (NeuralForecast)", "url": "https://docs.nixtla.io/"},
            {"label": "Time Series with Python (O'Reilly)", "url": "https://www.oreilly.com/library/view/time-series-analysis/9781492041672/"},
        ],
        "github": "https://github.com/Nixtla/neuralforecast",
        "difficulty_tip": {
            "Beginner": "Use Prophet for trend and seasonality decomposition.",
            "Intermediate": "Implement ARIMA and LSTM-based forecasting with rolling windows.",
            "Advanced": "Build multi-step probabilistic forecasting with NeuralForecast transformers.",
        },
    },
    "Reinforcement Learning": {
        "title": "Reinforcement Learning",
        "summary": "Train agents that learn by interacting with environments — from games to robotics.",
        "links": [
            {"label": "OpenAI Spinning Up", "url": "https://spinningup.openai.com/en/latest/"},
            {"label": "Stable Baselines3", "url": "https://stable-baselines3.readthedocs.io/"},
            {"label": "HuggingFace RL Course", "url": "https://huggingface.co/learn/deep-rl-course"},
        ],
        "github": "https://github.com/DLR-RM/stable-baselines3",
        "difficulty_tip": {
            "Beginner": "Implement Q-learning on CartPole with OpenAI Gym.",
            "Intermediate": "Train PPO agents using Stable Baselines3 on custom environments.",
            "Advanced": "Build multi-agent systems with custom reward shaping and policy distillation.",
        },
    },
}

# ─────────────────────────────────────────────────────────────
# PART 2 — Skill Links for Skill Gap Analyzer
# ─────────────────────────────────────────────────────────────
SKILL_LINKS = {
    "Python": "https://docs.python.org/3/tutorial/",
    "Pandas": "https://pandas.pydata.org/docs/getting_started/",
    "Scikit-learn": "https://scikit-learn.org/stable/getting_started.html",
    "TensorFlow": "https://tensorflow.org/tutorials",
    "PyTorch": "https://pytorch.org/tutorials/beginner/basics/intro.html",
    "SQL": "https://mode.com/sql-tutorial/",
    "Docker": "https://docs.docker.com/get-started/",
    "FastAPI": "https://fastapi.tiangolo.com/tutorial/",
    "Transformers": "https://huggingface.co/docs/transformers/index",
    "OpenCV": "https://docs.opencv.org/4.x/d9/df8/tutorial_root.html",
    "Matplotlib": "https://matplotlib.org/stable/tutorials/index.html",
    "Seaborn": "https://seaborn.pydata.org/tutorial.html",
    "AWS": "https://aws.amazon.com/getting-started/",
    "Git": "https://git-scm.com/book/en/v2",
    "Streamlit": "https://docs.streamlit.io/",
}

# Legacy compat
resources = {k: v["title"] for k, v in RESOURCES.items()}


def get_resource(topic):
    """Return full resource dict or a plain string fallback."""
    for key in RESOURCES:
        if key.lower() in topic.lower():
            return RESOURCES[key]
    return {
        "title": "Machine Learning Foundations",
        "summary": "Build a solid base across supervised, unsupervised, and deep learning concepts.",
        "links": [
            {"label": "Google ML Crash Course", "url": "https://developers.google.com/machine-learning/crash-course"},
            {"label": "fast.ai", "url": "https://www.fast.ai/"},
        ],
        "github": "https://github.com/scikit-learn/scikit-learn",
        "difficulty_tip": {
            "Beginner": "Start with the Google ML Crash Course to grasp core concepts.",
            "Intermediate": "Work through fast.ai Practical Deep Learning for real-world projects.",
            "Advanced": "Deep-dive into original research papers and reimplement key architectures.",
        },
    }