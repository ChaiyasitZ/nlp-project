#!/usr/bin/env python3
"""
Test the exact MongoDB connection string you provided
"""

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def test_atlas_connection():
    """Test connection using the MongoDB Atlas recommended method"""
    
    # Get URI from environment
    uri = os.getenv('MONGO_URI')
    
    if not uri:
        print("❌ No MONGO_URI found in .env file")
        return False
    
    print(f"🔍 Testing MongoDB Atlas connection...")
    print(f"📋 URI: {uri[:50]}...")
    
    try:
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("✅ Pinged your deployment. You successfully connected to MongoDB!")
        
        # Test database access
        db = client.newstimelineai  # Your database name
        print(f"📁 Database: {db.name}")
        
        # List collections
        collections = db.list_collection_names()
        print(f"📋 Collections: {collections}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_atlas_connection()
    
    if not success:
        print("\n💡 To fix authentication issues:")
        print("1. Go to MongoDB Atlas → Database Access")
        print("2. Create a new database user:")
        print("   - Username: newsuser")
        print("   - Password: (create a strong password)")
        print("   - Privileges: Read and write to any database")
        print("3. Update your .env file with the new credentials:")
        print("   MONGO_URI=mongodb+srv://newsuser:YOUR_PASSWORD@cluster0.urspt1h.mongodb.net/newstimelineai?retryWrites=true&w=majority&appName=Cluster0")
        print("4. Go to Network Access and add IP: 0.0.0.0/0")
        
    input("\nPress Enter to continue...")
