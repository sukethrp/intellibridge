# IntelliBridge: Human-AI Expert Matching System

IntelliBridge is an intelligent system that matches human experts with AI agents based on skills, knowledge areas, and complementarity. It uses advanced NLP techniques to process both structured and unstructured data to create optimal human-AI teams.

## 🎯 Features

- **Intelligent Matching**: Uses semantic similarity and complementarity metrics to match humans with AI agents
- **NLP Processing**: Extracts skills and knowledge areas from unstructured text using spaCy
- **Semantic Understanding**: Leverages Sentence-BERT for deep semantic matching
- **Interactive UI**: Streamlit-based interface for easy interaction
- **Explainable Matches**: Provides detailed reasoning for each match
- **Customizable Weights**: Adjust matching priorities based on different criteria

## 🛠️ Tech Stack

- Python 3.8+
- spaCy for NLP processing
- Sentence-BERT for semantic embeddings
- Streamlit for the web interface
- scikit-learn for similarity calculations
- Plotly for visualizations

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/intellibridge.git
cd intellibridge
```

2. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. Run the application:
```bash
streamlit run main.py
```

## 📁 Project Structure

```
intellibridge/
├── extractor.py      # NLP skill extraction
├── matcher.py        # Matching logic and scoring
├── main.py          # Streamlit interface
├── utils.py         # Helper functions
├── requirements.txt # Dependencies
└── README.md        # Documentation
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details. 