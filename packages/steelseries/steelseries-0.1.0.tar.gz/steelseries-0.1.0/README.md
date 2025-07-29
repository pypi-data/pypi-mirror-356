# steelseries

A simple wrapper for the SteelSeries GameSense API in Python.

## Features

- Register games and events with SteelSeries Engine
- Send live event data (0–100) to control RGB devices
- Built-in auto-sanitization of names

## Example

```python
import steelseries

steelseries.register_game("MYGAME")
steelseries.register_event("MYGAME", "HEALTH")
steelseries.send_event_data("MYGAME", "HEALTH", 75)
```
