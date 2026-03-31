# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-31

### Added
- Initial release of Emmeti Mirai Home Assistant integration
- Full Modbus TCP RTU support for Emmeti Mirai heat pump
- Config flow UI for easy setup
- Support for sensor, binary_sensor, number, select, and switch platforms
- Italian and English translations
- Customizable polling interval (5-3600s)
- Home Assistant UI configuration (no YAML required)
- Comprehensive entity definitions in const.py
- Custom SVG icon for the integration

### Features
- Temperature monitoring (ambient, outlet, inlet, ACS)
- Energy consumption tracking
- COP (Coefficient of Performance) monitoring
- Compressor hour tracking
- Setpoint temperature control
- Comfort/eco mode selection
- Humidity monitoring
- Manual switchable functions (resistor, circulation pump, solar central)
