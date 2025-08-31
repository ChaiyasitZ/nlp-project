from typing import List, Dict, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict, Counter
import re
from datetime import datetime


class SimilarityAnalyzer:
    """Analyze similarity between news articles"""
    
    def __init__(self):
        self.similarity_threshold = 0.3
        self.sentiment_keywords = {
            'positive': {
                'th': ['ดี', 'สำเร็จ', 'ประสบผลสำเร็จ', 'ก้าวหน้า', 'พัฒนา', 'เจริญ', 'ยินดี', 'ชื่นชม'],
                'en': ['good', 'great', 'excellent', 'successful', 'positive', 'progress', 'development', 'achievement']
            },
            'negative': {
                'th': ['แย่', 'ล้มเหลว', 'เสียหาย', 'วิกฤต', 'ปัญหา', 'อันตราย', 'เสียใจ', 'โกรธ'],
                'en': ['bad', 'terrible', 'failed', 'crisis', 'problem', 'danger', 'sad', 'angry', 'negative']
            },
            'neutral': {
                'th': ['ปกติ', 'ธรรมดา', 'เฉยๆ', 'คงที่'],
                'en': ['normal', 'ordinary', 'neutral', 'stable', 'unchanged']
            }
        }
    
    def compare_articles(self, article1: Dict[str, Any], article2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare two articles for similarity and differences
        
        Args:
            article1 (dict): First article data
            article2 (dict): Second article data
            
        Returns:
            dict: Comparison results including similarity scores and differences
        """
        # Calculate content similarity
        content_similarity = self._calculate_content_similarity(
            article1.get('content', ''),
            article2.get('content', ''),
            article1.get('language', 'th')
        )
        
        # Compare entities
        entity_comparison = self._compare_entities(
            article1.get('entities', {}),
            article2.get('entities', {})
        )
        
        # Compare keywords
        keyword_comparison = self._compare_keywords(
            article1.get('keywords', []),
            article2.get('keywords', [])
        )
        
        # Analyze sentiment
        sentiment_analysis = self._analyze_sentiment_comparison(
            article1.get('content', ''),
            article2.get('content', ''),
            article1.get('language', 'th')
        )
        
        # Find content differences
        content_differences = self._find_content_differences(
            article1.get('content', ''),
            article2.get('content', ''),
            article1.get('language', 'th')
        )
        
        # Calculate overall similarity
        overall_similarity = self._calculate_overall_similarity(
            content_similarity,
            entity_comparison['similarity'],
            keyword_comparison['similarity']
        )
        
        return {
            'similarity_score': overall_similarity,
            'content_similarity': content_similarity,
            'entity_comparison': entity_comparison,
            'keyword_comparison': keyword_comparison,
            'sentiment_analysis': sentiment_analysis,
            'content_differences': content_differences,
            'comparison_metadata': {
                'compared_at': datetime.utcnow(),
                'article1_id': article1.get('_id'),
                'article2_id': article2.get('_id'),
                'article1_source': article1.get('source'),
                'article2_source': article2.get('source')
            }
        }
    
    def _calculate_content_similarity(self, content1: str, content2: str, language: str = 'th') -> float:
        """Calculate semantic similarity between two content texts"""
        if not content1 or not content2:
            return 0.0
        
        try:
            # Preprocess texts
            processed_content1 = self._preprocess_text(content1, language)
            processed_content2 = self._preprocess_text(content2, language)
            
            if not processed_content1 or not processed_content2:
                return 0.0
            
            # Use TF-IDF vectorization
            vectorizer = TfidfVectorizer(
                max_features=1000,
                ngram_range=(1, 2),
                stop_words='english' if language == 'en' else None
            )
            
            tfidf_matrix = vectorizer.fit_transform([processed_content1, processed_content2])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
            
        except Exception as e:
            print(f"Error calculating content similarity: {str(e)}")
            return 0.0
    
    def _compare_entities(self, entities1: Dict[str, List[str]], entities2: Dict[str, List[str]]) -> Dict[str, Any]:
        """Compare named entities between two articles"""
        all_entity_types = set(entities1.keys()) | set(entities2.keys())
        
        common_entities = []
        different_entities = {
            'article1': [],
            'article2': []
        }
        
        for entity_type in all_entity_types:
            entities_1 = set(entities1.get(entity_type, []))
            entities_2 = set(entities2.get(entity_type, []))
            
            # Find common entities
            common = entities_1 & entities_2
            common_entities.extend(list(common))
            
            # Find different entities
            only_1 = entities_1 - entities_2
            only_2 = entities_2 - entities_1
            
            different_entities['article1'].extend(list(only_1))
            different_entities['article2'].extend(list(only_2))
        
        # Calculate entity similarity
        total_entities_1 = sum(len(entities) for entities in entities1.values())
        total_entities_2 = sum(len(entities) for entities in entities2.values())
        total_entities = total_entities_1 + total_entities_2
        
        if total_entities > 0:
            entity_similarity = (2 * len(common_entities)) / total_entities
        else:
            entity_similarity = 0.0
        
        return {
            'common_entities': common_entities,
            'different_entities': different_entities,
            'similarity': entity_similarity,
            'total_common': len(common_entities),
            'total_different_1': len(different_entities['article1']),
            'total_different_2': len(different_entities['article2'])
        }
    
    def _compare_keywords(self, keywords1: List[Dict[str, Any]], keywords2: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare keywords between two articles"""
        # Extract keyword strings
        keywords_1 = set()
        keywords_2 = set()
        
        for kw in keywords1:
            if isinstance(kw, dict):
                keywords_1.add(kw.get('keyword', ''))
            else:
                keywords_1.add(str(kw))
        
        for kw in keywords2:
            if isinstance(kw, dict):
                keywords_2.add(kw.get('keyword', ''))
            else:
                keywords_2.add(str(kw))
        
        # Remove empty strings
        keywords_1 = {kw for kw in keywords_1 if kw.strip()}
        keywords_2 = {kw for kw in keywords_2 if kw.strip()}
        
        # Find common and different keywords
        common_keywords = list(keywords_1 & keywords_2)
        different_keywords = {
            'article1': list(keywords_1 - keywords_2),
            'article2': list(keywords_2 - keywords_1)
        }
        
        # Calculate keyword similarity
        total_keywords = len(keywords_1) + len(keywords_2)
        if total_keywords > 0:
            keyword_similarity = (2 * len(common_keywords)) / total_keywords
        else:
            keyword_similarity = 0.0
        
        return {
            'common_keywords': common_keywords,
            'different_keywords': different_keywords,
            'similarity': keyword_similarity,
            'total_common': len(common_keywords),
            'total_different_1': len(different_keywords['article1']),
            'total_different_2': len(different_keywords['article2'])
        }
    
    def _analyze_sentiment_comparison(self, content1: str, content2: str, language: str = 'th') -> Dict[str, Any]:
        """Analyze and compare sentiment between two articles"""
        sentiment1 = self._analyze_sentiment(content1, language)
        sentiment2 = self._analyze_sentiment(content2, language)
        
        return {
            'article1': sentiment1,
            'article2': sentiment2,
            'sentiment_difference': {
                'positive': abs(sentiment1['positive'] - sentiment2['positive']),
                'neutral': abs(sentiment1['neutral'] - sentiment2['neutral']),
                'negative': abs(sentiment1['negative'] - sentiment2['negative'])
            }
        }
    
    def _analyze_sentiment(self, content: str, language: str = 'th') -> Dict[str, float]:
        """Analyze sentiment of a single article content"""
        if not content:
            return {'positive': 0.0, 'neutral': 1.0, 'negative': 0.0}
        
        content_lower = content.lower()
        
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        # Count sentiment keywords
        for keyword in self.sentiment_keywords['positive'][language]:
            positive_count += len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', content_lower))
        
        for keyword in self.sentiment_keywords['negative'][language]:
            negative_count += len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', content_lower))
        
        for keyword in self.sentiment_keywords['neutral'][language]:
            neutral_count += len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', content_lower))
        
        total_sentiment_words = positive_count + negative_count + neutral_count
        
        if total_sentiment_words == 0:
            return {'positive': 0.3, 'neutral': 0.4, 'negative': 0.3}  # Default neutral
        
        return {
            'positive': positive_count / total_sentiment_words,
            'neutral': neutral_count / total_sentiment_words,
            'negative': negative_count / total_sentiment_words
        }
    
    def _find_content_differences(self, content1: str, content2: str, language: str = 'th') -> List[Dict[str, Any]]:
        """Find significant differences between article contents"""
        differences = []
        
        # Split content into sentences
        sentences1 = self._split_sentences(content1, language)
        sentences2 = self._split_sentences(content2, language)
        
        # Find unique sentences (simplified approach)
        set1 = set(sentences1)
        set2 = set(sentences2)
        
        # Sentences only in article 1
        only_in_1 = set1 - set2
        for sentence in list(only_in_1)[:5]:  # Limit to 5 differences
            if len(sentence.strip()) > 30:  # Only significant sentences
                differences.append({
                    'type': 'removed',
                    'text': sentence.strip(),
                    'article': 1
                })
        
        # Sentences only in article 2
        only_in_2 = set2 - set1
        for sentence in list(only_in_2)[:5]:  # Limit to 5 differences
            if len(sentence.strip()) > 30:  # Only significant sentences
                differences.append({
                    'type': 'added',
                    'text': sentence.strip(),
                    'article': 2
                })
        
        return differences
    
    def _split_sentences(self, content: str, language: str = 'th') -> List[str]:
        """Split content into sentences"""
        if language == 'th':
            # Thai sentence splitting
            sentences = re.split(r'[.!?]', content)
        else:
            # English sentence splitting
            sentences = re.split(r'[.!?]+', content)
        
        return [s.strip() for s in sentences if len(s.strip()) > 10]
    
    def _preprocess_text(self, text: str, language: str = 'th') -> str:
        """Preprocess text for similarity analysis"""
        if not text:
            return ""
        
        # Basic cleaning
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single space
        text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
        text = text.lower().strip()
        
        return text
    
    def _calculate_overall_similarity(self, content_sim: float, entity_sim: float, keyword_sim: float) -> float:
        """Calculate weighted overall similarity score"""
        weights = {
            'content': 0.5,
            'entities': 0.3,
            'keywords': 0.2
        }
        
        overall = (
            content_sim * weights['content'] +
            entity_sim * weights['entities'] +
            keyword_sim * weights['keywords']
        )
        
        return min(max(overall, 0.0), 1.0)  # Ensure 0-1 range
    
    def compare_multiple_articles(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare multiple articles and find similarity patterns"""
        if len(articles) < 2:
            return {'error': 'Need at least 2 articles for comparison'}
        
        comparisons = []
        similarity_matrix = np.zeros((len(articles), len(articles)))
        
        for i in range(len(articles)):
            for j in range(i + 1, len(articles)):
                comparison = self.compare_articles(articles[i], articles[j])
                similarity_score = comparison['similarity_score']
                
                similarity_matrix[i][j] = similarity_score
                similarity_matrix[j][i] = similarity_score
                
                comparisons.append({
                    'article1_index': i,
                    'article2_index': j,
                    'similarity_score': similarity_score,
                    'comparison': comparison
                })
        
        # Find most similar and most different pairs
        similarities = [comp['similarity_score'] for comp in comparisons]
        
        most_similar_idx = np.argmax(similarities)
        most_different_idx = np.argmin(similarities)
        
        return {
            'comparisons': comparisons,
            'similarity_matrix': similarity_matrix.tolist(),
            'most_similar_pair': comparisons[most_similar_idx],
            'most_different_pair': comparisons[most_different_idx],
            'average_similarity': np.mean(similarities),
            'similarity_distribution': {
                'high': len([s for s in similarities if s > 0.7]),
                'medium': len([s for s in similarities if 0.3 <= s <= 0.7]),
                'low': len([s for s in similarities if s < 0.3])
            }
        }
