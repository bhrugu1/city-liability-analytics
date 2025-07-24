import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

def generate_claims_data(num_records=50000):
    data = []
    incident_types = ['Slip & Fall', 'Vehicle Damage', 'Property Damage', 'Environmental', 'Personal Injury', 'Equipment Malfunction']
    city_divisions = ['Public Works', 'Parks & Recreation', 'Transit', 'By-law Enforcement', 'Water & Wastewater', 'Fire Services']
    alleged_causes = {
        'Slip & Fall': ['Uneven Sidewalk', 'Icy Pavement', 'Poor Lighting', 'Obstruction'],
        'Vehicle Damage': ['Pothole', 'Debris on Road', 'Faulty Traffic Signal', 'Poor Road Design'],
        'Property Damage': ['Water Main Break', 'Tree Fall', 'Construction Error', 'Sewer Backup'],
        'Environmental': ['Pollution Spill', 'Drainage Issue', 'Waste Management Oversight'],
        'Personal Injury': ['Unsafe Equipment', 'Lack of Supervision', 'Inadequate Warning'],
        'Equipment Malfunction': ['Poor Maintenance', 'Outdated Equipment', 'Operator Error']
    }
    claim_statuses = ['Open', 'Closed - Settled', 'Closed - Denied', 'Closed - Withdrawn']

    start_date = datetime(2015, 1, 1)
    end_date = datetime(2024, 12, 31)

    for i in range(num_records):
        incident_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        claim_filed_date = incident_date + timedelta(days=random.randint(0, 90)) # Claims filed within 90 days

        incident_type = random.choice(incident_types)
        division = random.choice(city_divisions)
        # Ensure 'cause' is relevant to 'incident_type'
        cause_options = alleged_causes.get(incident_type, ['General Oversight', 'Unspecified Issue'])
        cause = random.choice(cause_options)

        # Simulate settlement amount and legal costs
        settlement_amount = round(random.uniform(500, 500000), 2) if random.random() < 0.7 else 0 # 70% of claims result in settlement
        legal_costs = round(random.uniform(100, 50000), 2) if settlement_amount > 0 else 0

        claim_status = random.choice(claim_statuses)
        # Ensure consistency between settlement amount and status
        if settlement_amount == 0 and claim_status == 'Closed - Settled':
            claim_status = random.choice(['Closed - Denied', 'Closed - Withdrawn'])
        elif settlement_amount > 0 and claim_status in ['Closed - Denied', 'Closed - Withdrawn']:
            claim_status = 'Closed - Settled'


        allegation_detail = f"Claim related to {cause} in {division}. Incident involved {incident_type}. {fake.sentence()} The alleged issue was {cause.lower()}."

        data.append({
            'Claim_ID': f'CLAIM-{i+1:06d}',
            'Date_of_Incident': incident_date.strftime('%Y-%m-%d'),
            'Date_Claim_Filed': claim_filed_date.strftime('%Y-%m-%d'),
            'Incident_Type': incident_type,
            'Alleged_Cause': cause,
            'City_Division_Involved': division,
            'Location_Details': f"{fake.street_address()}, {fake.city()}, {fake.postcode()}",
            'Latitude': fake.latitude(),
            'Longitude': fake.longitude(),
            'Claim_Status': claim_status,
            'Settlement_Amount': settlement_amount,
            'Legal_Costs': legal_costs,
            'Allegation_Details': allegation_detail
        })

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    # Ensure the data/raw directory exists
    import os
    data_dir = os.path.join('..', '..', 'data', 'raw')
    os.makedirs(data_dir, exist_ok=True)

    df_claims = generate_claims_data(num_records=75000) # Generating 75,000 records
    csv_path = os.path.join(data_dir, 'simulated_claims.csv')
    df_claims.to_csv(csv_path, index=False)
    print(f"Generated {len(df_claims)} simulated claims data and saved to {csv_path}.")
