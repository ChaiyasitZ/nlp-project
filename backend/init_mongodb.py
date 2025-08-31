#!/usr/bin/env python3
"""
MongoDB Atlas Initialization Script for NewsTimelineAI

This script initializes the MongoDB database with the required collections
and indexes for optimal performance.
"""

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

def get_mongodb_client():
    """Get MongoDB client connection"""
    mongo_uri = os.getenv('MONGO_URI')
    if not mongo_uri:
        raise ValueError("MONGO_URI not found in environment variables")
    
    try:
        client = MongoClient(mongo_uri)
        # Test the connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        return client
    except ConnectionFailure as e:
        print(f"❌ Failed to connect to MongoDB Atlas: {e}")
        return None

def initialize_database(client):
    """Initialize database and collections"""
    try:
        # Get database name from URI or use default
        db_name = "newstimelineai"
        db = client[db_name]
        
        print(f"🔧 Initializing database: {db_name}")
        
        # Define collections and their initial structure
        collections_config = {
            'articles': {
                'description': 'Stores processed news articles',
                'indexes': [
                    ('url', 1),  # Unique index on URL
                    ('published_date', -1),  # Descending by date
                    ('language', 1),
                    ('keywords', 1),
                    ('created_at', -1)
                ],
                'sample_doc': {
                    'url': 'https://example.com/news/sample',
                    'title': 'Sample News Article',
                    'content': 'Sample content...',
                    'published_date': datetime.utcnow(),
                    'language': 'th',
                    'keywords': ['keyword1', 'keyword2'],
                    'entities': ['entity1', 'entity2'],
                    'sentiment': {'score': 0.5, 'label': 'neutral'},
                    'summary': 'Sample summary...',
                    'created_at': datetime.utcnow(),
                    '_sample': True  # Mark as sample data
                }
            },
            'analyses': {
                'description': 'Stores timeline analysis results',
                'indexes': [
                    ('created_at', -1),
                    ('input_type', 1),
                    ('urls', 1)
                ],
                'sample_doc': {
                    'articles': [],
                    'timeline': {
                        'events': [],
                        'statistics': {}
                    },
                    'created_at': datetime.utcnow(),
                    'input_type': 'url',
                    'urls': ['https://example.com'],
                    '_sample': True
                }
            },
            'comparisons': {
                'description': 'Stores article similarity comparisons',
                'indexes': [
                    ('article1_id', 1),
                    ('article2_id', 1),
                    ('created_at', -1),
                    ([('article1_id', 1), ('article2_id', 1)], {'unique': True})
                ],
                'sample_doc': {
                    'article1_id': 'sample_id_1',
                    'article2_id': 'sample_id_2',
                    'similarity_result': {
                        'similarity_score': 0.75,
                        'common_keywords': ['keyword1'],
                        'common_entities': ['entity1']
                    },
                    'created_at': datetime.utcnow(),
                    '_sample': True
                }
            },
            'timelines': {
                'description': 'Stores generated timeline data',
                'indexes': [
                    ('analysis_id', 1),
                    ('created_at', -1),
                    ('event_date', 1)
                ],
                'sample_doc': {
                    'analysis_id': 'sample_analysis_id',
                    'events': [
                        {
                            'date': datetime.utcnow(),
                            'title': 'Sample Event',
                            'description': 'Sample event description',
                            'articles': ['article_id_1'],
                            'importance': 0.8
                        }
                    ],
                    'created_at': datetime.utcnow(),
                    '_sample': True
                }
            }
        }
        
        # Create collections and indexes
        for collection_name, config in collections_config.items():
            print(f"📁 Setting up collection: {collection_name}")
            print(f"   Description: {config['description']}")
            
            collection = db[collection_name]
            
            # Create indexes
            for index_config in config['indexes']:
                try:
                    if isinstance(index_config, tuple) and len(index_config) == 2:
                        # Handle compound indexes with options
                        if isinstance(index_config[0], list):
                            collection.create_index(index_config[0], **index_config[1])
                            print(f"   ✅ Created compound index: {index_config[0]}")
                        else:
                            collection.create_index(index_config[0], unique=(index_config[1] == 1))
                            print(f"   ✅ Created index: {index_config[0]}")
                    else:
                        collection.create_index(index_config)
                        print(f"   ✅ Created index: {index_config}")
                except OperationFailure as e:
                    if "already exists" in str(e):
                        print(f"   ⚠️  Index already exists: {index_config}")
                    else:
                        print(f"   ❌ Failed to create index {index_config}: {e}")
            
            # Insert sample document if collection is empty
            if collection.count_documents({}) == 0:
                collection.insert_one(config['sample_doc'])
                print(f"   ✅ Inserted sample document")
            else:
                print(f"   ℹ️  Collection already has documents")
        
        print(f"\n🎉 Database initialization completed successfully!")
        print(f"Database: {db_name}")
        print(f"Collections created: {len(collections_config)}")
        
        # Display collection statistics
        print(f"\n📊 Collection Statistics:")
        for collection_name in collections_config.keys():
            count = db[collection_name].count_documents({})
            print(f"   {collection_name}: {count} documents")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

def test_database_operations(client):
    """Test basic database operations"""
    try:
        db = client["newstimelineai"]
        
        print(f"\n🧪 Testing database operations...")
        
        # Test insert
        test_doc = {
            'test': True,
            'message': 'Database test successful',
            'timestamp': datetime.utcnow()
        }
        
        result = db.test_collection.insert_one(test_doc)
        print(f"   ✅ Insert test: {result.inserted_id}")
        
        # Test find
        found_doc = db.test_collection.find_one({'test': True})
        if found_doc:
            print(f"   ✅ Find test: Document found")
        else:
            print(f"   ❌ Find test: Document not found")
        
        # Test update
        update_result = db.test_collection.update_one(
            {'test': True},
            {'$set': {'updated': True}}
        )
        print(f"   ✅ Update test: {update_result.modified_count} document updated")
        
        # Test delete
        delete_result = db.test_collection.delete_one({'test': True})
        print(f"   ✅ Delete test: {delete_result.deleted_count} document deleted")
        
        # Clean up test collection
        db.test_collection.drop()
        print(f"   🧹 Cleaned up test collection")
        
        return True
        
    except Exception as e:
        print(f"❌ Database operation test failed: {e}")
        return False

def main():
    """Main initialization function"""
    print("🚀 Starting MongoDB Atlas initialization for NewsTimelineAI")
    print("=" * 60)
    
    # Get MongoDB client
    client = get_mongodb_client()
    if not client:
        print("❌ Cannot proceed without database connection")
        return False
    
    try:
        # Initialize database
        if not initialize_database(client):
            return False
        
        # Test database operations
        if not test_database_operations(client):
            return False
        
        print("\n" + "=" * 60)
        print("🎉 MongoDB Atlas initialization completed successfully!")
        print("You can now start your Flask application.")
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False
        
    finally:
        if client:
            client.close()
            print("🔌 Database connection closed")

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
