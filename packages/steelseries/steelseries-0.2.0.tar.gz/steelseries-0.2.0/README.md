# steelseries

A simple wrapper for the SteelSeries GameSense API in Python.

## Features

- Register games and events with SteelSeries Engine
- Send live event data (0–100) to control RGB devices
- Built-in auto-sanitization of names

## Example

```python
import steelseries

#-- register game --#
steelseries.register_game("MYGAME", "Developer", "Display", 1, True) # True == no debugging
          
#-- register event --#
steelseries.register_event("MYGAME", "HEALTH", False) # False or empty == debugging
          
#-- single update -- #
steelseries.send_event_data("MYGAME", "HEALTH", 75, True)
          
#-- animated update --#
steelseries.send_event_data_interpolated("MYGAME", "HEALTH", 0, 100, 3.0, 0.1, easing="ease-in", silent=True)
```
