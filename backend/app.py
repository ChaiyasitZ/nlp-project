from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
import os
import traceback
import json
from urllib.parse import quote_plus
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from config import config
from services.news_scraper import NewsScraper
from services.nlp_processor import NLPProcessor
from services.timeline_generator import TimelineGenerator
from services.similarity_analyzer import SimilarityAnalyzer


class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for MongoDB ObjectId and datetime"""
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Configure Flask JSON settings for modern Flask versions
    app.json.compact = False
    
    # Configure CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Initialize MongoDB Atlas connection
    mongo = None
    try:
        mongo_uri = app.config['MONGO_URI']
        
        # Use MongoDB Atlas recommended connection method with ServerApi
        client = MongoClient(mongo_uri, server_api=ServerApi('1'))
        
        # Test the connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        
        # Initialize PyMongo with the client
        app.config['MONGO_URI'] = mongo_uri
        mongo = PyMongo(app)
        
        # Get database name from URI or use default
        db_name = "newstimelineai"
        print(f"📁 Using database: {db_name}")
        
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB Atlas: {str(e)}")
        print("Please check your MONGO_URI in the .env file")
        print("Make sure your connection string includes the correct password")
        # Don't raise the exception during development - allow the app to start
        mongo = None
    
    # Initialize services
    news_scraper = NewsScraper()
    nlp_processor = NLPProcessor()
    timeline_generator = TimelineGenerator()
    similarity_analyzer = SimilarityAnalyzer()
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        try:
            # Test database connection
            if mongo and mongo.cx:
                mongo.cx.admin.command('ping')
                db_status = "connected"
            else:
                db_status = "not connected"
        except Exception as e:
            db_status = f"error: {str(e)}"
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'database': db_status,
            'version': '1.0.0'
        })
    
    @app.route('/api/analyze-news', methods=['POST'])
    def analyze_news():
        """Analyze news articles and generate timeline"""
        try:
            # Check if MongoDB is available
            if not mongo:
                return jsonify({'error': 'Database not available'}), 503
                
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            input_type = data.get('input_type', 'url')
            urls = data.get('urls', [])
            
            if input_type == 'url' and not urls:
                return jsonify({'error': 'No URLs provided'}), 400
            
            # Scrape articles
            articles = []
            for url in urls:
                try:
                    article_data = news_scraper.scrape_article(url)
                    if article_data:
                        articles.append(article_data)
                except Exception as e:
                    print(f"Error scraping {url}: {str(e)}")
                    continue
            
            if not articles:
                return jsonify({'error': 'No articles could be processed'}), 400
            
            # Process articles with NLP
            processed_articles = []
            for article in articles:
                processed = nlp_processor.process_article(article)
                processed_articles.append(processed)
            
            # Generate timeline
            timeline_data = timeline_generator.generate_timeline(processed_articles)
            
            # Store in database
            analysis_doc = {
                'articles': processed_articles,
                'timeline': timeline_data,
                'created_at': datetime.utcnow(),
                'input_type': input_type,
                'urls': urls
            }
            analysis_id = str(mongo.db.analyses.insert_one(analysis_doc).inserted_id)
            
            return jsonify({
                'analysis_id': analysis_id,
                'articles': processed_articles,
                'timeline': timeline_data,
                'status': 'success'
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/compare-articles', methods=['POST'])
    def compare_articles():
        """Compare two articles for similarity"""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            article1_id = data.get('article1_id')
            article2_id = data.get('article2_id')
            
            if not article1_id or not article2_id:
                return jsonify({'error': 'Both article IDs are required'}), 400
            
            # Get articles from database
            article1 = mongo.db.articles.find_one({'_id': article1_id})
            article2 = mongo.db.articles.find_one({'_id': article2_id})
            
            if not article1 or not article2:
                return jsonify({'error': 'One or both articles not found'}), 404
            
            # Perform similarity analysis
            similarity_result = similarity_analyzer.compare_articles(article1, article2)
            
            # Store comparison result
            comparison_id = str(mongo.db.comparisons.insert_one({
                'article1_id': article1_id,
                'article2_id': article2_id,
                'similarity_result': similarity_result,
                'created_at': datetime.utcnow()
            }).inserted_id)
            
            return jsonify({
                'comparison_id': comparison_id,
                'similarity_result': similarity_result,
                'status': 'success'
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/timeline/<analysis_id>', methods=['GET'])
    def get_timeline(analysis_id):
        """Get timeline data for a specific analysis"""
        try:
            from bson import ObjectId
            analysis = mongo.db.analyses.find_one({'_id': ObjectId(analysis_id)})
            
            if not analysis:
                return jsonify({'error': 'Analysis not found'}), 404
            
            return jsonify({
                'timeline': analysis.get('timeline'),
                'articles': analysis.get('articles'),
                'created_at': analysis.get('created_at').isoformat() if analysis.get('created_at') else None
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/similarity/<comparison_id>', methods=['GET'])
    def get_similarity(comparison_id):
        """Get similarity analysis for a specific comparison"""
        try:
            from bson import ObjectId
            comparison = mongo.db.comparisons.find_one({'_id': ObjectId(comparison_id)})
            
            if not comparison:
                return jsonify({'error': 'Comparison not found'}), 404
            
            return jsonify({
                'similarity_result': comparison.get('similarity_result'),
                'created_at': comparison.get('created_at').isoformat() if comparison.get('created_at') else None
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/articles', methods=['GET'])
    def get_articles():
        """Get list of all processed articles"""
        try:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))
            
            articles = list(mongo.db.articles.find()
                          .skip((page - 1) * per_page)
                          .limit(per_page))
            
            # Convert ObjectId to string for JSON serialization
            for article in articles:
                article['_id'] = str(article['_id'])
            
            total_count = mongo.db.articles.count_documents({})
            
            return jsonify({
                'articles': articles,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total_count,
                    'pages': (total_count + per_page - 1) // per_page
                }
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
