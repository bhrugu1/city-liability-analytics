"""
Chicago City Liability Analysis - Data Simulation Module

This module generates realistic simulated liability claims data specifically for the 
City of Chicago municipal analysis. It creates comprehensive claim records with 
Chicago-specific incident types, city divisions, geographic coordinates within 
Chicago metropolitan boundaries, and financial information to support Chicago 
municipal risk management and analytical modeling.

Geographic Focus: Chicago, Illinois metropolitan area
Coverage: 7 major Chicago zones avoiding Lake Michigan and water bodies

Author: Municipal Data Analysis Team
Date: July 2025
Project: Chicago City Liability Analytics Platform
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker for generating realistic fake data
fake = Faker()

def generate_claims_data(num_records=50000):
    """
    Generate simulated Chicago municipal liability claims data for analysis.
    
    This function creates realistic Chicago liability claim records with the following 
    Chicago-specific features:
    - Chicago municipal incident types (Slip & Fall, Vehicle Damage, etc.)
    - Chicago city divisions (Public Works, Parks & Recreation, Fire Services, etc.)
    - Contextually appropriate alleged causes for Chicago municipal context
    - Geographic coordinates limited to Chicago land areas (avoiding Lake Michigan)
    - Financial data reflecting Chicago municipal settlement patterns
    - Chicago claim status tracking and processing workflow
    
    Geographic Coverage:
    - Downtown Loop, North Side, South Side, West Side Chicago areas
    - Northwest and Southwest Chicago suburbs
    - Western suburbs (Oak Park, Cicero area)
    
    Args:
        num_records (int): Number of Chicago claim records to generate (default: 50,000)
    
    Returns:
        pandas.DataFrame: Comprehensive Chicago liability claims dataset
    """
    
    # Initialize data collection list
    data = []
    
    # Define incident types that commonly occur in municipal liability
    incident_types = [
        'Slip & Fall',           # Pedestrian accidents on city property
        'Vehicle Damage',        # Road-related vehicle incidents  
        'Property Damage',       # Damage to private property by city operations
        'Environmental',         # Pollution, drainage, environmental issues
        'Personal Injury',       # Physical injuries on city property
        'Equipment Malfunction'  # City equipment causing incidents
    ]
    
    # Define city divisions typically involved in liability claims
    city_divisions = [
        'Public Works',          # Infrastructure maintenance and construction
        'Parks & Recreation',    # Public parks, recreational facilities
        'Transit',              # Public transportation operations
        'By-law Enforcement',   # Municipal law enforcement activities
        'Water & Wastewater',   # Utility infrastructure and services
        'Fire Services'         # Emergency response and fire safety
    ]
    
    # Define context-appropriate alleged causes for each incident type
    # This creates realistic relationships between incident types and their causes
    alleged_causes = {
        'Slip & Fall': [
            'Uneven Sidewalk',    # Common infrastructure issue
            'Icy Pavement',       # Weather-related maintenance issue
            'Poor Lighting',      # Safety infrastructure deficiency
            'Obstruction'         # Maintenance or placement issue
        ],
        'Vehicle Damage': [
            'Pothole',            # Road maintenance issue
            'Debris on Road',     # Cleanliness/maintenance issue
            'Faulty Traffic Signal', # Infrastructure malfunction
            'Poor Road Design'    # Engineering/design issue
        ],
        'Property Damage': [
            'Water Main Break',   # Infrastructure failure
            'Tree Fall',          # Natural/maintenance issue
            'Construction Error', # Operational oversight
            'Sewer Backup'        # Infrastructure/maintenance issue
        ],
        'Environmental': [
            'Pollution Spill',    # Environmental management issue
            'Drainage Issue',     # Infrastructure/design problem
            'Waste Management Oversight' # Operational issue
        ],
        'Personal Injury': [
            'Unsafe Equipment',   # Maintenance/safety issue
            'Lack of Supervision', # Operational oversight
            'Inadequate Warning'  # Safety protocol issue
        ],
        'Equipment Malfunction': [
            'Poor Maintenance',   # Maintenance oversight
            'Outdated Equipment', # Capital investment issue
            'Operator Error'      # Training/supervision issue
        ]
    }
    
    # Define possible claim resolution statuses
    claim_statuses = [
        'Open',                 # Claim still being processed
        'Closed - Settled',     # Resolved with payment
        'Closed - Denied',      # Rejected without payment
        'Closed - Withdrawn'    # Claimant withdrew claim
    ]

    # Define date range for historical claim data (10 years)
    start_date = datetime(2015, 1, 1)
    end_date = datetime(2024, 12, 31)

    # Generate individual claim records
    for i in range(num_records):
        # Generate realistic incident date within specified range
        incident_date = start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )
        
        # Claim filing typically occurs 0-90 days after incident
        claim_filed_date = incident_date + timedelta(
            days=random.randint(0, 90)
        )

        # Select incident type and ensure contextually appropriate cause
        incident_type = random.choice(incident_types)
        division = random.choice(city_divisions)
        
        # Get appropriate causes for the selected incident type
        cause_options = alleged_causes.get(
            incident_type, 
            ['General Oversight', 'Unspecified Issue']  # Fallback options
        )
        cause = random.choice(cause_options)

        # Generate realistic financial data
        # 70% of claims result in some settlement (realistic municipal rate)
        if random.random() < 0.7:
            # Settlement amounts vary widely based on incident severity
            settlement_amount = round(random.uniform(500, 500000), 2)
            # Legal costs typically correlate with settlement complexity
            legal_costs = round(random.uniform(100, 50000), 2)
        else:
            # No financial impact for denied/withdrawn claims
            settlement_amount = 0
            legal_costs = 0

        # Assign claim status with logical consistency
        claim_status = random.choice(claim_statuses)
        
        # Ensure data consistency between settlement amount and status
        if settlement_amount == 0 and claim_status == 'Closed - Settled':
            # If no settlement, status should reflect that
            claim_status = random.choice(['Closed - Denied', 'Closed - Withdrawn'])
        elif settlement_amount > 0 and claim_status in ['Closed - Denied', 'Closed - Withdrawn']:
            # If there's a settlement, status should reflect payment
            claim_status = 'Closed - Settled'

        # Generate detailed allegation text using realistic language
        allegation_detail = (
            f"Claim related to {cause} in {division}. "
            f"Incident involved {incident_type}. "
            f"{fake.sentence()} "  # Random descriptive sentence
            f"The alleged issue was {cause.lower()}."
        )

        # Generate realistic geospatial data within Chicago metropolitan land area
        # Using multiple land-based zones to avoid Lake Michigan and other water bodies
        
        # Define safe land-based coordinate ranges for Chicago metropolitan area
        # These zones avoid Lake Michigan (east) and ensure all coordinates are on land
        land_zones = [
            # Downtown/Loop area (guaranteed land)
            {'lat_min': 41.8700, 'lat_max': 41.8900, 'lng_min': -87.6400, 'lng_max': -87.6200},
            
            # North Side (Lincoln Park, Lakeview - but staying west of lakefront)
            {'lat_min': 41.9000, 'lat_max': 41.9600, 'lng_min': -87.7000, 'lng_max': -87.6300},
            
            # South Side (Bronzeville, Hyde Park area)
            {'lat_min': 41.8000, 'lat_max': 41.8600, 'lng_min': -87.6800, 'lng_max': -87.6000},
            
            # West Side (Austin, Garfield Park area)
            {'lat_min': 41.8600, 'lat_max': 41.9200, 'lng_min': -87.8000, 'lng_max': -87.7000},
            
            # Southwest (Midway area)
            {'lat_min': 41.7600, 'lat_max': 41.8200, 'lng_min': -87.7500, 'lng_max': -87.6800},
            
            # Northwest suburbs (O'Hare area)
            {'lat_min': 41.9400, 'lat_max': 42.0200, 'lng_min': -87.9000, 'lng_max': -87.8000},
            
            # Western suburbs (Oak Park, Cicero area)
            {'lat_min': 41.8500, 'lat_max': 41.9000, 'lng_min': -87.8500, 'lng_max': -87.7800}
        ]
        
        # Randomly select a land zone for this incident
        selected_zone = random.choice(land_zones)
        
        # Generate coordinates within the selected land zone
        incident_latitude = random.uniform(selected_zone['lat_min'], selected_zone['lat_max'])
        incident_longitude = random.uniform(selected_zone['lng_min'], selected_zone['lng_max'])

        # Compile complete claim record
        data.append({
            'Claim_ID': f'CLAIM-{i+1:06d}',                    # Unique identifier
            'Date_of_Incident': incident_date.strftime('%Y-%m-%d'),     # ISO date format
            'Date_Claim_Filed': claim_filed_date.strftime('%Y-%m-%d'),  # ISO date format
            'Incident_Type': incident_type,                    # Categorization
            'Alleged_Cause': cause,                           # Specific cause
            'City_Division_Involved': division,               # Responsible department
            'Location_Details': f"{fake.street_address()}, Chicago, IL {fake.postcode()}", # Geographic info
            'Latitude': round(incident_latitude, 6),          # City-specific coordinates
            'Longitude': round(incident_longitude, 6),        # City-specific coordinates
            'Claim_Status': claim_status,                     # Processing status
            'Settlement_Amount': settlement_amount,           # Financial impact
            'Legal_Costs': legal_costs,                      # Additional costs
            'Allegation_Details': allegation_detail          # Full description
        })

    # Convert to DataFrame for analysis
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    """
    Main execution block for data generation.
    
    This block handles:
    1. Directory creation for data storage
    2. Data generation with specified parameters
    3. Export to CSV format for further processing
    4. User feedback on completion
    """
    
    # Ensure the data/raw directory exists for output
    import os
    data_dir = os.path.join('..', '..', 'data', 'raw')
    os.makedirs(data_dir, exist_ok=True)

    # Generate comprehensive Chicago claims dataset
    print("Generating simulated Chicago liability claims data...")
    df_claims = generate_claims_data(num_records=75000)  # Generate 75,000 Chicago records
    
    # Save to CSV for further processing
    csv_path = os.path.join(data_dir, 'simulated_claims.csv')
    df_claims.to_csv(csv_path, index=False)
    
    # Provide completion feedback
    print(f"✅ Generated {len(df_claims)} simulated claims data and saved to {csv_path}")
    print(f"📊 Dataset includes {df_claims['Incident_Type'].nunique()} incident types")
    print(f"🏛️ Covers {df_claims['City_Division_Involved'].nunique()} city divisions")
    print(f"💰 Total simulated exposure: ${df_claims['Settlement_Amount'].sum() + df_claims['Legal_Costs'].sum():,.2f}")
