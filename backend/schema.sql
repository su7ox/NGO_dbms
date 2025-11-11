-- This script contains the complete database structure for the NGO Management System.
-- To use:
-- 1. Create a new database in PostgreSQL (e.g., CREATE DATABASE ngo_db;)
-- 2. Connect to that database.
-- 3. Run this entire script.

-- ========= 1. AUTHENTICATION & CORE PROFILES =========

CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK(role IN ('Owner', 'Worker', 'Donor', 'Volunteer')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Donors (
    donor_id SERIAL PRIMARY KEY,
    user_id INT UNIQUE REFERENCES Users(user_id) ON DELETE SET NULL,
    donor_name VARCHAR(150) NOT NULL,
    donor_type VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(20),
    address TEXT,
    registration_date DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE Volunteers (
    volunteer_id SERIAL PRIMARY KEY,
    user_id INT UNIQUE REFERENCES Users(user_id) ON DELETE SET NULL,
    volunteer_name VARCHAR(150) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(20),
    skills TEXT,
    join_date DATE NOT NULL DEFAULT CURRENT_DATE
);

-- ========= 2. CAMPAIGNS & OPERATIONS =========

CREATE TABLE Campaigns (
    campaign_id SERIAL PRIMARY KEY,
    campaign_name VARCHAR(200) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    goal_amount DECIMAL(12, 2),
    status VARCHAR(20)
);

CREATE TABLE Events (
    event_id SERIAL PRIMARY KEY,
    event_name VARCHAR(200) NOT NULL,
    description TEXT,
    location VARCHAR(255),
    event_date TIMESTAMP
);

CREATE TABLE Tasks (
    task_id SERIAL PRIMARY KEY,
    event_id INT REFERENCES Events(event_id) ON DELETE SET NULL,
    task_name VARCHAR(150) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'To Do'
);

CREATE TABLE Volunteer_Assignments (
    assignment_id SERIAL PRIMARY KEY,
    volunteer_id INT NOT NULL REFERENCES Volunteers(volunteer_id) ON DELETE CASCADE,
    task_id INT NOT NULL REFERENCES Tasks(task_id) ON DELETE CASCADE,
    assignment_date DATE DEFAULT CURRENT_DATE,
    notes TEXT
);

-- ========= 3. TRANSACTIONS & RESOURCE FLOW =========

CREATE TABLE Donations (
    donation_id SERIAL PRIMARY KEY,
    donor_id INT REFERENCES Donors(donor_id) ON DELETE SET NULL,
    campaign_id INT REFERENCES Campaigns(campaign_id) ON DELETE SET NULL,
    donation_date DATE NOT NULL DEFAULT CURRENT_DATE,
    donation_type VARCHAR(20) NOT NULL,
    cash_amount DECIMAL(10, 2),
    notes TEXT
);

CREATE TABLE Donation_Items (
    item_id SERIAL PRIMARY KEY,
    donation_id INT NOT NULL REFERENCES Donations(donation_id) ON DELETE CASCADE,
    item_name VARCHAR(100) NOT NULL,
    item_category VARCHAR(50),
    quantity INT NOT NULL,
    unit VARCHAR(20)
);

CREATE TABLE Beneficiaries (
    beneficiary_id SERIAL PRIMARY KEY,
    beneficiary_name VARCHAR(200) NOT NULL,
    beneficiary_type VARCHAR(20),
    contact_info TEXT,
    description TEXT
);

CREATE TABLE Distributions (
    distribution_id SERIAL PRIMARY KEY,
    beneficiary_id INT NOT NULL REFERENCES Beneficiaries(beneficiary_id) ON DELETE CASCADE,
    item_name VARCHAR(100) NOT NULL,
    quantity_distributed INT NOT NULL,
    distribution_date DATE NOT NULL
);

CREATE TABLE Expenses (
    expense_id SERIAL PRIMARY KEY,
    campaign_id INT REFERENCES Campaigns(campaign_id) ON DELETE SET NULL,
    expense_category VARCHAR(50) NOT NULL,
    description TEXT,
    amount DECIMAL(10, 2) NOT NULL,
    expense_date DATE NOT NULL,
    receipt_url VARCHAR(255)
);
