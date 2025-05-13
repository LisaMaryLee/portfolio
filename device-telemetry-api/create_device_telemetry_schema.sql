-- Create the main telemetry database (if it doesn't already exist)
CREATE DATABASE IF NOT EXISTS stack_REST;
USE stack_REST;

-- Table 1: General system-level configuration data per appliance
CREATE TABLE IF NOT EXISTS ss_general (
    SID VARCHAR(32) PRIMARY KEY,  -- Unique system identifier
    ss_software_version VARCHAR(20) NOT NULL,  -- Installed software version
    model_number VARCHAR(50) NOT NULL,  -- Product model number
    time_zone VARCHAR(50) NOT NULL,  -- Time zone of the device
    locale VARCHAR(50) NOT NULL,  -- Regional/language setting
    dock_firmware_version VARCHAR(20) NOT NULL,  -- Firmware version for connected docks
    dock_qty INT NOT NULL,  -- Total number of docks connected
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- Tracks latest update timestamp
);

-- Table 2: Metadata for each cartridge inserted into the system
CREATE TABLE IF NOT EXISTS ss_cartridge_information (
    cartridge_ID BIGINT PRIMARY KEY,  -- Unique cartridge identifier
    SID VARCHAR(32) NOT NULL,  -- Associated system ID
    vendor VARCHAR(100) NOT NULL,  -- Manufacturer of the cartridge
    model VARCHAR(100) NOT NULL,  -- Cartridge model
    status VARCHAR(50) NOT NULL,  -- Status (e.g., OK, failed, degraded)
    encrypted_status VARCHAR(10) NOT NULL,  -- Whether cartridge is encrypted (e.g., 1/0 or Yes/No)
    load_count INT NOT NULL,  -- Number of times the cartridge was loaded
    cartridge_type VARCHAR(20) NOT NULL,  -- Type (e.g., HDD, SSD, RDX)
    write_protect VARCHAR(10) NOT NULL,  -- Write protection status
    temperature INT NOT NULL,  -- Temperature in Celsius
    capacity_GB FLOAT NOT NULL,  -- Total capacity in GB
    free_space_GB FLOAT NOT NULL,  -- Free space remaining in GB
    GB_read FLOAT NOT NULL,  -- Total GB read from cartridge
    GB_written FLOAT NOT NULL,  -- Total GB written to cartridge
    usage_free INT NOT NULL,  -- Percent of space free
    usage_threshold INT NOT NULL,  -- Warning threshold percentage
    partition_count INT NOT NULL,  -- Number of partitions on cartridge
    link_speed VARCHAR(20) NOT NULL,  -- SATA/SAS/NVMe link speed
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Record creation time
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- Record update time
);

-- Table 3: Partition-level metadata for each cartridge
CREATE TABLE IF NOT EXISTS ss_cartridge_partition (
    cartridge_ID VARCHAR(64) NOT NULL,  -- Cartridge this partition belongs to
    SID VARCHAR(32) NOT NULL,  -- Associated system ID
    offset VARCHAR(64) NOT NULL,  -- Offset on the media
    disk_label VARCHAR(64) NOT NULL,  -- Human-readable label
    partition_number INT NOT NULL,  -- Partition number
    file_system_type VARCHAR(64) NOT NULL,  -- e.g., NTFS, ext4, FAT32
    partition_type VARCHAR(128) NOT NULL,  -- GUID or legacy type descriptor
    size_remaining VARCHAR(64) NOT NULL,  -- Free space left in this partition
    size VARCHAR(64) NOT NULL,  -- Total size of this partition
    threshold VARCHAR(64) NOT NULL,  -- Usage warning threshold
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Record creation time
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Record update time
    PRIMARY KEY (cartridge_ID, partition_number)  -- Composite key ensures unique partition per cartridge
);

-- Table 4: Inventory of drives present in the system
CREATE TABLE IF NOT EXISTS ss_harddriveinventory (
    SID VARCHAR(32) NOT NULL,  -- System ID
    host_ID VARCHAR(32) NOT NULL,  -- Physical or logical host ID
    HardDriveModelNumber VARCHAR(128) NOT NULL,  -- Model string from drive
    HardDriveFirmwareRevision VARCHAR(64) NOT NULL,  -- Reported firmware version
    HardDriveCapacity VARCHAR(64) NOT NULL,  -- Capacity (raw or human-readable)
    DriveType VARCHAR(16) NOT NULL,  -- hdd, ssd, nvme, etc.
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Record update time
    PRIMARY KEY (SID, host_ID, HardDriveModelNumber)  -- Composite key tracks drive across systems
);
