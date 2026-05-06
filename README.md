# ML-Based Project Idea Generator for Developers

---

![status](https://img.shields.io/badge/status-active-success) ![backend](https://img.shields.io/badge/backend-Python_3-blue) ![frontend](https://img.shields.io/badge/frontend-Streamlit_1.40-FF4B4B) ![recommendation](https://img.shields.io/badge/recommendation-TF--IDF_Similarity-8A2BE2) ![AI](https://img.shields.io/badge/AI-Anthropic_API-orange)

**ML-Based Project Idea Generator** is an interactive platform that recommends tailored machine learning project ideas based on user interests, project domain, difficulty level, and dataset type. It combines TF-IDF similarity for local recommendations with cloud LLMs (Anthropic API) to generate detailed project blueprints and advantages. Produces actionable learning resource suggestions, similar project lookups, and interactive visual insights using Plotly.
## Features

- Project recommendations using TF-IDF similarity
- Filters for domain, difficulty, and dataset type
- Project blueprint generation
- Learning resource suggestions
- Similar project lookup
- Interactive charts with Plotly
- Optional AI-generated project advantages using Anthropic

## Tech Stack

- Python
- Streamlit
- Pandas
- scikit-learn
- Plotly
- python-dotenv
- Anthropic API (optional)

## Project Structure

```text
idea_generator/
|-- app.py
|-- recommender.py
|-- learning_resources.py
|-- similarity.py
|-- dataset.csv
|-- generate_large_dataset.py
|-- requirements.txt
|-- .gitignore
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/suresh4330/ml-based-project-idea-generator.git
cd ml-based-project-idea-generator
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project folder if you want to enable Anthropic-powered AI advantages:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

This step is optional. The app still works without the API key by using static fallback content.

## Run the App

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Use Cases

- Find ML project ideas for a portfolio
- Explore projects by skill level
- Discover learning topics and useful resources
- Build stronger end-to-end ML project plans

## Notes

- `.env` is excluded from Git for safety.
- `__pycache__` and `.pyc` files are ignored.
- The dataset is stored locally in `dataset.csv`.

## License

This project is available for personal and educational use.
