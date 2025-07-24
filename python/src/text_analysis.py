"""
Chicago City Liability Analysis - Natural Language Processing & Root Cause Analysis Module

This module performs advanced text analysis on Chicago municipal liability claim 
allegations to identify operational oversights, systemic patterns, and geospatial 
risk clusters within the Chicago metropolitan area. It combines NLP techniques with 
Chicago-specific geospatial analytics to provide actionable insights for Chicago 
municipal risk mitigation and operational improvements.

Geographic Focus: Chicago neighborhoods and municipal boundaries
Municipal Context: Chicago city operations and infrastructure

Author: Chicago Municipal Data Analysis Team
Date: July 2025
Project: Chicago City Liability Analytics Platform
"""

import pandas as pd
import sqlite3
import re
from nltk.corpus import stopwords
from collections import Counter
import spacy
import folium
import plotly.express as px
import os

# Natural Language Processing Setup
# ================================

# Note: Download NLTK stopwords if not already downloaded
# import nltk
# nltk.download('stopwords')

# Load spaCy English language model for advanced NLP processing
# SpaCy provides named entity recognition, part-of-speech tagging, and semantic analysis
try:
    nlp = spacy.load("en_core_web_sm")
    print("✅ SpaCy English model loaded successfully")
except OSError:
    print("❌ SpaCy model 'en_core_web_sm' not found.")
    print("Please run 'python -m spacy download en_core_web_sm' in your terminal.")
    exit()

# Initialize stopwords for text cleaning (common words like 'the', 'and', 'is')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    """
    Clean and preprocess text data for NLP analysis.
    
    This function performs comprehensive text preprocessing including:
    - Null value handling
    - Case normalization
    - Special character removal
    - Stopword filtering
    - Short word elimination
    
    Args:
        text (str): Raw text from allegation details
        
    Returns:
        str: Cleaned text ready for analysis
    """
    # Handle missing or null values gracefully
    if pd.isna(text):
        return ""
    
    # Convert to lowercase for standardization
    text = str(text).lower()
    
    # Remove special characters, numbers, and punctuation (keep only letters and spaces)
    text = re.sub(r'[^a-z\s]', '', text)
    
    # Filter out stopwords and very short words (likely not meaningful)
    # This reduces noise and focuses on content-bearing words
    text = ' '.join([
        word for word in text.split() 
        if word not in stop_words and len(word) > 1
    ])
    
    return text

def perform_root_cause_analysis(db_path):
    """
    Perform comprehensive root cause analysis using NLP and geospatial analytics.
    
    This function conducts multi-layered analysis to identify:
    - Operational oversight patterns in claim allegations
    - Financial impact of specific oversight categories
    - Geospatial clustering of high-risk incidents
    - Actionable insights for risk mitigation
    
    Args:
        db_path (str): Path to SQLite database containing claims data
        
    Returns:
        None: Generates analysis outputs and visualization files
    """
    
    print("🔍 Starting NLP-Based Root Cause Analysis")
    print("=" * 50)
    
    # Ensure output directory exists for maps and visualizations
    output_dir = os.path.join('..', '..', 'output')
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Output directory: {os.path.abspath(output_dir)}")

    # Database connection and data extraction
    print(f"🔗 Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    
    try:
        # Extract comprehensive dataset including geospatial coordinates
        query = """
        SELECT 
            Claim_ID, 
            Allegation_Details, 
            Incident_Type, 
            City_Division_Involved, 
            (Settlement_Amount + Legal_Costs) AS Total_Loss, 
            Latitude, 
            Longitude 
        FROM claims
        """
        df = pd.read_sql(query, conn)
        print(f"✅ Successfully loaded {len(df)} claims for analysis")
        
    except Exception as e:
        print(f"❌ Error reading data from database: {e}")
        conn.close()
        return
    finally:
        conn.close()

    # Text Preprocessing Pipeline
    print("🔄 Preprocessing allegation text data...")
    df['Cleaned_Allegation_Details'] = df['Allegation_Details'].apply(clean_text)
    print("✅ Text cleaning completed")

    # --- KEYWORD FREQUENCY ANALYSIS ---
    print("\n📊 Performing Keyword Frequency Analysis...")
    
    # Aggregate all cleaned text for comprehensive word frequency analysis
    all_words = ' '.join(df['Cleaned_Allegation_Details']).split()
    word_counts = Counter(all_words)
    
    print(f"📈 Total words analyzed: {len(all_words):,}")
    print(f"📚 Unique words identified: {len(word_counts):,}")
    print("\n🔤 Top 30 most frequent words in allegations (after cleaning):")
    
    # Display top keywords that may indicate systemic issues
    for word, count in word_counts.most_common(30):
        print(f"   • {word}: {count} occurrences")

    # --- OPERATIONAL OVERSIGHT DETECTION ---
    print("\n🔍 Detecting Operational Oversights...")
    
    # Define comprehensive oversight keyword taxonomy
    # These keywords are carefully selected based on municipal liability patterns
    oversight_keywords = [
        # Infrastructure maintenance issues
        'inspection', 'repair', 'maintenance', 'neglect', 'delay',
        # Training and supervision gaps
        'training', 'supervision', 'oversight', 'protocol',
        # Physical hazards and conditions
        'signage', 'faulty', 'poor', 'inadequate', 'missing', 'broken',
        'debris', 'pothole', 'uneven', 'icy', 'spill', 'defect',
        # Safety and compliance
        'unsafe', 'hazard', 'warning', 'barrier', 'condition'
    ]
    
    # Apply keyword matching to identify potential operational oversights
    df['Identified_Oversights'] = df['Cleaned_Allegation_Details'].apply(
        lambda text: [keyword for keyword in oversight_keywords if keyword in text]
    )
    
    # Filter claims with identified operational issues
    df_oversights = df[df['Identified_Oversights'].apply(len) > 0].copy()
    
    print(f"✅ Found {len(df_oversights)} claims with identified operational oversights")
    print(f"📊 Oversight detection rate: {(len(df_oversights)/len(df)*100):.1f}% of total claims")
    
    # Display sample results for validation
    print("\n📋 Sample claims with identified oversights:")
    sample_cols = ['Claim_ID', 'Incident_Type', 'City_Division_Involved', 'Identified_Oversights', 'Total_Loss']
    print(df_oversights[sample_cols].head())

    # --- FINANCIAL IMPACT ANALYSIS BY OVERSIGHT TYPE ---
    print("\n💰 Calculating Financial Impact by Oversight Category...")
    
    # Create detailed oversight-loss mapping for financial analysis
    oversight_loss_data = []
    for index, row in df_oversights.iterrows():
        for oversight in row['Identified_Oversights']:
            oversight_loss_data.append({
                'Oversight': oversight, 
                'Total_Loss': row['Total_Loss'],
                'Claim_ID': row['Claim_ID'],
                'Division': row['City_Division_Involved']
            })
    
    df_oversight_loss = pd.DataFrame(oversight_loss_data)

    if not df_oversight_loss.empty:
        # Calculate total financial impact by oversight category
        total_loss_by_oversight = (
            df_oversight_loss.groupby('Oversight')['Total_Loss']
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        
        # Calculate claim frequency by oversight type
        claim_count_by_oversight = (
            df_oversight_loss.groupby('Oversight')['Claim_ID']
            .nunique()
            .reset_index()
            .rename(columns={'Claim_ID': 'Claim_Count'})
        )
        
        # Merge financial and frequency data
        oversight_analysis = total_loss_by_oversight.merge(
            claim_count_by_oversight, on='Oversight'
        )
        oversight_analysis['Avg_Loss_Per_Claim'] = (
            oversight_analysis['Total_Loss'] / oversight_analysis['Claim_Count']
        )
        
        print(f"\n📊 Total Loss associated with top 10 identified oversights:")
        for _, row in oversight_analysis.head(10).iterrows():
            print(f"   • {row['Oversight']}: ${row['Total_Loss']:,.2f} "
                  f"({row['Claim_Count']} claims, avg: ${row['Avg_Loss_Per_Claim']:,.2f})")

        # Generate interactive visualization of top oversight costs
        fig_oversight_loss = px.bar(
            total_loss_by_oversight.head(10), 
            x='Oversight', 
            y='Total_Loss',
            title='Top 10 Operational Oversights by Associated Financial Loss',
            labels={
                'Oversight': 'Identified Oversight Category', 
                'Total_Loss': 'Total Loss Amount ($)'
            },
            color='Total_Loss', 
            color_continuous_scale=px.colors.sequential.OrRd,
            template='plotly_white'
        )
        
        # Enhance chart readability
        fig_oversight_loss.update_layout(
            xaxis_tickangle=45,
            hovermode='x unified'
        )
        
        # Save interactive visualization
        output_file = os.path.join(output_dir, "top_oversights_by_loss.html")
        fig_oversight_loss.write_html(output_file)
        print(f"✅ Saved oversight analysis: {output_file}")
        
    else:
        print("⚠️ No significant oversights identified or data for oversight analysis is empty.")


    # --- GEOSPATIAL RISK ANALYSIS ---
    print("\n🗺️ Performing Geospatial Risk Analysis...")
    
    # Filter out claims with invalid or missing geographic coordinates
    df_valid_geo = df.dropna(subset=['Latitude', 'Longitude'])
    invalid_geo_count = len(df) - len(df_valid_geo)
    
    print(f"📍 Valid geospatial records: {len(df_valid_geo)}")
    if invalid_geo_count > 0:
        print(f"⚠️ Records with invalid coordinates: {invalid_geo_count}")

    if not df_valid_geo.empty:
        # Calculate map center point for optimal visualization
        map_center = [
            df_valid_geo['Latitude'].mean(), 
            df_valid_geo['Longitude'].mean()
        ]
        
        # Initialize interactive map with professional styling
        m = folium.Map(
            location=map_center, 
            zoom_start=12,
            tiles='OpenStreetMap'
        )
        
        # Add title and legend information
        title_html = '''
        <h3 align="center" style="font-size:20px"><b>City Liability Claims - High-Risk Geographic Distribution</b></h3>
        <p align="center">Showing top 200 highest-loss claims by location</p>
        '''
        m.get_root().html.add_child(folium.Element(title_html))

        # Plot top 200 highest-loss claims for focused risk analysis
        high_loss_claims = df_valid_geo.nlargest(200, 'Total_Loss')
        marker_count = 0
        
        for idx, row in high_loss_claims.iterrows():
            # Final validation of coordinate data
            if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
                
                # Create detailed popup with claim information
                popup_content = f"""
                <div style="
                    width: 500px; 
                    padding: 15px; 
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                ">
                    <div style="
                        text-align: center; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 12px;
                        margin: -15px -15px 15px -15px;
                        border-radius: 8px 8px 0 0;
                        font-size: 18px;
                        font-weight: bold;
                    ">
                        📋 Claim #{row['Claim_ID']}
                    </div>
                    
                    <div style="margin-bottom: 15px;">
                        <div style="
                            display: inline-block;
                            background-color: #f8f9fa;
                            padding: 8px 12px;
                            border-radius: 20px;
                            font-size: 14px;
                            font-weight: bold;
                            color: #495057;
                            margin-bottom: 10px;
                        ">
                            🏷️ {row['Incident_Type']}
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 15px;">
                        <p style="margin: 8px 0; font-size: 15px; color: #333;">
                            <strong style="color: #495057;">🏛️ City Division:</strong> 
                            <span style="color: #007bff;">{row['City_Division_Involved']}</span>
                        </p>
                        
                        <p style="margin: 8px 0; font-size: 16px; color: #333;">
                            <strong style="color: #495057;">💰 Financial Impact:</strong> 
                            <span style="
                                color: #dc3545; 
                                font-weight: bold; 
                                font-size: 17px;
                            ">${row['Total_Loss']:,.2f}</span>
                        </p>
                        
                        <p style="margin: 8px 0; font-size: 13px; color: #6c757d;">
                            <strong>📍 Coordinates:</strong> {row['Latitude']:.4f}, {row['Longitude']:.4f}
                        </p>
                    </div>
                    
                    <hr style="border: none; height: 1px; background-color: #e9ecef; margin: 15px 0;">
                    
                    <div>
                        <p style="
                            margin: 0 0 8px 0; 
                            font-size: 15px; 
                            font-weight: bold; 
                            color: #495057;
                        ">📝 Incident Details:</p>
                        
                        <div style="
                            background-color: #f8f9fa;
                            padding: 12px;
                            border-radius: 6px;
                            border-left: 4px solid #007bff;
                            max-height: 120px;
                            overflow-y: auto;
                            font-size: 14px;
                            line-height: 1.5;
                            color: #495057;
                        ">
                            {row['Allegation_Details'][:400]}{'...' if len(row['Allegation_Details']) > 400 else ''}
                        </div>
                    </div>
                    
                    <div style="
                        margin-top: 15px;
                        padding-top: 10px;
                        border-top: 1px solid #e9ecef;
                        text-align: center;
                        font-size: 12px;
                        color: #6c757d;
                    ">
                        💡 Click and drag to explore the map
                    </div>
                </div>
                """
                
                # Color-code markers based on loss severity
                if row['Total_Loss'] > 100000:  # High-risk claims
                    icon_color = 'red'
                    icon_icon = 'exclamation-sign'
                elif row['Total_Loss'] > 50000:  # Medium-risk claims
                    icon_color = 'orange'
                    icon_icon = 'warning-sign'
                else:  # Lower-risk claims
                    icon_color = 'yellow'
                    icon_icon = 'info-sign'
                
                # Add marker to map
                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    popup=folium.Popup(popup_content, max_width=550),
                    icon=folium.Icon(color=icon_color, icon=icon_icon)
                ).add_to(m)
                
                marker_count += 1
        
        # Save interactive geospatial analysis
        map_filename = os.path.join(output_dir, "high_loss_claims_map.html")
        m.save(map_filename)
        print(f"✅ Geospatial analysis saved: {map_filename}")
        print(f"📍 Mapped {marker_count} high-risk claim locations")
        
    else:
        print("⚠️ No valid geospatial data available for mapping analysis.")

    # --- ANALYSIS SUMMARY ---
    print("\n📊 ROOT CAUSE ANALYSIS SUMMARY")
    print("=" * 45)
    print(f"📈 Total Claims Analyzed: {len(df):,}")
    print(f"🔍 Claims with Oversight Issues: {len(df_oversights):,}")
    print(f"📊 Oversight Detection Rate: {(len(df_oversights)/len(df)*100):.1f}%")
    
    if not df_oversight_loss.empty:
        total_oversight_loss = df_oversight_loss['Total_Loss'].sum()
        print(f"💰 Total Loss from Oversight Issues: ${total_oversight_loss:,.2f}")
        print(f"📉 Percentage of Total Exposure: {(total_oversight_loss/df['Total_Loss'].sum()*100):.1f}%")
    
    print(f"🗺️ Geospatial Records: {len(df_valid_geo):,}")
    print(f"📁 Generated Analysis Files:")
    print(f"   • Oversight financial impact visualization")
    print(f"   • Interactive geospatial risk map")

    print("\n✅ Root Cause Analysis complete!")
    print("🎯 Key insights for operational improvement identified.")

if __name__ == "__main__":
    """
    Main execution block for NLP-based root cause analysis.
    
    Executes comprehensive text analysis pipeline including:
    - Keyword frequency analysis
    - Operational oversight detection
    - Financial impact assessment
    - Geospatial risk mapping
    """
    
    # Define database path relative to project structure
    db_file_path = os.path.join('..', '..', 'data', 'processed', 'city_claims.db')
    
    # Execute comprehensive root cause analysis
    perform_root_cause_analysis(db_file_path)
