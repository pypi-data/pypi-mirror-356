# Greenfish

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/greenfish.svg)](https://pypi.org/project/greenfish/)

Greenfish is a desktop application for out-of-band server management using Redfish and IPMI protocols.

![Main Application](images/app.png)

It provides a unified interface for managing server hardware, regardless of vendor, with powerful monitoring and configuration capabilities.

## Features

### Core Functionality
- **Redfish & IPMI Support**: Unified interface for both protocols
- **System Management**: Comprehensive system information and health monitoring
- **Resource Management**: View and configure server components
- **User Account Management**: Create and manage user accounts on managed systems
- **Secure Boot Configuration**: Configure secure boot settings
- **Event Subscription**: Subscribe to and monitor system events
- **Log Management**: View and analyze system logs
- **Configuration Management**: Save, load, and apply system configurations

### Out-of-Band Management
- **IPMI Integration**: Full IPMI protocol support
- **Bare Metal Provisioning**: OS deployment via iPXE
- **Virtual Media Management**: Mount and manage virtual media
- **Remote Console**: KVM and serial console support
- **Hardware Monitoring**: Comprehensive sensor management

### User Interface
- **Modern Design**: Clean, responsive interface with dark/light theme support
- **Dashboard**: System health overview and resource utilization displays
- **Navigation**: Intuitive resource navigation
- **Property Panels**: Detailed resource information with editable properties

## Installation

### From PyPI
```bash
pip install greenfish
```

### From Source
```bash
git clone https://github.com/mexyusef/greenfish.git
cd greenfish
pip install -e .
```

## Quick Start

```bash
# Launch the application
greenfish

# Or with command line options
greenfish --config /path/to/config
```

## Documentation

Comprehensive documentation is available at [https://greenfish.readthedocs.io](https://greenfish.readthedocs.io)

## Requirements

- Python 3.8+
- PyQt5 or PySide2
- Additional dependencies listed in requirements.txt

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/mexyusef/greenfish.git
cd greenfish

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The Redfish Forum for the Redfish API specification
- The IPMI Forum for the IPMI specification
- All contributors who have helped with the project
