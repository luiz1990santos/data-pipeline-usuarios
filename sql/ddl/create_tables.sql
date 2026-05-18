
---------------------------
-- DB - ANALYTICS_HUB     |
---------------------------

-- CREATE DATABASE ANALYTICS_HUB;

-- USE ANALYTICS_HUB;

-- SP_HELP STAGING_USERS

CREATE TABLE STAGING_USERS(
    ID VARCHAR(50) PRIMARY KEY, 	
    first_name VARCHAR(50),	
    last_name VARCHAR(50),	
    gender VARCHAR(50),	
    email VARCHAR(50),	
    street VARCHAR(50),	
    number VARCHAR(50),	
    city VARCHAR(50),	
    state VARCHAR(50),	
    country VARCHAR(50),	
    latitude VARCHAR(50),	
    longitude VARCHAR(50),	
    date_of_birth VARCHAR(50),	
    age VARCHAR(50),	
    registration_date VARCHAR(50),	
    regist_age VARCHAR(50)

) ;