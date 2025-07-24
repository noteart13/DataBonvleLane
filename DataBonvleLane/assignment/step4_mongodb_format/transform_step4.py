"""
STEP 4: MONGODB FORMAT
Get right format for MongoDB insertion từ Step 3 data
"""

import json
from pathlib import Path
from datetime import datetime
import uuid

class Step4MongoTransformer:
    def __init__(self, step3_file_path):
        self.step3_file_path = step3_file_path
        self.step3_data = None
        
    def load_step3_data(self):
        """Load dữ liệu từ Step 3"""
        try:
            with open(self.step3_file_path, 'r', encoding='utf-8') as f:
                self.step3_data = json.load(f)
            print("✅ Step 3 data loaded successfully")
            return True
        except Exception as e:
            print(f"❌ Error loading Step 3 data: {e}")
            return False
    
    def generate_object_id(self):
        """Generate MongoDB-style ObjectId string"""
        # Generate a simple ObjectId-like string (24 hex characters)
        return str(uuid.uuid4()).replace('-', '')[:24]
    
    def create_agency_document(self):
        """Tạo MongoDB document cho Agency collection"""
        try:
            agency_data = self.step3_data.get('agency', {})
            
            agency_doc = {
                '_id': self.generate_object_id(),
                'agencyId': agency_data.get('agencyId'),
                'name': agency_data.get('name'),
                'contactDetails': agency_data.get('contactDetails'),
                'website': agency_data.get('website'),
                'profileUrl': agency_data.get('profileUrl'),
                'isArchived': agency_data.get('isArchived', False),
                'branding': {
                    'banner': agency_data.get('banner'),
                    'logo': agency_data.get('logo'),
                    'logoSmall': agency_data.get('logoSmall')
                },
                'createdAt': datetime.now().isoformat(),
                'updatedAt': datetime.now().isoformat()
            }
            
            print("✅ Agency document created")
            return agency_doc
            
        except Exception as e:
            print(f"❌ Error creating agency document: {e}")
            return {}
    
    def create_agents_documents(self):
        """Tạo MongoDB documents cho Agents collection"""
        try:
            agents_data = self.step3_data.get('agents', [])
            
            agents_docs = []
            for agent in agents_data:
                agent_doc = {
                    '_id': self.generate_object_id(),
                    'agentId': agent.get('agentId'),
                    'firstName': agent.get('firstName'),
                    'lastName': agent.get('lastName'),
                    'email': agent.get('email'),
                    'phoneNumber': agent.get('phoneNumber'),
                    'photo': agent.get('photo'),
                    'profileUrl': agent.get('profileUrl'),
                    'isActiveProfilePage': agent.get('isActiveProfilePage', True),
                    'agencyId': self.step3_data.get('agency', {}).get('agencyId'),
                    'createdAt': datetime.now().isoformat(),
                    'updatedAt': datetime.now().isoformat()
                }
                agents_docs.append(agent_doc)
            
            print(f"✅ {len(agents_docs)} agent documents created")
            return agents_docs
            
        except Exception as e:
            print(f"❌ Error creating agent documents: {e}")
            return []
    
    def create_property_document(self):
        """Tạo MongoDB document cho Properties collection"""
        try:
            pfs_data = self.step3_data.get('propertyforsale', {})
            
            property_doc = {
                '_id': self.generate_object_id(),
                'title': pfs_data.get('title'),
                'description': pfs_data.get('description'),
                'propertyType': pfs_data.get('propertyType'),
                'address': {
                    'street': pfs_data.get('street'),
                    'suburb': pfs_data.get('suburb'),
                    'state': pfs_data.get('state'),
                    'postcode': pfs_data.get('postcode'),
                    'city': pfs_data.get('city'),
                    'coordinates': pfs_data.get('coordinates', {})
                },
                'features': {
                    'bedrooms': pfs_data.get('bed'),
                    'bathrooms': pfs_data.get('bath'),
                    'garage': pfs_data.get('features', {}).get('garage'),
                    'parking': pfs_data.get('features', {}).get('parking'),
                    'area': pfs_data.get('area', {}),
                    'architecturalStyle': pfs_data.get('architecturalStyle'),
                    'constructionYear': pfs_data.get('constructionYear'),
                    'structuralRemodelYear': pfs_data.get('structuralRemodelYear'),
                    'appliances': pfs_data.get('features', {}).get('appliances'),
                    'indoorFeatures': pfs_data.get('features', {}).get('indoorFeatures'),
                    'outdoorAmenities': pfs_data.get('features', {}).get('outdoorAmenities')
                },
                'pricing': pfs_data.get('pricing', {}),
                'expectedPrice': pfs_data.get('expectedPrice'),
                'listingOption': pfs_data.get('listingOption'),
                'status': pfs_data.get('status'),
                'stakeHolder': pfs_data.get('stakeHolder'),
                'published': pfs_data.get('published', False),
                'recommended': pfs_data.get('recommended', False),
                'slug': pfs_data.get('slug'),
                'url': pfs_data.get('url'),
                'historySale': pfs_data.get('historySale', {}),
                'contactInfo': pfs_data.get('contactInfo', []),
                'agencyId': self.step3_data.get('agency', {}).get('agencyId'),
                'createdAt': datetime.now().isoformat(),
                'updatedAt': datetime.now().isoformat()
            }
            
            print("✅ Property document created")
            return property_doc
            
        except Exception as e:
            print(f"❌ Error creating property document: {e}")
            return {}
    
    def create_images_documents(self):
        """Tạo MongoDB documents cho Images collection"""
        try:
            images_data = self.step3_data.get('images', [])
            property_id = self.generate_object_id()  # Sẽ link với property
            
            images_docs = []
            for idx, image in enumerate(images_data):
                image_doc = {
                    '_id': self.generate_object_id(),
                    'url': image.get('url'),
                    'category': image.get('category'),
                    'star': image.get('star', False),
                    'order': idx + 1,
                    'propertyId': property_id,
                    'agencyId': self.step3_data.get('agency', {}).get('agencyId'),
                    'createdAt': datetime.now().isoformat(),
                    'updatedAt': datetime.now().isoformat()
                }
                images_docs.append(image_doc)
            
            print(f"✅ {len(images_docs)} image documents created")
            return images_docs
            
        except Exception as e:
            print(f"❌ Error creating image documents: {e}")
            return []
    
    def create_schools_documents(self):
        """Tạo MongoDB documents cho Schools collection"""
        try:
            schools_data = self.step3_data.get('schools', [])
            
            schools_docs = []
            for school in schools_data:
                school_doc = {
                    '_id': self.generate_object_id(),
                    'name': school.get('name'),
                    'address': school.get('address'),
                    'postCode': school.get('postCode'),
                    'state': school.get('state'),
                    'educationLevel': school.get('educationLevel'),
                    'type': school.get('type'),
                    'gender': school.get('gender'),
                    'year': school.get('year'),
                    'status': school.get('status'),
                    'url': school.get('url'),
                    'distance': school.get('distance'),
                    'domainSeoUrlSlug': school.get('domainSeoUrlSlug'),
                    'createdAt': datetime.now().isoformat(),
                    'updatedAt': datetime.now().isoformat()
                }
                
                # Add optional fields
                if 'isRadiusResult' in school:
                    school_doc['isRadiusResult'] = school['isRadiusResult']
                
                schools_docs.append(school_doc)
            
            print(f"✅ {len(schools_docs)} school documents created")
            return schools_docs
            
        except Exception as e:
            print(f"❌ Error creating school documents: {e}")
            return []
    
    def create_mongodb_collections(self):
        """Tạo tất cả MongoDB collections"""
        try:
            # Create all collection documents
            agency_doc = self.create_agency_document()
            agents_docs = self.create_agents_documents()
            property_doc = self.create_property_document()
            images_docs = self.create_images_documents()
            schools_docs = self.create_schools_documents()
            
            # Organize into collections structure
            mongodb_collections = {
                'agencies': [agency_doc] if agency_doc else [],
                'agents': agents_docs,
                'properties': [property_doc] if property_doc else [],
                'images': images_docs,
                'schools': schools_docs,
                'metadata': {
                    'totalDocuments': (
                        len([agency_doc] if agency_doc else []) +
                        len(agents_docs) +
                        len([property_doc] if property_doc else []) +
                        len(images_docs) +
                        len(schools_docs)
                    ),
                    'collections': {
                        'agencies': len([agency_doc] if agency_doc else []),
                        'agents': len(agents_docs),
                        'properties': len([property_doc] if property_doc else []),
                        'images': len(images_docs),
                        'schools': len(schools_docs)
                    },
                    'generatedAt': datetime.now().isoformat(),
                    'sourceData': 'Step 3 right format'
                }
            }
            
            print("✅ All MongoDB collections created")
            return mongodb_collections
            
        except Exception as e:
            print(f"❌ Error creating MongoDB collections: {e}")
            return {}
    
    def save_mongodb_format(self, output_file):
        """Save MongoDB format data"""
        try:
            mongodb_data = self.create_mongodb_collections()
            
            if mongodb_data:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(mongodb_data, f, indent=2, ensure_ascii=False)
                
                print(f"✅ MongoDB format saved to {output_file}")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error saving MongoDB format: {e}")
            return False

def main():
    """Main function cho Step 4 MongoDB transformation"""
    print("🗄️  STEP 4: MONGODB FORMAT")
    print("="*40)
    
    # Paths
    step3_file = Path("../step3_right_format/step3_right_format.json")
    output_file = Path("step4_mongodb_format.json")
    
    # Check input file exists
    if not step3_file.exists():
        print(f"❌ Step 3 file not found: {step3_file}")
        return
    
    # Create transformer
    transformer = Step4MongoTransformer(step3_file)
    
    # Run transformation
    if transformer.load_step3_data():
        if transformer.save_mongodb_format(output_file):
            print("\n🎉 STEP 4 MONGODB TRANSFORMATION COMPLETED!")
            print(f"📁 Output: {output_file}")
            
            # Show summary
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print("\n📊 MONGODB COLLECTIONS SUMMARY:")
            metadata = data.get('metadata', {})
            collections = metadata.get('collections', {})
            
            for collection_name, count in collections.items():
                print(f"  ✅ {collection_name}: {count} documents")
            
            print(f"\n📈 TOTAL: {metadata.get('totalDocuments', 0)} documents")
            print("✅ Ready for MongoDB insertion!")
            
        else:
            print("\n❌ Failed to save MongoDB format")
    else:
        print("\n❌ Failed to load Step 3 data")

if __name__ == "__main__":
    main()
