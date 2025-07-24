#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MongoDB Atlas Cloud Import Script
================================
Import real estate data to MongoDB Atlas for public sharing

Usage:
    python atlas_import.py

Requirements:
    - pymongo
    - MongoDB Atlas cluster setup
    - Connection string configured
"""

import json
import os
import sys
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import time

class AtlasImporter:
    def __init__(self):
        # MongoDB Atlas Connection String
        # Configured with actual cluster credentials
        self.ATLAS_URI = "mongodb+srv://khoi:123@khoilh7705.xdst8xm.mongodb.net/?retryWrites=true&w=majority&appName=khoilh7705"
        self.DATABASE_NAME = "real_estate_db"
        self.DATA_FILE = "../step4_mongodb_format/step4_mongodb_format.json"
        
        self.client = None
        self.db = None
        
    def load_data(self):
        """Load MongoDB format data from Step 4"""
        try:
            print("📂 Loading Step 4 MongoDB format data...")
            
            if not os.path.exists(self.DATA_FILE):
                print(f"❌ Data file not found: {self.DATA_FILE}")
                return None
                
            with open(self.DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            print(f"✅ Data loaded successfully")
            print(f"📊 Collections found: {list(data.keys())}")
            return data
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def connect_to_atlas(self):
        """Connect to MongoDB Atlas"""
        try:
            print("🌐 Connecting to MongoDB Atlas...")
            
            # Check if connection string is configured
            if "<password>" in self.ATLAS_URI or "xxxxx" in self.ATLAS_URI:
                print("❌ Please configure your Atlas connection string first!")
                print("📝 Edit this file and replace ATLAS_URI with your actual connection string")
                return False
            
            # Create client with timeout settings
            self.client = MongoClient(
                self.ATLAS_URI,
                serverSelectionTimeoutMS=30000,  # 30 second timeout
                socketTimeoutMS=20000,
                connectTimeoutMS=20000,
                maxPoolSize=1
            )
            
            # Test connection
            self.client.server_info()
            
            # Get database
            self.db = self.client[self.DATABASE_NAME]
            
            print(f"✅ Connected to MongoDB Atlas successfully")
            print(f"🗄️  Database: {self.DATABASE_NAME}")
            
            return True
            
        except ServerSelectionTimeoutError:
            print("❌ Connection timeout - Check your network and Atlas configuration")
            print("💡 Make sure:")
            print("   - IP address is whitelisted (0.0.0.0/0 for public access)")
            print("   - Username/password are correct")
            print("   - Cluster is running")
            return False
            
        except ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB Atlas: {e}")
            return False
            
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def create_collections_and_indexes(self):
        """Create collections with proper indexes"""
        try:
            print("📚 Creating collections and indexes...")
            
            # Collection configurations
            collections_config = {
                "agencies": [
                    ("agencyId", 1),
                    ("name", 1)
                ],
                "agents": [
                    ("agentId", 1),
                    ("agencyId", 1),
                    ("email", 1)
                ],
                "properties": [
                    ("agencyId", 1),
                    ("address.location", "2dsphere"),
                    ("propertyType", 1),
                    ("status", 1)
                ],
                "images": [
                    ("propertyId", 1),
                    ("agencyId", 1),
                    ("order", 1)
                ],
                "schools": [
                    ("educationLevel", 1),
                    ("type", 1),
                    ("distance", 1)
                ]
            }
            
            for collection_name, indexes in collections_config.items():
                # Create collection if not exists
                if collection_name not in self.db.list_collection_names():
                    self.db.create_collection(collection_name)
                
                collection = self.db[collection_name]
                
                # Create indexes
                for index_spec in indexes:
                    if isinstance(index_spec, tuple) and len(index_spec) == 2:
                        field, order = index_spec
                        if order == "2dsphere":
                            collection.create_index([(field, "2dsphere")])
                        else:
                            collection.create_index([(field, order)])
                
                print(f"✅ Collection '{collection_name}' ready with indexes")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating collections: {e}")
            return False
    
    def import_data(self, data):
        """Import data to Atlas collections"""
        try:
            print("📤 Importing data to MongoDB Atlas...")
            
            total_imported = 0
            
            # Import each collection
            for collection_name, documents in data.items():
                if collection_name == "metadata":
                    continue  # Skip metadata
                
                if not documents:
                    print(f"⚠️  No documents to import for {collection_name}")
                    continue
                
                collection = self.db[collection_name]
                
                # Clear existing data
                collection.delete_many({})
                
                # Fix geo coordinates format for properties
                if collection_name == "properties":
                    documents = self._fix_geo_coordinates(documents)
                
                # Insert documents
                if isinstance(documents, list):
                    result = collection.insert_many(documents)
                    count = len(result.inserted_ids)
                else:
                    result = collection.insert_one(documents)
                    count = 1
                
                total_imported += count
                print(f"✅ Imported {count} documents into '{collection_name}'")
            
            print(f"🎉 Total documents imported: {total_imported}")
            return True
            
        except Exception as e:
            print(f"❌ Error importing data: {e}")
            return False
    
    def _fix_geo_coordinates(self, documents):
        """Fix geo coordinates format for MongoDB 2dsphere index"""
        fixed_documents = []
        
        for doc in documents:
            if isinstance(doc, dict):
                # Convert coordinates to GeoJSON format
                if "address" in doc and "coordinates" in doc["address"]:
                    coords = doc["address"]["coordinates"]
                    if "lat" in coords and "lng" in coords:
                        # Convert to GeoJSON Point format
                        doc["address"]["location"] = {
                            "type": "Point",
                            "coordinates": [coords["lng"], coords["lat"]]  # [longitude, latitude]
                        }
                        # Remove original coordinates to avoid conflicts
                        del doc["address"]["coordinates"]
                
                fixed_documents.append(doc)
            else:
                fixed_documents.append(doc)
        
        return fixed_documents
    
    def verify_import(self):
        """Verify data was imported correctly"""
        try:
            print("🔍 Verifying import...")
            
            collections = ["agencies", "agents", "properties", "images", "schools"]
            total_docs = 0
            
            for collection_name in collections:
                collection = self.db[collection_name]
                count = collection.count_documents({})
                total_docs += count
                print(f"📊 {collection_name}: {count} documents")
            
            print(f"✅ Total documents in Atlas: {total_docs}")
            
            # Sample queries
            print("\n🔍 Sample data verification:")
            
            # Check agency
            agency = self.db.agencies.find_one()
            if agency:
                print(f"📍 Agency: {agency.get('name', 'N/A')}")
            
            # Check property
            property_doc = self.db.properties.find_one()
            if property_doc:
                print(f"🏠 Property: {property_doc.get('title', 'N/A')}")
            
            # Check images count
            images_count = self.db.images.count_documents({})
            print(f"📸 Images: {images_count} total")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during verification: {e}")
            return False
    
    def generate_connection_info(self):
        """Generate connection info for sharing"""
        try:
            print("\n🌐 CONNECTION INFO FOR SHARING:")
            print("=" * 50)
            
            # Atlas cluster info
            cluster_name = self.ATLAS_URI.split("@")[1].split(".")[0] if "@" in self.ATLAS_URI else "Unknown"
            
            print(f"🗄️  Database: {self.DATABASE_NAME}")
            print(f"☁️  Cluster: {cluster_name}")
            print(f"📊 Collections: agencies, agents, properties, images, schools")
            
            # Connection methods
            print(f"\n📱 ACCESS METHODS:")
            print(f"1. MongoDB Compass: {self.ATLAS_URI}")
            print(f"2. Python: pymongo.MongoClient('{self.ATLAS_URI}')")
            print(f"3. Atlas Web UI: https://cloud.mongodb.com/")
            
            # Sample queries
            print(f"\n💡 SAMPLE QUERIES:")
            print(f"- db.properties.find()")
            print(f"- db.agencies.find()")
            print(f"- db.images.find().limit(5)")
            print(f"- db.schools.find({{'educationLevel': 'primary'}})")
            
            return True
            
        except Exception as e:
            print(f"❌ Error generating connection info: {e}")
            return False
    
    def close_connection(self):
        """Close Atlas connection"""
        if self.client:
            self.client.close()
            print("✅ Atlas connection closed")

def main():
    """Main execution function"""
    print("🌐 MONGODB ATLAS IMPORT")
    print("=" * 50)
    
    importer = AtlasImporter()
    
    try:
        # Load data
        data = importer.load_data()
        if not data:
            return False
        
        # Connect to Atlas
        if not importer.connect_to_atlas():
            return False
        
        # Create collections and indexes
        if not importer.create_collections_and_indexes():
            return False
        
        # Import data
        if not importer.import_data(data):
            return False
        
        # Verify import
        if not importer.verify_import():
            return False
        
        # Generate sharing info
        importer.generate_connection_info()
        
        print("\n🎉 ATLAS IMPORT COMPLETED SUCCESSFULLY!")
        print("💫 Database is now live and accessible to everyone!")
        
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️  Import cancelled by user")
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False
        
    finally:
        importer.close_connection()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
