# NewsTimelineAI Backend

Flask backend for automatic news timeline generation and similarity analysis.

## Features

- News article ingestion from URLs
- NLP-based event extraction
- Timeline generation
- Semantic similarity analysis
- Entity recognition and keyword extraction

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure MongoDB connection in config.py

3. Run the application:
```bash
python app.py
```

## API Endpoints

- `POST /api/analyze-news` - Analyze news articles
- `POST /api/compare-articles` - Compare multiple articles
- `GET /api/timeline/<analysis_id>` - Get timeline data
- `GET /api/similarity/<comparison_id>` - Get similarity analysis

## Dependencies

- Flask
- MongoDB
- PyThaiNLP
- scikit-learn
- beautifulsoup4
- requests
