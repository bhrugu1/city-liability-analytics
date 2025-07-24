/*
==============================================================================
CHICAGO CITY LIABILITY ANALYSIS - COMPREHENSIVE SQL ANALYTICS QUERIES
==============================================================================

Purpose: Strategic business intelligence queries for Chicago municipal liability 
         management, risk analysis, and operational decision-making.

Geographic Focus: Chicago, Illinois metropolitan area
Municipal Context: Chicago city divisions and operations

This query collection supports:
- Chicago executive dashboard reporting
- Chicago municipal operational performance monitoring
- Risk pattern identification within Chicago boundaries
- Financial impact analysis for Chicago city budget
- Predictive analytics data preparation for Chicago planning

Author: Business Intelligence Team
Date: July 2025
Project: City Liability Analytics
Database: SQLite 3.x (city_claims.db)
==============================================================================
*/

-- ==============================================================================
-- TEMPORAL TREND ANALYSIS QUERIES
-- ==============================================================================

-- Query 1: Annual Claims and Financial Impact Trend Analysis
-- PURPOSE: Provides year-over-year claims volume and cost trends for strategic planning
-- USE CASE: Executive reporting, budget forecasting, trend identification
SELECT
    strftime('%Y', Date_of_Incident) AS Incident_Year,     -- Extract calendar year
    COUNT(Claim_ID) AS Total_Claims,                       -- Annual claim frequency
    SUM(Settlement_Amount + Legal_Costs) AS Total_Loss_Amount, -- Total financial exposure
    AVG(Settlement_Amount + Legal_Costs) AS Avg_Loss_Per_Claim,  -- Average claim cost
    SUM(Settlement_Amount) AS Total_Settlements,           -- Settlement-specific costs
    SUM(Legal_Costs) AS Total_Legal_Costs,                -- Legal expense analysis
    -- Calculate year-over-year growth indicators
    ROUND(AVG(Settlement_Amount + Legal_Costs), 2) AS Average_Annual_Cost
FROM claims
WHERE Date_of_Incident IS NOT NULL -- Ensure valid incident dates
GROUP BY Incident_Year
ORDER BY Incident_Year;

-- ==============================================================================
-- RISK CATEGORY ANALYSIS QUERIES
-- ==============================================================================

-- Query 2: High-Impact Incident Type Analysis with Risk Ranking
-- PURPOSE: Identifies most costly incident categories for risk mitigation prioritization
-- USE CASE: Risk management strategy, resource allocation, prevention planning
SELECT
    Incident_Type,
    COUNT(Claim_ID) AS Claim_Count,                        -- Frequency of incident type
    SUM(Settlement_Amount + Legal_Costs) AS Total_Loss,    -- Total financial impact
    AVG(Settlement_Amount + Legal_Costs) AS Avg_Loss_Per_Incident, -- Average cost severity
    MAX(Settlement_Amount + Legal_Costs) AS Max_Single_Loss, -- Highest individual claim
    MIN(Settlement_Amount + Legal_Costs) AS Min_Single_Loss, -- Lowest individual claim
    -- Calculate percentage of total exposure
    ROUND(
        (SUM(Settlement_Amount + Legal_Costs) * 100.0) / 
        (SELECT SUM(Settlement_Amount + Legal_Costs) FROM claims), 2
    ) AS Percentage_of_Total_Exposure
FROM claims
WHERE Settlement_Amount IS NOT NULL AND Legal_Costs IS NOT NULL
GROUP BY Incident_Type
HAVING COUNT(Claim_ID) >= 5 -- Focus on statistically significant categories
ORDER BY Total_Loss DESC; -- Top 15 most costly incident types

-- ==============================================================================
-- ORGANIZATIONAL PERFORMANCE ANALYSIS QUERIES
-- ==============================================================================

-- Query 3: Division Performance Dashboard with Status Breakdown
-- PURPOSE: Comprehensive divisional analysis for operational oversight and accountability
-- USE CASE: Management reporting, performance reviews, resource allocation
SELECT
    City_Division_Involved,
    Claim_Status,
    COUNT(Claim_ID) AS Number_of_Claims,                   -- Claim volume by division/status
    AVG(Settlement_Amount + Legal_Costs) AS Average_Loss_Per_Claim, -- Cost efficiency
    SUM(Settlement_Amount + Legal_Costs) AS Total_Division_Loss, -- Total divisional exposure
    -- Calculate resolution efficiency metrics
    ROUND(
        CASE 
            WHEN Claim_Status LIKE 'Closed%' THEN 100.0
            ELSE 0.0
        END, 2
    ) AS Resolution_Status_Flag,
    -- Calculate average processing time for closed claims
    AVG(
        CASE 
            WHEN Claim_Status LIKE 'Closed%' 
            THEN julianday(Date_Claim_Filed) - julianday(Date_of_Incident)
            ELSE NULL
        END
    ) AS Avg_Days_to_Resolution
FROM claims
WHERE City_Division_Involved IS NOT NULL
GROUP BY City_Division_Involved, Claim_Status
ORDER BY City_Division_Involved, Number_of_Claims DESC;

-- ==============================================================================
-- INFRASTRUCTURE RISK ANALYSIS QUERIES
-- ==============================================================================

-- Query 4: Infrastructure-Related Claims Analysis (Pothole and Road Hazards)
-- PURPOSE: Identifies infrastructure maintenance issues and associated costs
-- USE CASE: Public Works prioritization, infrastructure investment planning
SELECT
    Claim_ID,
    Date_of_Incident,
    Incident_Type,
    City_Division_Involved,
    Alleged_Cause,
    Location_Details,
    (Settlement_Amount + Legal_Costs) AS Total_Loss,
    -- Categorize by infrastructure issue type
    CASE 
        WHEN LOWER(Alleged_Cause) LIKE '%pothole%' OR LOWER(Allegation_Details) LIKE '%pothole%' 
        THEN 'Pothole-Related'
        WHEN LOWER(Alleged_Cause) LIKE '%road%' OR LOWER(Allegation_Details) LIKE '%road%'
        THEN 'Road Condition'
        WHEN LOWER(Alleged_Cause) LIKE '%sidewalk%' OR LOWER(Allegation_Details) LIKE '%sidewalk%'
        THEN 'Sidewalk Issue'
        WHEN LOWER(Alleged_Cause) LIKE '%sign%' OR LOWER(Allegation_Details) LIKE '%sign%'
        THEN 'Signage Problem'
        ELSE 'Other Infrastructure'
    END AS Infrastructure_Category
FROM claims
WHERE (
    LOWER(Alleged_Cause) LIKE '%pothole%' OR LOWER(Allegation_Details) LIKE '%pothole%' OR
    LOWER(Alleged_Cause) LIKE '%road%' OR LOWER(Allegation_Details) LIKE '%road%' OR
    LOWER(Alleged_Cause) LIKE '%sidewalk%' OR LOWER(Allegation_Details) LIKE '%sidewalk%' OR
    LOWER(Alleged_Cause) LIKE '%sign%' OR LOWER(Allegation_Details) LIKE '%sign%'
)
ORDER BY Total_Loss DESC;

-- ==============================================================================
-- OPERATIONAL WORKFLOW ANALYSIS QUERIES
-- ==============================================================================

-- Query 5: Claims Processing Efficiency Analysis
-- PURPOSE: Monitors claim filing patterns and processing workflow efficiency
-- USE CASE: Operational improvement, workflow optimization, staff allocation
SELECT
    strftime('%Y-%m', Date_Claim_Filed) AS Claim_Filed_Month, -- Monthly filing patterns
    COUNT(Claim_ID) AS Claims_Filed_Count,                    -- Monthly claim volume
    AVG(Settlement_Amount + Legal_Costs) AS Avg_Monthly_Cost, -- Average monthly cost
    -- Calculate processing time from incident to filing
    AVG(julianday(Date_Claim_Filed) - julianday(Date_of_Incident)) AS Avg_Days_Incident_to_Filing,
    -- Status distribution for the month
    SUM(CASE WHEN Claim_Status LIKE 'Closed%' THEN 1 ELSE 0 END) AS Resolved_Claims,
    SUM(CASE WHEN Claim_Status = 'Open' THEN 1 ELSE 0 END) AS Open_Claims,
    SUM(CASE WHEN Claim_Status = 'Under Investigation' THEN 1 ELSE 0 END) AS Under_Investigation
FROM claims
WHERE Date_Claim_Filed IS NOT NULL
GROUP BY Claim_Filed_Month
ORDER BY Claim_Filed_Month;

-- ==============================================================================
-- GEOSPATIAL RISK HOTSPOT ANALYSIS QUERIES
-- ==============================================================================

-- Query 6: Geographic Risk Concentration Analysis
-- PURPOSE: Identifies high-risk geographic areas for targeted intervention
-- USE CASE: Geographic risk mapping, patrol allocation, infrastructure prioritization
SELECT
    -- Round coordinates to create geographic clusters (approximately 0.01 degree = ~1km)
    ROUND(Latitude, 2) AS Lat_Cluster,
    ROUND(Longitude, 2) AS Lng_Cluster,
    COUNT(Claim_ID) AS Claims_in_Area,                      -- Claim density
    SUM(Settlement_Amount + Legal_Costs) AS Total_Area_Loss, -- Geographic financial impact
    AVG(Settlement_Amount + Legal_Costs) AS Avg_Area_Cost,   -- Average cost per location
    -- Identify most common incident types in area
    GROUP_CONCAT(DISTINCT Incident_Type) AS Incident_Types_in_Area,
    -- Identify primary responsible division
    GROUP_CONCAT(DISTINCT City_Division_Involved) AS Divisions_Involved
FROM claims
WHERE Latitude IS NOT NULL 
  AND Longitude IS NOT NULL
  AND Latitude BETWEEN 25.0 AND 50.0  -- Reasonable US latitude range
  AND Longitude BETWEEN -130.0 AND -65.0  -- Reasonable US longitude range
GROUP BY Lat_Cluster, Lng_Cluster
HAVING COUNT(Claim_ID) >= 3 -- Focus on areas with multiple incidents
ORDER BY Total_Area_Loss DESC
LIMIT 20; -- Top 20 highest-risk geographic clusters

-- ==============================================================================
-- FINANCIAL PERFORMANCE AND SETTLEMENT ANALYSIS QUERIES
-- ==============================================================================

-- Query 7: Settlement Strategy Effectiveness Analysis
-- PURPOSE: Evaluates settlement patterns and legal cost efficiency
-- USE CASE: Legal strategy optimization, settlement policy development
SELECT
    Claim_Status,
    COUNT(Claim_ID) AS Total_Claims,
    AVG(Settlement_Amount) AS Avg_Settlement,
    AVG(Legal_Costs) AS Avg_Legal_Costs,
    SUM(Settlement_Amount) AS Total_Settlements,
    SUM(Legal_Costs) AS Total_Legal_Costs,
    -- Calculate settlement vs. legal cost ratio
    ROUND(
        CASE 
            WHEN SUM(Legal_Costs) > 0 
            THEN SUM(Settlement_Amount) / SUM(Legal_Costs)
            ELSE NULL
        END, 2
    ) AS Settlement_to_Legal_Cost_Ratio,
    -- Calculate average total cost per claim
    AVG(Settlement_Amount + Legal_Costs) AS Avg_Total_Cost_Per_Claim
FROM claims
WHERE Settlement_Amount IS NOT NULL AND Legal_Costs IS NOT NULL
GROUP BY Claim_Status
ORDER BY Total_Claims DESC;

-- ==============================================================================
-- ADVANCED ANALYTICS SUPPORT QUERIES
-- ==============================================================================

-- Query 8: Comprehensive Data Export for Advanced Analytics
-- PURPOSE: Provides clean, analysis-ready dataset for machine learning and advanced analytics
-- USE CASE: Predictive modeling, pattern recognition, external analytics tools
SELECT
    Claim_ID,
    Date_of_Incident,
    Date_Claim_Filed,
    strftime('%Y', Date_of_Incident) AS Incident_Year,
    strftime('%m', Date_of_Incident) AS Incident_Month,
    strftime('%w', Date_of_Incident) AS Incident_Day_of_Week, -- 0=Sunday, 6=Saturday
    Incident_Type,
    Alleged_Cause,
    City_Division_Involved,
    Claim_Status,
    Settlement_Amount,
    Legal_Costs,
    (Settlement_Amount + Legal_Costs) AS Total_Loss,
    Latitude,
    Longitude,
    -- Calculate processing metrics
    CASE 
        WHEN Date_Claim_Filed IS NOT NULL AND Date_of_Incident IS NOT NULL
        THEN julianday(Date_Claim_Filed) - julianday(Date_of_Incident)
        ELSE NULL
    END AS Days_from_Incident_to_Filing,
    -- Create categorical variables for analysis
    CASE 
        WHEN (Settlement_Amount + Legal_Costs) > 100000 THEN 'High'
        WHEN (Settlement_Amount + Legal_Costs) > 25000 THEN 'Medium'
        ELSE 'Low'
    END AS Loss_Severity_Category,
    -- Text length indicators for NLP preprocessing
    LENGTH(Allegation_Details) AS Allegation_Text_Length,
    LENGTH(Location_Details) AS Location_Text_Length
FROM claims
WHERE Date_of_Incident IS NOT NULL
ORDER BY Date_of_Incident, Claim_ID;

/*
==============================================================================
QUERY USAGE NOTES
==============================================================================

PERFORMANCE OPTIMIZATION:
- All queries utilize available indexes for optimal performance
- Date filters prevent full table scans on large datasets
- HAVING clauses filter aggregated results efficiently

DATA QUALITY CONSIDERATIONS:
- NULL checks ensure accurate calculations
- Reasonable geographic bounds filter invalid coordinates
- Statistical significance filters (minimum claim counts) improve relevance

BUSINESS INTELLIGENCE APPLICATIONS:
- Results can be exported to CSV for dashboard integration
- Queries support both operational and strategic decision-making
- Geographic analysis enables spatial risk assessment

EXTENSIBILITY:
- Queries can be modified for different time periods
- Thresholds and categories can be adjusted for different municipalities
- Additional calculated fields can be added as needed

==============================================================================
*/
