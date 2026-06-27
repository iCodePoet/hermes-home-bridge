---
name: hermes_home_bridge
description: "Get real-time room temperature and humidity from Arduino DHT11/22 sensor."
version: 1.0.0
author: user
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [IoT, Sensor, Smart-Home, Temperature, Humidity]
---

# hermes-home-bridge Skill

Get current temperature and humidity of the room from the connected microcontroller board with a DHT sensor.

## When to Use

- "What is the current room temperature?"
- "Tell me the indoor temperature/humidity right now."
- "현재 방 온도(혹은 습도)가 몇이야?"
- "지금 실내 온도/습도 알려줘"

## Common Commands

### Get Room Temperature and Humidity

Run the bridge script with the `--once` option to retrieve the sensor values in JSON format.

```bash
# Run this command in your local project directory
uv run src/serial_bridge.py --once
```

Example Output:
```json
{"temperature": 27.30, "humidity": 6.00}
```

The output is printed to stdout in JSON. Parse this JSON and reply to the user with the temperature in Celsius (°C) and humidity in percent (%).
