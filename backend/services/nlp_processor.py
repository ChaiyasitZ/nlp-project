import re
from typing import List, Dict, Any
import pythainlp
from pythainlp import word_tokenize, pos_tag
from pythainlp.corpus import thai_stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from datetime import datetime
import dateparser


class NLPProcessor:
    """NLP processor for Thai and English text analysis"""
    
    def __init__(self):
        self.thai_stopwords = list(thai_stopwords())
        self.english_stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'was', 'are', 'were', 'be', 'been',
            'have', 'has', 'had', 'will', 'would', 'could', 'should', 'may', 'might'
        }
        
        # Entity patterns for Thai text
        self.thai_entity_patterns = {
            'PERSON': [
                r'นาย[ก-ฮ][ก-ฮ\s]+',
                r'นาง[ก-ฮ][ก-ฮ\s]+',
                r'น\.ส\.[ก-ฮ][ก-ฮ\s]+',
                r'ดร\.[ก-ฮ][ก-ฮ\s]+',
                r'ศ\.[ก-ฮ][ก-ฮ\s]+',
                r'รศ\.[ก-ฮ][ก-ฮ\s]+',
                r'ผศ\.[ก-ฮ][ก-ฮ\s]+'
            ],
            'ORGANIZATION': [
                r'กระทรวง[ก-ฮ\s]+',
                r'กรม[ก-ฮ\s]+',
                r'องค์การ[ก-ฮ\s]+',
                r'บริษัท[ก-ฮ\s]+',
                r'มหาวิทยาลัย[ก-ฮ\s]+',
                r'โรงเรียน[ก-ฮ\s]+',
                r'พรรค[ก-ฮ\s]+'
            ],
            'LOCATION': [
                r'จังหวัด[ก-ฮ\s]+',
                r'อำเภอ[ก-ฮ\s]+',
                r'ตำบล[ก-ฮ\s]+',
                r'กรุงเทพ[ก-ฮ]*',
                r'เมือง[ก-ฮ\s]+',
                r'ประเทศ[ก-ฮ\s]+'
            ]
        }
    
    def process_article(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single article with NLP analysis
        
        Args:
            article_data (dict): Raw article data
            
        Returns:
            dict: Processed article with NLP results
        """
        content = article_data.get('content', '')
        title = article_data.get('title', '')
        
        # Detect language
        language = self._detect_language(content)
        
        # Tokenize text
        tokens = self._tokenize_text(content, language)
        
        # Extract entities
        entities = self._extract_entities(content, language)
        
        # Extract keywords
        keywords = self._extract_keywords(content, language)
        
        # Extract events
        events = self._extract_events(content, title, language)
        
        # Extract dates from content
        dates = self._extract_dates_from_text(content)
        
        # Add NLP results to article data
        processed_article = article_data.copy()
        processed_article.update({
            'language': language,
            'tokens': tokens,
            'entities': entities,
            'keywords': keywords,
            'events': events,
            'content_dates': dates,
            'processed_at': datetime.utcnow(),
            'word_count': len(tokens),
            'sentence_count': len(re.split(r'[.!?]', content))
        })
        
        return processed_article
    
    def _detect_language(self, text: str) -> str:
        """Detect if text is primarily Thai or English"""
        thai_chars = len(re.findall(r'[ก-ฮ]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        
        if thai_chars > english_chars:
            return 'th'
        elif english_chars > thai_chars:
            return 'en'
        else:
            return 'mixed'
    
    def _tokenize_text(self, text: str, language: str) -> List[str]:
        """Tokenize text based on language"""
        if language == 'th' or language == 'mixed':
            tokens = word_tokenize(text, engine='newmm')
        else:
            tokens = re.findall(r'\b\w+\b', text.lower())
        
        # Remove stopwords and short tokens
        if language == 'th' or language == 'mixed':
            filtered_tokens = [
                token for token in tokens 
                if token not in self.thai_stopwords and len(token) > 1
            ]
        else:
            filtered_tokens = [
                token for token in tokens 
                if token not in self.english_stopwords and len(token) > 2
            ]
        
        return filtered_tokens
    
    def _extract_entities(self, text: str, language: str) -> Dict[str, List[str]]:
        """Extract named entities from text"""
        entities = {
            'PERSON': [],
            'ORGANIZATION': [],
            'LOCATION': [],
            'MISC': []
        }
        
        if language == 'th' or language == 'mixed':
            # Use regex patterns for Thai entities
            for entity_type, patterns in self.thai_entity_patterns.items():
                for pattern in patterns:
                    matches = re.findall(pattern, text)
                    entities[entity_type].extend([match.strip() for match in matches])
        
        # Remove duplicates
        for entity_type in entities:
            entities[entity_type] = list(set(entities[entity_type]))
        
        return entities
    
    def _extract_keywords(self, text: str, language: str, max_keywords: int = 10) -> List[Dict[str, float]]:
        """Extract important keywords using TF-IDF"""
        try:
            # Tokenize for TF-IDF
            if language == 'th' or language == 'mixed':
                tokens = word_tokenize(text, engine='newmm')
                processed_text = ' '.join([
                    token for token in tokens 
                    if token not in self.thai_stopwords and len(token) > 1
                ])
            else:
                processed_text = re.sub(r'[^\w\s]', ' ', text.lower())
            
            # Use TF-IDF
            vectorizer = TfidfVectorizer(
                max_features=max_keywords * 2,
                ngram_range=(1, 2),
                stop_words='english' if language == 'en' else None
            )
            
            tfidf_matrix = vectorizer.fit_transform([processed_text])
            feature_names = vectorizer.get_feature_names_out()
            tfidf_scores = tfidf_matrix.toarray()[0]
            
            # Get top keywords
            keyword_scores = list(zip(feature_names, tfidf_scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            keywords = [
                {'keyword': keyword, 'score': float(score)}
                for keyword, score in keyword_scores[:max_keywords]
                if score > 0
            ]
            
            return keywords
            
        except Exception as e:
            print(f"Error extracting keywords: {str(e)}")
            return []
    
    def _extract_events(self, content: str, title: str, language: str) -> List[Dict[str, Any]]:
        """Extract events from article content"""
        events = []
        
        # Event indicators for Thai
        thai_event_patterns = [
            r'เกิดเหตุ[ก-ฮ\s]+',
            r'เสียชีวิต[ก-ฮ\s]*',
            r'ได้รับบาดเจ็บ[ก-ฮ\s]*',
            r'ประกาศ[ก-ฮ\s]+',
            r'เปิดเผย[ก-ฮ\s]+',
            r'ลงนาม[ก-ฮ\s]+',
            r'ประชุม[ก-ฮ\s]+',
            r'แถลงข่าว[ก-ฮ\s]*'
        ]
        
        # English event patterns
        english_event_patterns = [
            r'announced\s+\w+',
            r'declared\s+\w+',
            r'signed\s+\w+',
            r'meeting\s+\w+',
            r'conference\s+\w+',
            r'died\s+\w*',
            r'injured\s+\w*'
        ]
        
        patterns = thai_event_patterns if language == 'th' or language == 'mixed' else english_event_patterns
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # Extract surrounding context
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 50)
                context = content[start:end].strip()
                
                events.append({
                    'event_text': match.group(),
                    'context': context,
                    'position': match.start(),
                    'confidence': 0.7  # Basic confidence score
                })
        
        return events[:5]  # Limit to 5 events per article
    
    def _extract_dates_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract dates mentioned in the text content"""
        dates = []
        
        # Thai date patterns
        thai_date_patterns = [
            r'\d{1,2}\s+[ก-ฮ]+\s+\d{4}',  # 15 มกราคม 2567
            r'\d{1,2}/\d{1,2}/\d{4}',      # 15/01/2024
            r'\d{1,2}-\d{1,2}-\d{4}'       # 15-01-2024
        ]
        
        for pattern in thai_date_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                date_str = match.group()
                parsed_date = dateparser.parse(date_str)
                if parsed_date:
                    dates.append({
                        'date_string': date_str,
                        'parsed_date': parsed_date,
                        'position': match.start()
                    })
        
        return dates
    
    def calculate_similarity(self, text1: str, text2: str, language: str = 'th') -> float:
        """Calculate semantic similarity between two texts"""
        try:
            # Tokenize both texts
            tokens1 = self._tokenize_text(text1, language)
            tokens2 = self._tokenize_text(text2, language)
            
            # Create processed texts
            processed_text1 = ' '.join(tokens1)
            processed_text2 = ' '.join(tokens2)
            
            if not processed_text1 or not processed_text2:
                return 0.0
            
            # Use TF-IDF vectorization
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform([processed_text1, processed_text2])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
            
        except Exception as e:
            print(f"Error calculating similarity: {str(e)}")
            return 0.0
