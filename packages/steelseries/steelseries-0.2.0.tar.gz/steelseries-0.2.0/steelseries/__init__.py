# steelseries.py

import os
import json
import re
import requests

# Read SteelSeries Engine address from coreProps.json
def get_sse_address(silent=False):
    """
    silent
    """
    try:
        program_data = os.getenv('PROGRAMDATA')
        core_props_path = os.path.join(program_data, 'SteelSeries', 'SteelSeries Engine 3', 'coreProps.json')
        with open(core_props_path, 'r') as f:
            return json.load(f).get("address", "")
    except Exception as e:
        if not silent:
            print(f"[Error] Could not load coreProps.json: {e}")
        return ""

# Store address once at module level
sse_address = get_sse_address(silent=True)


# Helper to sanitize names
def sanitize_name(name, label="name", silent=False):
    original = name
    name = re.sub(r"[^A-Z0-9_-]", "_", name.upper())
    if name != original and not silent:
        print(f"[WARNING] Invalid {label} '{original}' auto-fixed to '{name}'")
        print("[WARNING] Allowed characters: uppercase A-Z, 0-9, hyphen (-), underscore (_)")
    return name


# Register a game/app with SteelSeries Engine
def register_game(gamename="DEMO", developer="NeoEmberArts", displayname="Demo App", iconcolorid=1, silent=False):
    """
    game name, developer, displayname, iconcolorid, silent
    """
    if not sse_address:
        if not silent:
            print("SteelSeries Engine address not found.")
        return

    gamename = sanitize_name(gamename, "gamename", silent=silent)

    app_data = {
        "game": gamename,
        "game_display_name": displayname,
        "developer": developer,
        "icon_color_id": iconcolorid
    }

    try:
        response = requests.post(f"http://{sse_address}/game_metadata", json=app_data)
        response.raise_for_status()
        if not silent:
            print("[OK] Game registered.")
    except requests.exceptions.HTTPError as http_err:
        if not silent:
            print(f"[HTTP Error] {http_err.response.status_code}: {http_err.response.text}")
    except Exception as e:
        if not silent:
            print(f"[Error] Failed to register game: {e}")


# Register an event for the game
def register_event(gamename="DEMO", eventname="EVENT", silent=False):
    """
    game name, event name, silent
    """
    if not sse_address:
        if not silent:
            print("SteelSeries Engine address not found.")
        return

    gamename = sanitize_name(gamename, "gamename", silent=silent)
    eventname = sanitize_name(eventname, "eventname", silent=silent)

    event_data = {
        "game": gamename,
        "event": eventname,
        "min_value": 0,
        "max_value": 100,
        "icon_id": 1
    }

    try:
        response = requests.post(f"http://{sse_address}/register_game_event", json=event_data)
        response.raise_for_status()
        if not silent:
            print(f"[OK] Event '{eventname}' registered successfully under game '{gamename}'.")
    except requests.exceptions.HTTPError as http_err:
        if not silent:
            print(f"[HTTP Error] {http_err.response.status_code}: {http_err.response.text}")
    except Exception as e:
        if not silent:
            print(f"[Error] Failed to register event: {e}")


# Send data to a registered event
def send_event_data(gamename="DEMO", eventname="EVENT", value=50, silent=False):
    """
    game name, event name, value, silent
    """
    if not sse_address:
        if not silent:
            print("SteelSeries Engine address not found.")
        return

    gamename = sanitize_name(gamename, "gamename", silent=silent)
    eventname = sanitize_name(eventname, "eventname", silent=silent)

    payload = {
        "game": gamename,
        "events": [{
            "event": eventname,
            "data": {"value": value}
        }]
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(f"http://{sse_address}/multiple_game_events", data=json.dumps(payload), headers=headers)
        if response.status_code != 200:
            if not silent:
                print(f"[ERROR] Failed to send event data: {response.status_code} - {response.text}")
        else:
            if not silent:
                print(f"[OK] Event data sent for '{eventname}' with value {value}.")
    except Exception as e:
        if not silent:
            print(f"[Error] Exception occurred while sending event data: {e}")




import time
import math

def apply_easing(t, easing):
    # t is normalized between 0 and 1
    if easing == "linear":
        return t
    elif easing == "ease-in":
        return t * t
    elif easing == "ease-out":
        return t * (2 - t)
    elif easing == "ease-in-out":
        return 0.5 * (math.sin((t - 0.5) * math.pi) + 1)
    else:
        return t  # fallback to linear


def send_event_data_interpolated(
    gamename="DEMO",
    eventname="EVENT",
    start_value=0,
    end_value=100,
    duration=5.0,
    interval=0.5,
    easing="linear",  # NEW
    silent=False
):
    """
    game name, event name, start, stop, durration, interval, easing, silent
    easing styles: 
        • "linear" (default)
        • "ease-in"
        • "ease-out"
        • "ease-in-out"
    """
    if not sse_address:
        if not silent:
            print("SteelSeries Engine address not found.")
        return

    gamename = sanitize_name(gamename, "gamename", silent=silent)
    eventname = sanitize_name(eventname, "eventname", silent=silent)

    steps = max(int(duration / interval), 1)

    for i in range(steps + 1):
        t = i / steps  # normalized time (0.0 to 1.0)
        eased_t = apply_easing(t, easing)
        value = start_value + (end_value - start_value) * eased_t
        send_event_data(gamename, eventname, int(round(value)), silent=silent)
        time.sleep(interval)

    if not silent:
        print(f"[OK] Interpolated data sent from {start_value} to {end_value} over {duration}s using '{easing}'.")



# Show help for available functions
def help(silent=False):
    if silent:
        return
    print("""
steelseries.py - SteelSeries GameSense Integration

Functions:
-----------
register_game(gamename="DEMO", developer="NeoEmberArts", displayname="Demo App", iconcolorid=1, silent=False)
    - Registers a game/app with SteelSeries Engine.
    - gamename must contain only A-Z, 0-9, -, _ (auto-fixed if not).

register_event(gamename="DEMO", eventname="EVENT", silent=False)
    - Registers an event for the game.
    - You must register the game before calling this.
    - Event names must follow the same character rules (auto-fixed if not).

send_event_data(gamename="DEMO", eventname="EVENT", value=50, silent=False)
    - Sends a value to the given event (0–100 recommended).
    - Used to update devices like RGB keyboards, OLEDs, etc.

send_event_data_interpolated(gamename="DEMO", eventname="EVENT",
                             start_value=0, end_value=100,
                             duration=5.0, interval=0.5,
                             easing="linear", silent=False)
    - Smoothly interpolates from start_value to end_value over time.
    - Sends updates every `interval` seconds for `duration` seconds.
    - Supported easing styles:
        • "linear" (default)
        • "ease-in"
        • "ease-out"
        • "ease-in-out"
    - Great for smooth animations or transitions.

help(silent=False) # silent parameter here is super useful ;)
    - Shows this help text.

Usage Examples:
--------------
import steelseries

#-- register game --#
steelseries.register_game("MYGAME", "Developer", "Display", 1, True) # True == no debugging
          
#-- register event --#
steelseries.register_event("MYGAME", "HEALTH", False) # False or empty == debugging
          
#-- single update -- #
steelseries.send_event_data("MYGAME", "HEALTH", 75, True)
          
#-- animated update --#
steelseries.send_event_data_interpolated("MYGAME", "HEALTH", 0, 100, 3.0, 0.1, easing="ease-in", silent=False)
--------------
""")
    



