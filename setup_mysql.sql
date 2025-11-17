-- MySQL Setup Script for HRMS Location Tracking
-- Run this script to create database and user

-- Create database
CREATE DATABASE IF NOT EXISTS hrms_location_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Create user (optional - you can use root)
CREATE USER IF NOT EXISTS 'hrms_user'@'localhost' IDENTIFIED BY 'hrms_password_123';

-- Grant all privileges on the database
GRANT ALL PRIVILEGES ON hrms_location_db.* TO 'hrms_user'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;

-- Show databases to verify
SHOW DATABASES;

-- Select the database
USE hrms_location_db;

-- Show message
SELECT 'Database hrms_location_db created successfully!' AS Status;
