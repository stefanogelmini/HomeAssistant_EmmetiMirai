# Template Setup Guide for Hourly Setpoints

## Introduction
This document serves as a comprehensive guide to configuring templates for hourly setpoints in the Home Assistant Emmeti Mirai integration.

## Prerequisites
Before you start, ensure that you have the following:
- A running instance of Home Assistant.
- Access to the configuration.yaml file or relevant files depending on your setup.
- Familiarity with YAML syntax.

## Setting Up Hourly Setpoints
### Step 1: Define the Input Number
First, you need to define the input number that will hold your hourly setpoints. Add this to your configuration.yaml:

```yaml
input_number:
  hourly_setpoint:
    name: Hourly Setpoint
    min: 0
    max: 30
    step: 1
```

### Step 2: Create a Template Sensor
Next, create a template sensor that will dynamically adjust according to the time of day. Add the following to your sensors.yaml:

```yaml
template:
  - sensor:
      - name: "Current Hour Setpoint"
        state: >
          {% set hour = now().hour %}
          {% if hour == 0 %} 20 {% elif hour == 1 %} 21 {% elif hour == 2 %} 22 {% endif %}
```

### Step 3: Automate Setpoints
You can automate your setpoints based on the current hour. Add the following automation:

```yaml
automation:
  - alias: Set Hourly Temperature
    trigger:
      platform: time
      minutes: '/30'
    action:
      service: climate.set_temperature
      data:
        entity_id: climate.your_climate_entity
        temperature: "{{ states('sensor.current_hour_setpoint') }}"
```

## Final Thoughts
Make sure to check your configuration for errors by using the configuration check tool in Home Assistant. Restart your Home Assistant instance to apply the changes.

This guide should help you set up hourly setpoints effectively. For further assistance, refer to the Home Assistant documentation or community forums.

## Additional Resources
- [Home Assistant Documentation](https://www.home-assistant.io/docs/)
- [YAML Syntax](https://yaml.org/spec/)

---