import pandas as pd
import sqlite3
import re
from nltk.corpus import stopwords
from collections import Counter
import spacy
import folium
import plotly.express as px
import os

# Download NLTK stopwords if not already downloaded
# import nltk
# nltk.download('stopwords')

# Load spaCy model
# If you get an OSError, run this command in your terminal: python -m spacy download en_core_web_sm
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("SpaCy model 'en_core_web_sm' not found.")
    print("Please run 'python -m spacy download en_core_web_sm' in your terminal.")
    exit()

stop_words = set(stopwords.words('english'))

def clean_text(text):
    """Cleans text by lowercasing, removing non-alphabetic chars, and stop words."""
    if pd.isna(text): # Handle NaN values
        return ""
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text) # Remove non-alphabetic characters
    text = ' '.join([word for word in text.split() if word not in stop_words and len(word) > 1]) # Remove single chars too
    return text

def perform_root_cause_analysis(db_path):
    # Ensure the output directory exists for saving maps
    output_dir = os.path.join('..', '..', 'output')
    os.makedirs(output_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT Claim_ID, Allegation_Details, Incident_Type, City_Division_Involved, (Settlement_Amount + Legal_Costs) AS Total_Loss, Latitude, Longitude FROM claims", conn)
    except Exception as e:
        print(f"Error reading data from database: {e}")
        conn.close()
        return
    finally:
        conn.close()

    # Clean the allegation details
    df['Cleaned_Allegation_Details'] = df['Allegation_Details'].apply(clean_text)

    print("\nPerforming Root Cause Analysis...")

    # Keyword Extraction
    all_words = ' '.join(df['Cleaned_Allegation_Details']).split()
    word_counts = Counter(all_words)
    print("\nTop 30 most frequent words in allegations (after cleaning):")
    for word, count in word_counts.most_common(30):
        print(f"- {word}: {count}")

    # Identify specific operational oversights using a predefined list of keywords
    # This is a simple keyword matching approach. For more advanced, consider N-grams or pre-trained NLP models.
    oversight_keywords = [
        'inspection', 'repair', 'training', 'signage', 'maintenance', 'delay',
        'neglect', 'faulty', 'poor', 'inadequate', 'missing', 'broken',
        'debris', 'pothole', 'uneven', 'icy', 'spill', 'defect', 'supervision'
    ]
    df['Identified_Oversights'] = df['Cleaned_Allegation_Details'].apply(
        lambda text: [kw for kw in oversight_keywords if kw in text]
    )

    # Filter claims where at least one oversight keyword was identified
    df_oversights = df[df['Identified_Oversights'].apply(len) > 0].copy() # Use .copy() to avoid SettingWithCopyWarning

    print(f"\nFound {len(df_oversights)} claims with identified operational oversights.")
    print("Sample claims with identified oversights:")
    print(df_oversights[['Claim_ID', 'Incident_Type', 'City_Division_Involved', 'Identified_Oversights', 'Total_Loss']].head())

    # Aggregate total loss by identified oversight keywords
    oversight_loss_data = []
    for index, row in df_oversights.iterrows():
        for oversight in row['Identified_Oversights']:
            oversight_loss_data.append({'Oversight': oversight, 'Total_Loss': row['Total_Loss']})
    df_oversight_loss = pd.DataFrame(oversight_loss_data)

    if not df_oversight_loss.empty:
        total_loss_by_oversight = df_oversight_loss.groupby('Oversight')['Total_Loss'].sum().sort_values(ascending=False).reset_index()
        print("\nTotal Loss associated with top 10 identified oversights:")
        print(total_loss_by_oversight.head(10))

        # Plotting top oversights by total loss
        fig_oversight_loss = px.bar(total_loss_by_oversight.head(10), x='Oversight', y='Total_Loss',
                                    title='Top 10 Operational Oversights by Associated Total Loss',
                                    labels={'Oversight': 'Identified Oversight', 'Total_Loss': 'Total Loss Amount ($)'},
                                    color='Total_Loss', color_continuous_scale=px.colors.sequential.OrRd,
                                    template='plotly_white')
        fig_oversight_loss.write_html(os.path.join(output_dir, "top_oversights_by_loss.html"))
        print(f"Saved: {os.path.join(output_dir, 'top_oversights_by_loss.html')}")
    else:
        print("\nNo significant oversights identified or data for oversight analysis is empty.")


    # Geospatial Analysis for high-loss claims
    # Filter out rows with invalid lat/lon
    df_valid_geo = df.dropna(subset=['Latitude', 'Longitude'])

    if not df_valid_geo.empty:
        map_center = [df_valid_geo['Latitude'].mean(), df_valid_geo['Longitude'].mean()]
        m = folium.Map(location=map_center, zoom_start=12)

        # Plot top 200 highest loss claims on the map
        for idx, row in df_valid_geo.nlargest(200, 'Total_Loss').iterrows():
            if pd.notna(row['Latitude']) and pd.notna(row['Longitude']): # Final check for valid coordinates
                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    popup=f"<b>Claim ID:</b> {row['Claim_ID']}<br>"
                          f"<b>Type:</b> {row['Incident_Type']}<br>"
                          f"<b>Division:</b> {row['City_Division_Involved']}<br>"
                          f"<b>Loss:</b> ${row['Total_Loss']:.2f}<br>"
                          f"<b>Details:</b> {row['Allegation_Details']}",
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(m)
        map_filename = os.path.join(output_dir, "high_loss_claims_map.html")
        m.save(map_filename)
        print(f"\nGeospatial map of high-loss claims saved to {map_filename}")
    else:
        print("\nNo valid geospatial data to plot map.")

    print("\nRoot Cause Analysis complete.")

if __name__ == "__main__":
    db_file_path = os.path.join('..', '..', 'data', 'processed', 'city_claims.db')
    perform_root_cause_analysis(db_file_path)
