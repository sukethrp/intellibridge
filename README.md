# IntelliBridge: Human-AI Expert Matching System

IntelliBridge is an intelligent system that matches human experts with AI agents based on skills, knowledge areas, and complementarity. It uses advanced NLP techniques (regex and keyword extraction) to process both structured and unstructured data to create optimal human-AI teams.

## 🎯 Features

- **Intelligent Matching**: Uses semantic similarity and complementarity metrics to match humans with AI agents
- **NLP Processing**: Extracts skills and knowledge areas from unstructured text using regex and keyword matching (no heavy NLP dependencies)
- **Semantic Understanding**: Leverages Sentence-BERT for deep semantic matching
- **Interactive UI**: Streamlit-based interface for easy interaction
- **Explainable Matches**: Provides detailed reasoning for each match
- **Customizable Weights**: Adjust matching priorities based on different criteria
- **Feedback Loop**: Rate matches and clear feedback to improve recommendations
- **Sample Data Loader**: Instantly populate the app with example profiles for demo/testing

## 🛠️ Tech Stack

- Python 3.10+ (pinned for Streamlit Cloud compatibility)
- Streamlit >= 1.10.0 (recommended: 1.32.0)
- sentence-transformers for semantic embeddings
- scikit-learn, numpy, pandas for data processing
- plotly for visualizations

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/intellibridge.git
cd intellibridge
```

2. (Recommended) Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Ensure Streamlit is up to date:**
```bash
pip install --upgrade streamlit
```

5. Run the application:
```bash
streamlit run main.py
```

6. **Using the App:**
   - Go to [http://localhost:8501](http://localhost:8501) in your browser.
   - Click **"Load Sample Data"** to instantly populate the app with example human and AI profiles.
   - Adjust matching preferences, view matches, and provide feedback.
   - Use the **"Clear All Feedback"** button in the Feedback & Analytics tab to reset feedback data.

## 📁 Project Structure

```
intellibridge/
├── extractor.py      # NLP skill extraction (regex/keywords)
├── matcher.py        # Matching logic and scoring
├── main.py           # Streamlit interface
├── sample_data.json  # Example profiles for demo/testing
├── requirements.txt  # Dependencies
├── runtime.txt       # Python version pin for Streamlit Cloud
└── README.md         # Documentation
```

## ☁️ Deploying on Streamlit Cloud

1. Push your project to a public GitHub repository.
2. Go to [https://share.streamlit.io/](https://share.streamlit.io/).
3. Select your repo, branch (`main`), and main file (`main.py`).
4. Deploy and share your app with the world!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details. 