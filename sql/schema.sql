/*
==============================================================================
CHICAGO CITY LIABILITY ANALYSIS - DATABASE SCHEMA DEFINITION
==============================================================================

Purpose: Defines the comprehensive database structure for Chicago municipal 
         liability claims management and analytics.

Geographic Focus: Chicago, Illinois metropolitan area
Municipal Context: Chicago city divisions and operations

This schema supports:
- Comprehensive Chicago claim lifecycle tracking
- Financial impact analysis and reporting for Chicago
- Geospatial risk analysis and mapping within Chicago boundaries
- Chicago municipal operational performance monitoring
- Advanced analytics and business intelligence for Chicago city management

Author: Data Engineering Team
Date: July 2025
Project: City Liability Analytics
Database: SQLite 3.x
==============================================================================
*/

-- ==============================================================================
-- MAIN CLAIMS TABLE - COMPREHENSIVE LIABILITY DATA REPOSITORY
-- ==============================================================================

CREATE TABLE IF NOT EXISTS claims (
    -- PRIMARY IDENTIFICATION
    Claim_ID VARCHAR(50) PRIMARY KEY,        -- Unique identifier for each liability claim
                                             -- Format: Alphanumeric string for tracking
    
    -- TEMPORAL TRACKING FIELDS
    Date_of_Incident DATE,                  -- Date when the actual incident occurred
                                           -- Critical for trend analysis and statute of limitations
    Date_Claim_Filed DATE,                 -- Date when formal claim was submitted to city
                                          -- Used for processing time calculations
    
    -- INCIDENT CLASSIFICATION
    Incident_Type VARCHAR(100),             -- Standardized incident category
                                           -- Examples: 'Slip & Fall', 'Vehicle Damage', 'Property Damage'
                                           -- Enables risk pattern analysis
    Alleged_Cause VARCHAR(255),             -- Specific alleged cause of the incident
                                           -- Detailed classification for root cause analysis
    
    -- ORGANIZATIONAL CONTEXT
    City_Division_Involved VARCHAR(100),    -- Municipal department/division associated with incident
                                           -- Critical for accountability and budget allocation
                                           -- Examples: 'Public Works', 'Parks & Recreation'
    
    -- GEOSPATIAL DATA FOR RISK MAPPING
    Location_Details TEXT,                  -- Human-readable location description
                                           -- Provides context for incident location
    Latitude REAL,                         -- Geographic latitude coordinate (decimal degrees)
                                          -- Enables geospatial analysis and risk mapping
    Longitude REAL,                        -- Geographic longitude coordinate (decimal degrees)
                                          -- Combined with latitude for precise location analysis
    
    -- CLAIM LIFECYCLE MANAGEMENT
    Claim_Status VARCHAR(50),               -- Current processing status of the claim
                                           -- Values: 'Open', 'Under Investigation', 'Closed - Settled',
                                           --         'Closed - Denied', 'Closed - Withdrawn'
                                           -- Essential for operational workflow tracking
    
    -- FINANCIAL IMPACT TRACKING
    Settlement_Amount REAL,                 -- Total monetary settlement paid to claimant
                                           -- Core metric for financial exposure analysis
    Legal_Costs REAL,                      -- Legal fees and expenses incurred by city
                                          -- Important for total cost of claims assessment
    
    -- DETAILED DOCUMENTATION
    Allegation_Details TEXT                 -- Comprehensive textual description of allegations
                                           -- Source for NLP analysis and pattern recognition
                                           -- Critical for understanding incident circumstances
);

-- ==============================================================================
-- PERFORMANCE OPTIMIZATION INDEXES
-- ==============================================================================

-- Temporal Analysis Index - Optimizes date-based queries and trend analysis
CREATE INDEX IF NOT EXISTS idx_incident_date ON claims (Date_of_Incident);

-- Organizational Analysis Index - Speeds up division-based reporting
CREATE INDEX IF NOT EXISTS idx_division ON claims (City_Division_Involved);

-- Risk Classification Index - Enhances incident type analysis performance
CREATE INDEX IF NOT EXISTS idx_incident_type ON claims (Incident_Type);

-- Workflow Management Index - Optimizes status-based queries
CREATE INDEX IF NOT EXISTS idx_claim_status ON claims (Claim_Status);

-- Financial Analysis Index - Improves cost-based query performance
CREATE INDEX IF NOT EXISTS idx_settlement_amount ON claims (Settlement_Amount);

-- Geospatial Analysis Index - Enhances location-based queries
CREATE INDEX IF NOT EXISTS idx_coordinates ON claims (Latitude, Longitude);

-- Composite Index for Complex Analytics - Optimizes multi-dimensional analysis
CREATE INDEX IF NOT EXISTS idx_division_incident_date ON claims (City_Division_Involved, Incident_Type, Date_of_Incident);

/*
==============================================================================
SCHEMA DESIGN NOTES
==============================================================================

DATA TYPES RATIONALE:
- VARCHAR lengths chosen to accommodate realistic municipal data
- REAL type for financial amounts supports decimal precision
- TEXT for detailed descriptions allows unlimited content
- DATE type ensures proper temporal sorting and analysis

INDEXING STRATEGY:
- Single-column indexes for common filter conditions
- Composite indexes for complex analytical queries
- Geospatial index for mapping and location analysis
- Financial indexes for cost and settlement analysis

PERFORMANCE CONSIDERATIONS:
- Indexes balance query speed with insert/update performance
- Index selection based on expected query patterns
- Composite indexes support complex analytical workloads

SCALABILITY FEATURES:
- Schema supports millions of records
- Efficient indexing for large-scale analytics
- Flexible text fields for varied municipal contexts
- Extensible design for additional fields

==============================================================================
*/