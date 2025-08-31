# API Testing for NewsTimelineAI Backend

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_analyze_news():
    """Test news analysis endpoint"""
    print("Testing news analysis...")
    
    # Sample data
    test_data = {
        "input_type": "url",
        "urls": [
            "https://www.bangkokpost.com/thailand/general/2484218/pm-orders-flood-relief-measures",
            "https://www.nationthailand.com/thailand/general/40025123"
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/api/analyze-news",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Analysis ID: {result.get('analysis_id')}")
        print(f"Articles processed: {len(result.get('articles', []))}")
        print(f"Timeline events: {len(result.get('timeline', {}).get('events', []))}")
    else:
        print(f"Error: {response.text}")
    print()

def test_articles_list():
    """Test articles listing endpoint"""
    print("Testing articles list...")
    response = requests.get(f"{BASE_URL}/api/articles")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Total articles: {len(result.get('articles', []))}")
        print(f"Pagination: {result.get('pagination')}")
    else:
        print(f"Error: {response.text}")
    print()

if __name__ == "__main__":
    print("NewsTimelineAI API Testing")
    print("=" * 30)
    
    try:
        test_health_check()
        test_analyze_news()
        test_articles_list()
        
        print("All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the backend server.")
        print("Make sure the Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"Error during testing: {str(e)}")
