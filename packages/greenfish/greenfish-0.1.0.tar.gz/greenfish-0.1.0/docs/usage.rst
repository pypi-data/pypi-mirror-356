Usage
=====

Getting Started
--------------

After installing Greenfish, you can launch the application by running:

.. code-block:: bash

    greenfish

This will open the main application window.

Creating a Connection Profile
----------------------------

Before you can manage a server, you need to create a connection profile:

1. Click on the "Connection" menu and select "Manage Profiles"
2. In the Profile Manager dialog, click "Add"
3. Enter the following information:
   - Name: A descriptive name for the profile
   - Base URL: The URL of the Redfish service or IP address of the server
   - Username: The username for authentication
   - Password: The password for authentication
   - Authentication Type: Select the appropriate authentication type
   - Description: Optional description for the profile
4. Click "Save" to create the profile

Connecting to a Server
---------------------

To connect to a server:

1. Click on the "Connection" menu and select "Connect"
2. Select a profile from the dropdown list
3. Click "Connect"

Once connected, the dashboard will display an overview of the server's health and status.

Navigation
---------

The navigation pane on the left side of the application allows you to browse through the available resources:

- System Information: Overview of the system
- Hardware Inventory: Details of hardware components
- Sensor Readings: Current sensor values
- Event Log: System events and alerts
- User Management: User account management
- Virtual Media: Virtual media management
- Network Configuration: Network settings
- Firmware Update: Firmware update interface
- Remote Console: KVM and serial console access
- Secure Boot: Secure boot configuration
- BIOS Settings: BIOS configuration

System Information
----------------

The System Information view provides an overview of the server, including:

- Model and manufacturer
- Serial number
- System health status
- Power state
- Processor and memory information
- Firmware versions

Hardware Inventory
----------------

The Hardware Inventory view allows you to browse through the hardware components of the server:

- Processors
- Memory
- Storage
- Network interfaces
- Power supplies
- Fans

Virtual Media Management
----------------------

The Virtual Media Manager allows you to:

1. Mount virtual media:
   - Click "Mount"
   - Select the media type (ISO, IMG, etc.)
   - Enter the path or URL to the media
   - Click "Mount" to attach the media

2. Unmount media:
   - Select the mounted media in the list
   - Click "Unmount"

3. Eject media:
   - Select the inserted media in the list
   - Click "Eject"

Remote Console
------------

To access the remote console:

1. Navigate to the Remote Console view
2. Select the console type (KVM or Serial)
3. Click "Launch Console"

This will open a new window with the remote console interface.

Command Line Interface
--------------------

Greenfish also provides a command-line interface for automation:

.. code-block:: bash

    # Get system information
    greenfish-cli info --profile <profile_name>

    # Power operations
    greenfish-cli power on --profile <profile_name>
    greenfish-cli power off --profile <profile_name>
    greenfish-cli power reset --profile <profile_name>

    # Get sensor readings
    greenfish-cli sensors --profile <profile_name>

    # Mount virtual media
    greenfish-cli media mount --profile <profile_name> --type iso --url <url>
