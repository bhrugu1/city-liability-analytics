-- sql/schema.sql
-- Defines the table structure for city liability claims.
-- This schema is designed to store various details about each claim,
-- including dates, types, involved divisions, financial aspects,
-- and textual allegations.

CREATE TABLE IF NOT EXISTS claims (
    Claim_ID VARCHAR(50) PRIMARY KEY,        -- Unique identifier for each claim
    Date_of_Incident DATE,                  -- Date when the incident occurred
    Date_Claim_Filed DATE,                  -- Date when the claim was officially filed
    Incident_Type VARCHAR(100),             -- Category of the incident (e.g., Slip & Fall, Vehicle Damage)
    Alleged_Cause VARCHAR(255),             -- The specific alleged cause of the incident
    City_Division_Involved VARCHAR(100),    -- The city division associated with the incident
    Location_Details TEXT,                  -- Detailed description of the incident location
    Latitude REAL,                          -- Latitude coordinate of the incident location
    Longitude REAL,                         -- Longitude coordinate of the incident location
    Claim_Status VARCHAR(50),               -- Current status of the claim (e.g., Open, Closed - Settled)
    Settlement_Amount REAL,                 -- Amount paid in settlement, if applicable
    Legal_Costs REAL,                       -- Legal expenses incurred for the claim
    Allegation_Details TEXT                 -- Detailed textual description of the allegation
);

-- Add indexes to frequently queried columns for improved performance.
-- These indexes will speed up searches and joins based on these columns.
CREATE INDEX IF NOT EXISTS idx_incident_date ON claims (Date_of_Incident);
CREATE INDEX IF NOT EXISTS idx_division ON claims (City_Division_Involved);
CREATE INDEX IF NOT EXISTS idx_incident_type ON claims (Incident_Type);
CREATE INDEX IF NOT EXISTS idx_claim_status ON claims (Claim_Status);