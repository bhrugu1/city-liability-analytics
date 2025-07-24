# Chicago City Liability Analytics Platform

**Chicago City Liability Analytics Platform** is a comprehensive data analytics solution that analyzes municipal liability claims for the City of Chicago to identify risk patterns, operational oversights, and cost-saving opportunities. The system processes 75,000 simulated Chicago liability claims using advanced Python analytics, SQLite database management, NLP-powered root cause analysis (NLTK/spaCy), and creates interactive geospatial visualizations covering the greater Chicago metropolitan area.

## 🏙️ Chicago-Specific Features

- **Geographic Focus**: Analysis covers Chicago's 7 major zones including Downtown Loop, North Side, South Side, West Side, and suburban areas
- **Municipal Context**: Tailored for Chicago's city divisions including Public Works, Parks & Recreation, Fire Services, Transit, Water & Wastewater, and By-law Enforcement
- **Realistic Geospatial Data**: All 75,000 claims mapped to actual Chicago land areas (avoiding Lake Michigan and water bodies)
- **Chicago Infrastructure**: Analysis of Chicago-specific issues including pothole claims, winter weather incidents, and urban infrastructure challenges

## 🎯 Key Features

- **Complete Data Pipeline**: End-to-end ETL process from Chicago claims simulation to comprehensive analysis
- **Advanced Text Analytics**: NLP-powered root cause analysis using NLTK and spaCy for Chicago incident patterns
- **Interactive Chicago Map**: Folium-based geospatial visualizations showing high-risk areas across Chicago neighborhoods
- **Municipal Performance Metrics**: Automated KPI calculation and quarterly reporting for Chicago city management
- **Chicago Risk Assessment**: Geographic clustering and operational oversight identification specific to Chicago's urban environment

## 📊 Chicago Analysis Results

- **75,000 Chicago claims** analyzed across metropolitan area (2015-2024)
- **$14.5 billion** total financial exposure for City of Chicago
- **$2.1 billion** attributed to infrastructure oversight issues (14.5% of total exposure)
- **Chicago Geographic Coverage**: 7 major zones from Downtown Loop to suburban areas
- **Municipal Efficiency**: 75% claim resolution rate with 45-day average processing time
- **Chicago-Specific Insights**: Identified seasonal patterns, infrastructure risks, and divisional performance across Chicago's municipal departments

## 🏗️ Chicago Project Architecture

```
Chicago_City_Liability_Analysis/
├── data/
│   ├── raw/chicago_simulated_claims.csv
│   └── processed/chicago_city_claims.db
├── python/src/
│   ├── data_simulation.py          # Chicago claims data generation
│   ├── load_data_to_db.py         # Chicago database ETL pipeline
│   ├── analysis.py                # Chicago statistical analysis
│   ├── text_analysis.py           # Chicago NLP & geospatial mapping
│   └── kpi_calculation.py         # Chicago municipal KPI metrics
├── sql/
│   ├── schema.sql                 # Chicago claims database schema
│   └── queries.sql                # Chicago business intelligence queries
├── output/
│   ├── high_loss_claims_map.html  # Interactive Chicago risk map
│   └── *.html                     # Chicago analytics dashboards
└── docs/chicago_project_report.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Required packages: `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `folium`, `nltk`, `spacy`, `faker`

### Installation

1. Clone the repository:
```bash
git clone https://github.com/bhrugu1/chicago-city-liability-analytics.git
cd chicago-city-liability-analytics
cd city-liability-analytics
```

2. Install dependencies:
```bash
pip install pandas numpy matplotlib seaborn plotly folium nltk spacy faker
```

3. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

### Usage

1. **Generate simulated data:**
```bash
cd python/src
python data_simulation.py
```

2. **Load data to database:**
```bash
python load_data_to_db.py
```

3. **Run analysis:**
```bash
python analysis.py
python text_analysis.py
python kpi_calculation.py
```

4. **View results:**
- Interactive charts in `output/` directory
- Comprehensive report in `docs/project_report.md`

## 📈 Analysis Components

### 1. Loss Frequency & Severity Analysis
- Temporal trend analysis
- Incident type categorization
- City division impact assessment

### 2. Text Analytics & Root Cause Analysis
- NLP-powered allegation processing
- Operational oversight identification
- Geographic risk mapping

### 3. KPI Dashboard
- Quarterly performance metrics
- Financial exposure tracking
- Resolution rate monitoring

## 💡 Key Insights

- **Top Risk Factor**: Poor conditions account for 29% of total losses
- **High-Risk Divisions**: Public Works and Parks & Recreation
- **Geographic Patterns**: Identified clusters requiring priority attention
- **Cost Optimization**: Potential $420M savings through targeted interventions

## 🛠️ Technology Stack

- **Database**: SQLite
- **Backend**: Python 3.13
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn, plotly, folium
- **NLP**: NLTK, spaCy
- **Data Generation**: faker

## 📋 Project Structure

- **Data Layer**: Raw and processed data storage
- **Analysis Layer**: Statistical analysis and ML processing
- **Visualization Layer**: Interactive charts and geographic mapping
- **Reporting Layer**: Automated KPI calculation and business reporting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-analysis`)
3. Commit changes (`git commit -am 'Add new analysis feature'`)
4. Push to branch (`git push origin feature/new-analysis`)
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

**Author**: Data Analysis Team  
**Repository**: [city-liability-analytics](https://github.com/bhrugu1/city-liability-analytics)  
**Date**: July 2025

---

*This project demonstrates advanced data analytics techniques for municipal risk management and operational optimization.*
