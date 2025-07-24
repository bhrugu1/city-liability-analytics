# City Liability Analytics

**City Liability Analytics** analyzes municipal liability claims to identify risk patterns and cost-saving opportunities. Processes 75K simulated claims using Python, SQLite, NLP (NLTK/spaCy), and creates interactive visualizations with Plotly/Folium. Identifies operational oversights costing billions, enabling data-driven municipal risk management.

## 🎯 Key Features

- **Data Pipeline**: Complete ETL process from simulation to analysis
- **Text Analytics**: NLP-powered root cause analysis using NLTK and spaCy
- **Interactive Visualizations**: Plotly charts and Folium geospatial maps
- **Performance Metrics**: Automated KPI calculation and quarterly reporting
- **Risk Assessment**: Geographic clustering and operational oversight identification

## 📊 Project Results

- **75,000 claims** analyzed (2015-2024)
- **$14.5 billion** total financial exposure identified
- **$2.1 billion** attributed to "poor conditions" oversight
- **75% claim resolution rate** with 45-day average processing time

## 🏗️ Architecture

```
City_Liability_Analysis/
├── data/
│   ├── raw/simulated_claims.csv
│   └── processed/city_claims.db
├── python/src/
│   ├── data_simulation.py
│   ├── load_data_to_db.py
│   ├── analysis.py
│   ├── text_analysis.py
│   └── kpi_calculation.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── output/
└── docs/project_report.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Required packages: `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `folium`, `nltk`, `spacy`, `faker`

### Installation

1. Clone the repository:
```bash
git clone https://github.com/bhrugu1/city-liability-analytics.git
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
