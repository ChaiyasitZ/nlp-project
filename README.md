# NewsTimelineAI

**Automatic News Timeline and Similarity Analysis**

A web application that automatically collects news from multiple sources, extracts key events, entities, and locations, generates timelines, and analyzes content similarity and differences between news sources.

## 🎯 Features

### Core Features
- **News Ingestion**: Scrape news articles from multiple sources via URLs
- **NLP-based Event Extraction**: Named Entity Recognition (NER) for extracting people, places, organizations
- **Timeline Generation**: Automatic chronological timeline with interactive visualization
- **Similarity Analysis**: Semantic similarity analysis using Sentence-BERT/Transformer models
- **Comparison View**: Side-by-side article comparison with highlighted differences
- **Time-based Analysis**: Filter and analyze news by date ranges

### Technical Features
- **Multi-language Support**: Thai and English language processing
- **Interactive Charts**: Timeline visualization with Chart.js
- **Responsive Design**: Modern UI with Tailwind CSS
- **RESTful API**: Flask backend with MongoDB storage

## 🏗️ Architecture

```
nlp-project/
├── frontend/          # React + Vite frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── NewsInput.jsx
│   │   │   ├── Timeline.jsx
│   │   │   ├── Comparison.jsx
│   │   │   └── SimilarityAnalysis.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
├── backend/           # Flask backend
│   ├── services/
│   │   ├── news_scraper.py
│   │   ├── nlp_processor.py
│   │   ├── timeline_generator.py
│   │   └── similarity_analyzer.py
│   ├── app.py
│   ├── config.py
│   └── requirements.txt
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- MongoDB Atlas account (free tier available)

### Database Setup
1. **Create MongoDB Atlas Account**: 
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create a free account and cluster

2. **Configure Database Connection**:
   ```bash
   cd backend
   copy .env.example .env  # Windows
   # cp .env.example .env  # macOS/Linux
   ```
   
3. **Update `.env` file** with your Atlas connection string:
   ```env
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/newstimelineai?retryWrites=true&w=majority
   ```

### Database Setup
1. **Create MongoDB Atlas Account**: 
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create a free account and cluster
   - See detailed instructions in `MONGODB_ATLAS_SETUP.md`

2. **Configure Database Connection**:
   ```bash
   cd backend
   copy .env.example .env  # Windows
   # cp .env.example .env  # macOS/Linux
   ```
   
3. **Update `.env` file** with your Atlas connection string:
   ```env
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/newstimelineai?retryWrites=true&w=majority
   ```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:5173`

### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment (see Database Setup above)
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux

# Update .env with your MongoDB Atlas connection string

# Start the server
python app.py
```
The backend API will be available at `http://localhost:5000`

### Quick Start with Scripts
```bash
# Windows
./start-dev.bat

# macOS/Linux
chmod +x start-dev.sh
./start-dev.sh
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/analyze-news` | Analyze news articles and generate timeline |
| POST | `/api/compare-articles` | Compare two articles for similarity |
| GET | `/api/timeline/<analysis_id>` | Get timeline data |
| GET | `/api/similarity/<comparison_id>` | Get similarity analysis |
| GET | `/api/articles` | Get list of processed articles |

## 💻 Usage

1. **Input News**: Enter URLs of news articles or select a date range
2. **View Timeline**: See chronological events with interactive charts
3. **Compare Articles**: Select articles to compare content and perspectives
4. **Analyze Similarity**: View detailed similarity scores and differences

## 🔧 Tech Stack

### Frontend
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS
- **Charts**: Chart.js with react-chartjs-2
- **Icons**: Lucide React
- **HTTP Client**: Axios

### Backend
- **Framework**: Flask 3.0
- **Database**: MongoDB with PyMongo
- **NLP**: PyThaiNLP, scikit-learn
- **Web Scraping**: BeautifulSoup4, Requests
- **ML**: Sentence-Transformers, scikit-learn

### NLP Tools
- **Thai Processing**: PyThaiNLP (tokenization, POS tagging)
- **Entity Recognition**: Regex + Dictionary-based NER
- **Similarity**: TF-IDF, Cosine Similarity
- **Date Extraction**: dateparser

## 🎯 Success Metrics

- **Accuracy**: NER and Similarity ≥80% (human evaluation)
- **Performance**: Process 10-20 articles within <10 seconds
- **User Engagement**: Timeline views and comparison usage

## 🔮 Future Enhancements

- [ ] Real-time news feeds
- [ ] Sentiment analysis
- [ ] Multi-language support expansion
- [ ] Export to PDF/CSV
- [ ] Advanced ML models (BERT, GPT)
- [ ] Social media integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- PyThaiNLP team for Thai language processing
- Chart.js for interactive visualizations
- Tailwind CSS for modern styling
- The open-source community

---

**Built with ❤️ for better news understanding**