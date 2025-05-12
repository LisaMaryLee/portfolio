-- Create database
CREATE DATABASE IF NOT EXISTS stack_REST;
USE stack_REST;

-- Table 1: General System Information
CREATE TABLE IF NOT EXISTS ss_general (
    SID VARCHAR(32) PRIMARY KEY,
    ss_software_version VARCHAR(20) NOT NULL,
    model_number VARCHAR(50) NOT NULL,
    time_zone VARCHAR(50) NOT NULL,
    locale VARCHAR(50) NOT NULL,
    dock_firmware_version VARCHAR(20) NOT NULL,
    dock_qty INT NOT NULL,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table 2: Cartridge Information
CREATE TABLE IF NOT EXISTS ss_cartridge_information (
    cartridge_ID BIGINT PRIMARY KEY,
    SID VARCHAR(32) NOT NULL,
    vendor VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    encrypted_status VARCHAR(10) NOT NULL,
    load_count INT NOT NULL,
    cartridge_type VARCHAR(20) NOT NULL,
    write_protect VARCHAR(10) NOT NULL,
    temperature INT NOT NULL,
    capacity_GB FLOAT NOT NULL,
    free_space_GB FLOAT NOT NULL,
    GB_read FLOAT NOT NULL,
    GB_written FLOAT NOT NULL,
    usage_free INT NOT NULL,
    usage_threshold INT NOT NULL,
    partition_count INT NOT NULL,
    link_speed VARCHAR(20) NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table 3: Cartridge Partition Information
CREATE TABLE IF NOT EXISTS ss_cartridge_partition (
    cartridge_ID VARCHAR(64) NOT NULL,
    SID VARCHAR(32) NOT NULL,
    offset VARCHAR(64) NOT NULL,
    disk_label VARCHAR(64) NOT NULL,
    partition_number INT NOT NULL,
    file_system_type VARCHAR(64) NOT NULL,
    partition_type VARCHAR(128) NOT NULL,
    size_remaining VARCHAR(64) NOT NULL,
    size VARCHAR(64) NOT NULL,
    threshold VARCHAR(64) NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (cartridge_ID, partition_number)
);

-- Table 4: Hard Drive Inventory
CREATE TABLE IF NOT EXISTS ss_harddriveinventory (
    SID VARCHAR(32) NOT NULL,
    host_ID VARCHAR(32) NOT NULL,
    HardDriveModelNumber VARCHAR(128) NOT NULL,
    HardDriveFirmwareRevision VARCHAR(64) NOT NULL,
    HardDriveCapacity VARCHAR(64) NOT NULL,
    DriveType VARCHAR(16) NOT NULL,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (SID, host_ID, HardDriveModelNumber)
);
