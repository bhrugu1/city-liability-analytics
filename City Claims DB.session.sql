-- sql/queries.sql
-- This file contains example SQL queries for initial data exploration,
-- aggregation, and transformation within the SQLite database.
-- These queries can be run directly in VS Code using a SQL extension.

-- Example 1: Total claims and total loss amount per year
-- This query helps understand the overall trend of claims and financial impact over time.
SELECT
    strftime('%Y', Date_of_Incident) AS Incident_Year, -- Extract year from incident date
    COUNT(Claim_ID) AS Total_Claims,                   -- Count of unique claims
    SUM(Settlement_Amount + Legal_Costs) AS Total_Loss_Amount -- Sum of settlement and legal costs
FROM claims
GROUP BY Incident_Year
ORDER BY Incident_Year;

-- Example 2: Top 10 incident types by total loss amount
-- Identifies which types of incidents are most costly to the city.
SELECT
    Incident_Type,
    SUM(Settlement_Amount + Legal_Costs) AS Total_Loss
FROM claims
GROUP BY Incident_Type
ORDER BY Total_Loss DESC
LIMIT 10; -- Limit to top 10 for focused analysis

-- Example 3: Claims count and average loss by City Division and Claim Status
-- Provides insights into which divisions have claims and their resolution status,
-- and the average cost associated with claims in each status.
SELECT
    City_Division_Involved,
    Claim_Status,
    COUNT(Claim_ID) AS Number_of_Claims,
    AVG(Settlement_Amount + Legal_Costs) AS Average_Loss_Per_Claim
FROM claims
GROUP BY City_Division_Involved, Claim_Status
ORDER BY City_Division_Involved, Number_of_Claims DESC;

-- Example 4: Claims where "Pothole" is mentioned in the Alleged_Cause or Allegation_Details
-- Useful for identifying specific recurring issues.
SELECT
    Claim_ID,
    Date_of_Incident,
    Incident_Type,
    City_Division_Involved,
    Alleged_Cause,
    Allegation_Details,
    (Settlement_Amount + Legal_Costs) AS Total_Loss
FROM claims
WHERE Alleged_Cause LIKE '%Pothole%' OR Allegation_Details LIKE '%pothole%';

-- Example 5: Monthly trend of new claims filed
-- Helps track the inflow of new claims over time.
SELECT
    strftime('%Y-%m', Date_Claim_Filed) AS Claim_Filed_Month,
    COUNT(Claim_ID) AS Claims_Filed_Count
FROM claims
GROUP BY Claim_Filed_Month
ORDER BY Claim_Filed_Month;
