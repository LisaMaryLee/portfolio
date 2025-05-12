from flask_restx import fields

columns = {
    'ss_general': [
        'SID', 'ss_software_version', 'model_number', 'time_zone', 'locale',
        'dock_firmware_version', 'dock_qty'
    ],
    'ss_cartridge_information': [
        'cartridge_ID', 'SID', 'vendor', 'model', 'status', 'encrypted_status',
        'load_count', 'cartridge_type', 'write_protect', 'temperature', 'capacity_GB',
        'free_space_GB', 'GB_read', 'GB_written', 'usage_free', 'usage_threshold',
        'partition_count', 'link_speed'
    ],
    'ss_cartridge_partition': [
        'cartridge_ID', 'SID', 'offset', 'disk_label', 'partition_number',
        'file_system_type', 'partition_type', 'size_remaining', 'size', 'threshold'
    ],
    'ss_harddriveinventory': [
        'SID', 'host_ID', 'HardDriveModelNumber', 'HardDriveFirmwareRevision', 'HardDriveCapacity', 'DriveType'
    ]
}

# Define the Swagger models for the tables
ss_general_model = {
    'SID': fields.String(required=True, description='The unique identifier', example="3659890703846945"),
    'ss_software_version': fields.String(required=True, description='Software version', example="X.2.6"),
    'model_number': fields.String(required=True, description='Model number', example="qs4v2"),
    'time_zone': fields.String(required=True, description='Time zone', example="UTC"),
    'locale': fields.String(required=True, description='Locale', example="English (United States)"),
    'dock_firmware_version': fields.String(required=True, description='Dock firmware version', example="18"),
    'dock_qty': fields.Integer(required=True, description='Quantity of docks', example=4)
}

ss_cartridge_information_model = {
    'cartridge_ID': fields.Integer(required=True, description='Cartridge ID', example=321654900),
    'SID': fields.String(required=True, description='The unique identifier', example="3659890703846945"),
    'vendor': fields.String(required=True, description='Vendor name', example="Vendor1"),
    'model': fields.String(required=True, description='Model name', example="ApplianceModel1"),
    'status': fields.String(required=True, description='Status of the cartridge', example="Good"),
    'encrypted_status': fields.String(required=True, description='Encryption status', example="0"),
    'load_count': fields.Integer(required=True, description='Load count', example=25),
    'cartridge_type': fields.String(required=True, description='Type of cartridge', example="HDD"),
    'write_protect': fields.String(required=True, description='Write protection status', example="0"),
    'temperature': fields.Integer(required=True, description='Temperature', example=30),
    'capacity_GB': fields.Float(required=True, description='Capacity in GB', example=500.5),
    'free_space_GB': fields.Float(required=True, description='Free space in GB', example=250.25),
    'GB_read': fields.Float(required=True, description='GB read', example=100.75),
    'GB_written': fields.Float(required=True, description='GB written', example=200.5),
    'usage_free': fields.Integer(required=True, description='Usage free percentage', example=75),
    'usage_threshold': fields.Integer(required=True, description='Usage threshold percentage', example=80),
    'partition_count': fields.Integer(required=True, description='Number of partitions', example=3),
    'link_speed': fields.String(required=True, description='Link speed', example="6Gbps")
}
ss_cartridge_partition_model = {
    'cartridge_ID': fields.String(required=True, description='Cartridge ID', example=321654900),
    'SID': fields.String(required=True, description='The unique identifier', example="3659890703846945"),
    'offset': fields.String(required=True, description='Offset', example="0x00000000"),
    'disk_label': fields.String(required=True, description='Disk label', example="Disk2"),
    'partition_number': fields.Integer(required=True, description='Partition number', example=1),
    'file_system_type': fields.String(required=True, description='File system type', example="NTFS"),
    'partition_type': fields.String(required=True, description='Partition type', example="EBD0A0A2-B9E5-4433-87C0-68B6B72699C7"),
    'size_remaining': fields.String(required=True, description='Size remaining', example="100GB"),
    'size': fields.String(required=True, description='Size', example="500GB"),
    'threshold': fields.String(required=True, description='Threshold', example="80%")
}

ss_harddriveinventory_model = {
    'SID': fields.String(required=True, description='The unique identifier', example="3659890703846945"),
    'host_ID': fields.String(required=True, description='Host ID', example="1234567890123456"),
    'HardDriveModelNumber': fields.String(required=True, description='Hard Drive Model Number', example="FUJITSU MHX2300BT"),
    'HardDriveFirmwareRevision': fields.String(required=True, description='Hard Drive Firmware Revision', example="0000000B"),
    'HardDriveCapacity': fields.String(required=True, description='Hard Drive Capacity', example="300069052416"),
    'DriveType': fields.String(required=True, description='Drive Type', example="hdd")
}

# Table configurations indicating whether to use insert-only or insert-or-replace
table_config = {
    'ss_general': 'insert_or_replace',
    'ss_harddriveinventory': 'insert_or_replace',
    'ss_cartridge_information': 'insert',
    'ss_cartridge_partition': 'insert'
}

# Map table names to their respective Swagger models
models = {
    'ss_general': ss_general_model,
    'ss_cartridge_information': ss_cartridge_information_model,
    'ss_cartridge_partition': ss_cartridge_partition_model,
    'ss_harddriveinventory': ss_harddriveinventory_model
}

