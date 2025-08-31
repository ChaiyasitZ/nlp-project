#!/usr/bin/env python3
"""
MongoDB Atlas Connection Test Script

This script helps diagnose MongoDB Atlas connection issues.
"""

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

def test_connection():
    """Test MongoDB Atlas connection with detailed error reporting"""
    print("🔍 MongoDB Atlas Connection Diagnostic")
    print("=" * 50)
    
    # Get connection string
    mongo_uri = os.getenv('MONGO_URI')
    if not mongo_uri:
        print("❌ MONGO_URI not found in .env file")
        return False
    
    print(f"📋 Connection String: {mongo_uri[:50]}...")
    
    # Parse connection string for debugging
    if "mongodb+srv://" in mongo_uri:
        print("✅ Using SRV connection format")
        
        # Extract components
        try:
            # Basic parsing to check format
            if "@" in mongo_uri:
                auth_part = mongo_uri.split("@")[0]
                if ":" in auth_part:
                    print("✅ Username and password detected")
                else:
                    print("❌ Missing username or password")
            
            if "cluster" in mongo_uri.lower():
                print("✅ Cluster URL detected")
            else:
                print("⚠️  No cluster URL detected")
                
        except Exception as e:
            print(f"❌ Error parsing connection string: {e}")
    
    print("\n🔌 Testing connection...")
    
    try:
        # Create client with shorter timeout for faster diagnosis
        client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=5000,
            socketTimeoutMS=5000
        )
        
        # Test connection
        print("⏳ Attempting to connect...")
        
        # Try to ping the server
        result = client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        print(f"✅ Ping result: {result}")
        
        # Get server info
        server_info = client.server_info()
        print(f"📊 MongoDB Version: {server_info.get('version', 'Unknown')}")
        
        # List databases (if permissions allow)
        try:
            dbs = client.list_database_names()
            print(f"📁 Available databases: {dbs}")
        except OperationFailure as e:
            print(f"⚠️  Cannot list databases (permission issue): {e}")
        
        # Test specific database access
        db_name = "newstimelineai"
        db = client[db_name]
        
        try:
            # Try to access the database
            collections = db.list_collection_names()
            print(f"📁 Collections in '{db_name}': {collections}")
        except OperationFailure as e:
            print(f"⚠️  Cannot access database '{db_name}': {e}")
        
        client.close()
        return True
        
    except ServerSelectionTimeoutError as e:
        print(f"❌ Server selection timeout: {e}")
        print("\n🔧 Possible solutions:")
        print("   1. Check your internet connection")
        print("   2. Verify cluster is running in MongoDB Atlas")
        print("   3. Check network access settings in Atlas")
        return False
        
    except ConnectionFailure as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 Possible solutions:")
        print("   1. Check username and password")
        print("   2. Verify cluster URL is correct")
        print("   3. Check if cluster is paused")
        return False
        
    except OperationFailure as e:
        error_code = getattr(e, 'code', None)
        
        if error_code == 8000:  # Authentication failed
            print(f"❌ Authentication failed: {e}")
            print("\n🔧 Possible solutions:")
            print("   1. Verify username and password are correct")
            print("   2. Check if database user exists in Atlas")
            print("   3. Verify user has proper permissions")
            print("   4. Make sure password doesn't contain special characters that need encoding")
            
        elif error_code == 13:  # Unauthorized
            print(f"❌ Unauthorized access: {e}")
            print("\n🔧 Possible solutions:")
            print("   1. Check user permissions in MongoDB Atlas")
            print("   2. Verify user has read/write access to the database")
            
        else:
            print(f"❌ Operation failed: {e}")
            
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

def main():
    """Main test function"""
    success = test_connection()
    
    if not success:
        print(f"\n💡 Next steps:")
        print("   1. Log into MongoDB Atlas (https://cloud.mongodb.com)")
        print("   2. Check 'Network Access' settings")
        print("   3. Add your IP address: 0.0.0.0/0 (for testing)")
        print("   4. Check 'Database Access' for user permissions")
        print("   5. Verify cluster is not paused")
        
    print(f"\n{'='*50}")
    return success

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to continue...")
    sys.exit(0 if success else 1)
