from typing import List, Dict, Any
from datetime import datetime, timedelta
import re
from collections import defaultdict


class TimelineGenerator:
    """Generate timeline from processed news articles"""
    
    def __init__(self):
        self.event_weight_factors = {
            'entities_count': 0.3,
            'keywords_count': 0.2,
            'content_length': 0.2,
            'source_credibility': 0.3
        }
        
        # Source credibility scores (can be adjusted)
        self.source_credibility = {
            'Bangkok Post': 0.9,
            'The Nation Thailand': 0.9,
            'Thai PBS': 0.95,
            'Thairath': 0.8,
            'Khaosod': 0.8,
            'Matichon': 0.85,
            'Manager': 0.7,
            'Sanook': 0.6,
            'Kapook': 0.6,
            'Daily News': 0.7
        }
    
    def generate_timeline(self, processed_articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate timeline from processed articles
        
        Args:
            processed_articles (list): List of processed article dictionaries
            
        Returns:
            dict: Timeline data with events, chart data, and statistics
        """
        # Sort articles by date
        dated_articles = self._filter_and_sort_articles(processed_articles)
        
        # Group articles by date
        date_groups = self._group_articles_by_date(dated_articles)
        
        # Extract timeline events
        timeline_events = self._extract_timeline_events(date_groups)
        
        # Calculate event intensity for chart
        chart_data = self._generate_chart_data(timeline_events)
        
        # Generate summary statistics
        statistics = self._generate_statistics(processed_articles, timeline_events)
        
        return {
            'events': timeline_events,
            'chart_data': chart_data,
            'statistics': statistics,
            'date_range': self._get_date_range(dated_articles),
            'total_articles': len(processed_articles),
            'generated_at': datetime.utcnow()
        }
    
    def _filter_and_sort_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter articles with valid dates and sort by date"""
        dated_articles = []
        
        for article in articles:
            # Try to get date from published_date or content_dates
            article_date = None
            
            if article.get('published_date'):
                article_date = article['published_date']
            elif article.get('content_dates') and len(article['content_dates']) > 0:
                # Use the first date found in content
                article_date = article['content_dates'][0]['parsed_date']
            elif article.get('scraped_at'):
                # Fallback to scraped date
                article_date = article['scraped_at']
            
            if article_date:
                article['timeline_date'] = article_date
                dated_articles.append(article)
        
        # Sort by date
        return sorted(dated_articles, key=lambda x: x['timeline_date'])
    
    def _group_articles_by_date(self, articles: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group articles by date (day-level)"""
        date_groups = defaultdict(list)
        
        for article in articles:
            date_key = article['timeline_date'].strftime('%Y-%m-%d')
            date_groups[date_key].append(article)
        
        return dict(date_groups)
    
    def _extract_timeline_events(self, date_groups: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Extract significant events for timeline"""
        timeline_events = []
        event_id = 1
        
        for date_str, articles in date_groups.items():
            # Calculate event significance for this date
            event_intensity = self._calculate_event_intensity(articles)
            
            # Get main entities and keywords for this date
            all_entities = self._merge_entities(articles)
            all_keywords = self._merge_keywords(articles)
            
            # Create event summary
            event_title = self._generate_event_title(articles, all_entities)
            event_description = self._generate_event_description(articles, all_keywords)
            
            # Get unique sources
            sources = list(set([article['source'] for article in articles]))
            
            timeline_event = {
                'id': event_id,
                'date': date_str,
                'title': event_title,
                'description': event_description,
                'intensity': event_intensity,
                'entities': all_entities,
                'keywords': all_keywords[:10],  # Top 10 keywords
                'sources': sources,
                'article_count': len(articles),
                'articles': [
                    {
                        'id': article.get('_id', f"article_{i}"),
                        'title': article['title'],
                        'source': article['source'],
                        'url': article['url']
                    }
                    for i, article in enumerate(articles)
                ]
            }
            
            timeline_events.append(timeline_event)
            event_id += 1
        
        return timeline_events
    
    def _calculate_event_intensity(self, articles: List[Dict[str, Any]]) -> float:
        """Calculate intensity score for events on a given date"""
        if not articles:
            return 0.0
        
        total_score = 0.0
        
        for article in articles:
            score = 0.0
            
            # Entity count factor
            entity_count = sum(len(entities) for entities in article.get('entities', {}).values())
            score += entity_count * self.event_weight_factors['entities_count']
            
            # Keyword count factor
            keyword_count = len(article.get('keywords', []))
            score += keyword_count * self.event_weight_factors['keywords_count']
            
            # Content length factor (normalized)
            content_length = article.get('word_count', 0)
            normalized_length = min(content_length / 1000, 1.0)  # Cap at 1000 words
            score += normalized_length * self.event_weight_factors['content_length']
            
            # Source credibility factor
            source = article.get('source', 'Unknown')
            credibility = self.source_credibility.get(source, 0.5)
            score += credibility * self.event_weight_factors['source_credibility']
            
            total_score += score
        
        # Average and normalize to 0-10 scale
        average_score = total_score / len(articles)
        return min(average_score * 2, 10.0)  # Scale to 0-10
    
    def _merge_entities(self, articles: List[Dict[str, Any]]) -> List[str]:
        """Merge and deduplicate entities from multiple articles"""
        entity_counts = defaultdict(int)
        
        for article in articles:
            entities = article.get('entities', {})
            for entity_type, entity_list in entities.items():
                for entity in entity_list:
                    entity_counts[entity] += 1
        
        # Sort by frequency and return top entities
        sorted_entities = sorted(entity_counts.items(), key=lambda x: x[1], reverse=True)
        return [entity for entity, count in sorted_entities[:15]]
    
    def _merge_keywords(self, articles: List[Dict[str, Any]]) -> List[Dict[str, float]]:
        """Merge and weight keywords from multiple articles"""
        keyword_scores = defaultdict(float)
        
        for article in articles:
            keywords = article.get('keywords', [])
            for keyword_data in keywords:
                if isinstance(keyword_data, dict):
                    keyword = keyword_data.get('keyword', '')
                    score = keyword_data.get('score', 0.0)
                else:
                    keyword = str(keyword_data)
                    score = 1.0
                
                keyword_scores[keyword] += score
        
        # Sort by score and return top keywords
        sorted_keywords = sorted(keyword_scores.items(), key=lambda x: x[1], reverse=True)
        return [
            {'keyword': keyword, 'score': score}
            for keyword, score in sorted_keywords
        ]
    
    def _generate_event_title(self, articles: List[Dict[str, Any]], entities: List[str]) -> str:
        """Generate a descriptive title for the timeline event"""
        if len(articles) == 1:
            return articles[0]['title']
        
        # Use most common entities or generic description
        if entities:
            main_entity = entities[0]
            return f"News about {main_entity} ({len(articles)} articles)"
        else:
            return f"Multiple news events ({len(articles)} articles)"
    
    def _generate_event_description(self, articles: List[Dict[str, Any]], keywords: List[Dict[str, float]]) -> str:
        """Generate a description for the timeline event"""
        sources = list(set([article['source'] for article in articles]))
        
        description_parts = []
        
        if len(articles) > 1:
            description_parts.append(f"{len(articles)} articles from {len(sources)} source(s)")
        
        if keywords:
            top_keywords = [kw['keyword'] for kw in keywords[:5]]
            description_parts.append(f"Key topics: {', '.join(top_keywords)}")
        
        if sources:
            description_parts.append(f"Sources: {', '.join(sources)}")
        
        return '. '.join(description_parts)
    
    def _generate_chart_data(self, timeline_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate chart data for timeline visualization"""
        if not timeline_events:
            return {'labels': [], 'datasets': []}
        
        # Sort events by date
        sorted_events = sorted(timeline_events, key=lambda x: x['date'])
        
        labels = [event['date'] for event in sorted_events]
        intensities = [event['intensity'] for event in sorted_events]
        article_counts = [event['article_count'] for event in sorted_events]
        
        return {
            'labels': labels,
            'datasets': [
                {
                    'label': 'Event Intensity',
                    'data': intensities,
                    'borderColor': 'rgb(59, 130, 246)',
                    'backgroundColor': 'rgba(59, 130, 246, 0.1)',
                    'tension': 0.4,
                    'yAxisID': 'y'
                },
                {
                    'label': 'Article Count',
                    'data': article_counts,
                    'borderColor': 'rgb(16, 185, 129)',
                    'backgroundColor': 'rgba(16, 185, 129, 0.1)',
                    'tension': 0.4,
                    'yAxisID': 'y1'
                }
            ]
        }
    
    def _generate_statistics(self, all_articles: List[Dict[str, Any]], timeline_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics"""
        if not all_articles:
            return {}
        
        # Count entities and keywords
        all_entities = defaultdict(int)
        all_keywords = defaultdict(float)
        sources = defaultdict(int)
        
        for article in all_articles:
            # Count entities
            entities = article.get('entities', {})
            for entity_type, entity_list in entities.items():
                for entity in entity_list:
                    all_entities[entity] += 1
            
            # Count keywords
            keywords = article.get('keywords', [])
            for keyword_data in keywords:
                if isinstance(keyword_data, dict):
                    keyword = keyword_data.get('keyword', '')
                    score = keyword_data.get('score', 0.0)
                else:
                    keyword = str(keyword_data)
                    score = 1.0
                all_keywords[keyword] += score
            
            # Count sources
            source = article.get('source', 'Unknown')
            sources[source] += 1
        
        # Get top items
        top_entities = sorted(all_entities.items(), key=lambda x: x[1], reverse=True)[:10]
        top_keywords = sorted(all_keywords.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'total_events': len(timeline_events),
            'total_articles': len(all_articles),
            'unique_sources': len(sources),
            'top_entities': [{'entity': entity, 'count': count} for entity, count in top_entities],
            'top_keywords': [{'keyword': keyword, 'score': score} for keyword, score in top_keywords],
            'source_distribution': dict(sources),
            'average_intensity': sum(event['intensity'] for event in timeline_events) / len(timeline_events) if timeline_events else 0
        }
    
    def _get_date_range(self, articles: List[Dict[str, Any]]) -> Dict[str, str]:
        """Get the date range of articles"""
        if not articles:
            return {'start': None, 'end': None}
        
        dates = [article['timeline_date'] for article in articles]
        return {
            'start': min(dates).strftime('%Y-%m-%d'),
            'end': max(dates).strftime('%Y-%m-%d')
        }
