"""
MongoDB service for GitAgent user management
"""

import os
from datetime import datetime
from typing import Optional, Dict, Any
import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError


class MongoDBService:
    """Service for managing GitAgent users in MongoDB"""
    
    def __init__(self):
        self.connection_string = "mongodb+srv://root:root@learningmongo.cr2lsf3.mongodb.net/"
        self.database_name = "GitAgent"
        self.collection_name = "Users"
        self.client = None
        self.db = None
        self.collection = None
    
    def connect(self) -> bool:
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(
                self.connection_string,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=10000,  # 10 second timeout
                socketTimeoutMS=10000    # 10 second timeout
            )
            
            # Test the connection
            self.client.admin.command('ping')
            
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            
            return True
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error connecting to MongoDB: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            self.collection = None
    
    def user_exists(self, email: str) -> bool:
        """Check if user exists in database"""
        if self.collection is None:
            return False
        
        try:
            user = self.collection.find_one({"email": email})
            return user is not None
        except Exception as e:
            print(f"❌ Error checking user existence: {e}")
            return False
    
    def create_user(self, email: str, api_key: Optional[str] = None) -> bool:
        """Create a new user in the database"""
        if self.collection is None:
            return False
        
        try:
            user_data = {
                "email": email,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow(),
                "apiKey": api_key or ""  # Will be manually set later
            }
            
            result = self.collection.insert_one(user_data)
            return result.inserted_id is not None
            
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            return False
    
    def get_user(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user data from database"""
        if self.collection is None:
            return None
        
        try:
            user = self.collection.find_one({"email": email})
            return user
        except Exception as e:
            print(f"❌ Error getting user: {e}")
            return None
    
    def update_user(self, email: str, update_data: Dict[str, Any]) -> bool:
        """Update user data in database"""
        if self.collection is None:
            return False
        
        try:
            update_data["updatedAt"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"email": email},
                {"$set": update_data}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            print(f"❌ Error updating user: {e}")
            return False
    
    def has_valid_api_key(self, email: str) -> bool:
        """Check if user has a valid API key"""
        user = self.get_user(email)
        if not user:
            return False
        
        api_key = user.get("apiKey", "")
        return api_key and api_key.strip() != "" 