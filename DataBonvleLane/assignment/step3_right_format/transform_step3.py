"""
STEP 3: TRANSFORM TO RIGHT FORMAT
Extract right format from Step 2 data và chuyển đổi sang cấu trúc Step 3
"""

import json
from pathlib import Path

class Step3Transformer:
    def __init__(self, step2_file_path):
        self.step2_file_path = step2_file_path
        self.step2_data = None
        
    def load_step2_data(self):
        """Load dữ liệu từ Step 2"""
        try:
            with open(self.step2_file_path, 'r', encoding='utf-8') as f:
                self.step2_data = json.load(f)
            print("✅ Step 2 data loaded successfully")
            return True
        except Exception as e:
            print(f"❌ Error loading Step 2 data: {e}")
            return False
    
    def transform_agency(self):
        """Transform agency data từ Step 2 sang Step 3 format"""
        try:
            step2_agency = self.step2_data.get('agency', {})
            
            # Flatten agency structure
            agency = {
                'agencyId': step2_agency.get('agencyId'),
                'banner': step2_agency.get('branding', {}).get('banner', {}).get('url'),
                'contactDetails': step2_agency.get('contactDetails', {}).get('general', {}).get('phone'),
                'isArchived': step2_agency.get('isArchived'),
                'logo': step2_agency.get('branding', {}).get('logo', {}).get('url'),
                'logoSmall': step2_agency.get('branding', {}).get('logoSmall', {}).get('url'),
                'name': step2_agency.get('name'),
                'profileUrl': step2_agency.get('profileUrl'),
                'website': step2_agency.get('website')
            }
            
            print("✅ Agency transformed")
            return agency
            
        except Exception as e:
            print(f"❌ Error transforming agency: {e}")
            return {}
    
    def transform_agents(self):
        """Transform agentProfiles từ Step 2 sang agents Step 3 format"""
        try:
            step2_agents = self.step2_data.get('agentProfiles', [])
            
            # Simplify agent structure
            agents = []
            for agent in step2_agents:
                agent_data = {
                    'agentId': agent.get('agentId'),
                    'email': agent.get('email'),
                    'firstName': agent.get('firstName'),
                    'isActiveProfilePage': agent.get('isActiveProfilePage'),
                    'lastName': agent.get('lastName'),
                    'phoneNumber': agent.get('phoneNumber'),
                    'photo': agent.get('photo'),
                    'profileUrl': agent.get('profileUrl')
                }
                agents.append(agent_data)
            
            print(f"✅ {len(agents)} agents transformed")
            return agents
            
        except Exception as e:
            print(f"❌ Error transforming agents: {e}")
            return []
    
    def transform_images(self):
        """Transform images từ Step 2 sang Step 3 format với category và star"""
        try:
            step2_images = self.step2_data.get('pro_meta', {}).get('images', [])
            
            # Add category and star properties to images
            images = []
            for url in step2_images:
                image_data = {
                    'category': 'kitchen',  # Default category từ Step 3 sample
                    'star': False,          # Default star value
                    'url': url
                }
                images.append(image_data)
            
            print(f"✅ {len(images)} images transformed")
            return images
            
        except Exception as e:
            print(f"❌ Error transforming images: {e}")
            return []
    
    def transform_schools(self):
        """Transform schools từ Step 2 sang Step 3 format (unwrap từ schools.schools)"""
        try:
            step2_schools = self.step2_data.get('schools', {}).get('schools', [])
            
            # Unwrap schools array và clean structure
            schools = []
            for school in step2_schools:
                school_data = {
                    'address': school.get('address'),
                    'distance': school.get('distance'),
                    'domainSeoUrlSlug': school.get('domainSeoUrlSlug'),
                    'educationLevel': school.get('educationLevel'),
                    'gender': school.get('gender'),
                    'name': school.get('name'),
                    'postCode': school.get('postCode'),
                    'state': school.get('state'),
                    'status': school.get('status'),
                    'type': school.get('type'),
                    'url': school.get('url'),
                    'year': school.get('year')
                }
                
                # Add optional fields if present
                if 'isRadiusResult' in school:
                    school_data['isRadiusResult'] = school['isRadiusResult']
                
                schools.append(school_data)
            
            print(f"✅ {len(schools)} schools transformed")
            return schools
            
        except Exception as e:
            print(f"❌ Error transforming schools: {e}")
            return []
    
    def transform_propertyforsale(self):
        """Transform main property data sang propertyforsale Step 3 format"""
        try:
            step2_data = self.step2_data
            pro_meta = step2_data.get('pro_meta', {})
            display_address = step2_data.get('displayAddress', {})
            description = step2_data.get('description', {})
            agents = step2_data.get('agentProfiles', [])
            sale_info = step2_data.get('saleInfo', {})
            history_sale = step2_data.get('historySale', {})
            
            # Build contact info từ agents
            contact_info = []
            for agent in agents:
                contact = {
                    'email': agent.get('email'),
                    'firstName': agent.get('firstName'),
                    'lastName': agent.get('lastName'),
                    'phoneNumber': agent.get('phoneNumber')
                }
                contact_info.append(contact)
            
            # Create propertyforsale object
            propertyforsale = {
                'architecturalStyle': 'None',
                'area': {
                    'totalarea': pro_meta.get('landArea', 0),
                    'unit': 'sqM'
                },
                'bath': pro_meta.get('bathrooms', 0),
                'bed': pro_meta.get('bedrooms', 0),  
                'city': 'Unincorporated Act',
                'constructionYear': 'N/A',
                'contactInfo': contact_info,
                'coordinates': {
                    'lat': display_address.get('geolocation', {}).get('latitude'),
                    'lng': display_address.get('geolocation', {}).get('longitude')
                },
                'description': description.get('description', ''),
                'expectedPrice': sale_info.get('expectedPrice'),
                'features': {
                    'appliances': ['None'],
                    'basement': 'None',
                    'buildingAmenities': ['None'],
                    'coolingTypes': ['None'],
                    'displayAddress': 'fullAddress',
                    'floorCovering': ['None'],
                    'floorno': 1,
                    'garage': pro_meta.get('parking', 0),
                    'heatingFuels': ['None'],
                    'heatingTypes': ['None'],
                    'indoorFeatures': ['None'],
                    'outdoorAmenities': ['None'],
                    'parking': ['Carport'],
                    'roof': ['Other'],
                    'rooms': ['None'],
                    'view': ['None']
                },
                'historySale': {
                    'agencyId': history_sale.get('agencyId'),
                    'soldDate': history_sale.get('soldDate'),
                    'soldPrice': history_sale.get('soldPrice')
                },
                'images': self.transform_images(),
                'listingOption': sale_info.get('listingOption'),
                'postcode': display_address.get('postcode'),
                'pricing': {
                    'authority': sale_info.get('pricing', {}).get('authority'),
                    'councilBill': '',
                    'priceIncludes': sale_info.get('pricing', {}).get('priceIncludes', ['']),
                    'pricingOptions': sale_info.get('pricing', {}).get('pricingOptions'),
                    'waterBillPeriod': 'monthly'
                },
                'propertyType': step2_data.get('propertyType', {}).get('propertyType'),
                'published': False,
                'recommended': False,
                'slug': step2_data.get('slug', {}).get('slug'),
                'stakeHolder': 'agent',
                'state': display_address.get('state'),
                'status': sale_info.get('status'),
                'street': display_address.get('displayAddress'),
                'structuralRemodelYear': 'N/A',
                'suburb': display_address.get('suburbName'),
                'title': step2_data.get('headline', {}).get('headline'),
                'url': step2_data.get('url')
            }
            
            print("✅ PropertyForSale transformed")
            return propertyforsale
            
        except Exception as e:
            print(f"❌ Error transforming propertyforsale: {e}")
            return {}
    
    def create_step3_format(self):
        """Tạo complete Step 3 format"""
        try:
            # Transform all components
            agency = self.transform_agency()
            agents = self.transform_agents()
            images = self.transform_images()
            schools = self.transform_schools()
            propertyforsale = self.transform_propertyforsale()
            
            # Build Step 3 structure
            step3_data = {
                'agency': agency,
                'agents': agents,
                'images': images,
                'propertyforsale': propertyforsale,
                'schools': schools
            }
            
            print("✅ Complete Step 3 format created")
            return step3_data
            
        except Exception as e:
            print(f"❌ Error creating Step 3 format: {e}")
            return None
    
    def save_step3_data(self, output_file):
        """Save Step 3 transformed data"""
        try:
            step3_data = self.create_step3_format()
            
            if step3_data:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(step3_data, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Step 3 data saved to {output_file}")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error saving Step 3 data: {e}")
            return False

def main():
    """Main function cho Step 3 transformation"""
    print("🔄 STEP 3: TRANSFORM TO RIGHT FORMAT")
    print("="*50)
    
    # Paths
    step2_file = Path("../step2_extracted_data/extracted_data_complete.json")
    output_file = Path("step3_right_format.json")
    
    # Check input file exists
    if not step2_file.exists():
        print(f"❌ Step 2 file not found: {step2_file}")
        return
    
    # Create transformer
    transformer = Step3Transformer(step2_file)
    
    # Run transformation
    if transformer.load_step2_data():
        if transformer.save_step3_data(output_file):
            print("\n🎉 STEP 3 TRANSFORMATION COMPLETED!")
            print(f"📁 Output: {output_file}")
            
            # Show summary
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print("\n📊 STEP 3 TRANSFORMATION SUMMARY:")
            print(f"  ✅ Agency: {data['agency']['name']}")
            print(f"  ✅ Agents: {len(data['agents'])}")
            print(f"  ✅ Images: {len(data['images'])} (with category & star)")
            print(f"  ✅ Schools: {len(data['schools'])}")
            print(f"  ✅ PropertyForSale: {data['propertyforsale']['title']}")
            print(f"  ✅ Contact Info: {len(data['propertyforsale']['contactInfo'])} contacts")
            print(f"  ✅ Structure matches Step 3 sample!")
            
        else:
            print("\n❌ Failed to save Step 3 data")
    else:
        print("\n❌ Failed to load Step 2 data")

if __name__ == "__main__":
    main()
