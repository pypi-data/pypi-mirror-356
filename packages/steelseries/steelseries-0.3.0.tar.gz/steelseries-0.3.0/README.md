# steelseries

A simple wrapper for the SteelSeries GameSense API in Python.

## Features

- Register games and events with SteelSeries Engine
- Send live event data (0–100) to control RGB devices
- Built-in auto-sanitization of names

## Example

```python
# import
import steelseries as ss

# register game
ss.register_game("TESTING", "NEO", "TESTING DEMO", 1)

# register event
ss.register_event("TESTING", "HEALTH")

# animate the lighting - bounce in from 0 to 100 in 1 second
ss.send_event_data_interpolated("TESTING", "HEALTH", 0, 100, 1, 0.01, "bounce_in", True)

# send in background to not halt app - will flicker if more than 1 command is run at the same time
ss.send_event_data_interpolated_async("TESTING", "HEALTH", 100, 50, 0.5, 0.01, "ease-in", True) 
ss.send_event_data_interpolated("TESTING", "HEALTH", 100, 0, 0.5, 0.01, "ease-in", True)

# send single value, 50%
ss.send_event_data("TESTING", "HEALTH", 50, True) # wait until done to put 50%
```
