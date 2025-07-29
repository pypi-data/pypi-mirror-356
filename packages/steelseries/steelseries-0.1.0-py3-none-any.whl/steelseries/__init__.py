# steelseries.py

import os
import json
import re
import requests

# Read SteelSeries Engine address from coreProps.json
def get_sse_address():
    try:
        program_data = os.getenv('PROGRAMDATA')
        core_props_path = os.path.join(program_data, 'SteelSeries', 'SteelSeries Engine 3', 'coreProps.json')
        with open(core_props_path, 'r') as f:
            return json.load(f).get("address", "")
    except Exception as e:
        print(f"[Error] Could not load coreProps.json: {e}")
        return ""

# Store address once at module level
sse_address = get_sse_address()


# Helper to sanitize names
def sanitize_name(name, label="name"):
    original = name
    name = re.sub(r"[^A-Z0-9_-]", "_", name.upper())
    if name != original:
        print(f"[WARNING] Invalid {label} '{original}' auto-fixed to '{name}'")
        print("[WARNING] Allowed characters: uppercase A-Z, 0-9, hyphen (-), underscore (_)")
    return name


# Register a game/app with SteelSeries Engine
def register_game(gamename="DEMO", developer="NeoEmberArts", displayname="Demo App", iconcolorid=1):
    if not sse_address:
        print("SteelSeries Engine address not found.")
        return

    gamename = sanitize_name(gamename, "gamename")

    app_data = {
        "game": gamename,
        "game_display_name": displayname,
        "developer": developer,
        "icon_color_id": iconcolorid
    }

    try:
        response = requests.post(f"http://{sse_address}/game_metadata", json=app_data)
        response.raise_for_status()
        print("[OK] Game registered.")
    except requests.exceptions.HTTPError as http_err:
        print(f"[HTTP Error] {http_err.response.status_code}: {http_err.response.text}")
    except Exception as e:
        print(f"[Error] Failed to register game: {e}")


# Register an event for the game
def register_event(gamename="DEMO", eventname="EVENT"):
    if not sse_address:
        print("SteelSeries Engine address not found.")
        return

    gamename = sanitize_name(gamename, "gamename")
    eventname = sanitize_name(eventname, "eventname")

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
        print(f"[OK] Event '{eventname}' registered successfully under game '{gamename}'.")
    except requests.exceptions.HTTPError as http_err:
        print(f"[HTTP Error] {http_err.response.status_code}: {http_err.response.text}")
    except Exception as e:
        print(f"[Error] Failed to register event: {e}")


# Send data to a registered event
def send_event_data(gamename="DEMO", eventname="EVENT", value=50):
    if not sse_address:
        print("SteelSeries Engine address not found.")
        return

    gamename = sanitize_name(gamename, "gamename")
    eventname = sanitize_name(eventname, "eventname")

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
            print(f"[ERROR] Failed to send event data: {response.status_code} - {response.text}")
        else:
            print(f"[OK] Event data sent for '{eventname}' with value {value}.")
    except Exception as e:
        print(f"[Error] Exception occurred while sending event data: {e}")


# Show help for available functions
def help():
    print("""
steelseries.py - SteelSeries GameSense Integration

Functions:
-----------
register_game(gamename="DEMO", developer="NeoEmberArts", displayname="Demo App", iconcolorid=1)
    - Registers a game/app with SteelSeries Engine.
    - gamename must contain only A-Z, 0-9, -, _ (auto-fixed if not).

register_event(gamename="DEMO", eventname="EVENT")
    - Registers an event for the game.
    - You must register the game before calling this.
    - Event names must follow the same character rules (auto-fixed if not).

send_event_data(gamename="DEMO", eventname="EVENT", value=50)
    - Sends a value to the given event (0–100 recommended).
    - Used to update devices like RGB keyboards, OLEDs, etc.

help()
    - Shows this help text.

Usage Example:
--------------
import steelseries

steelseries.register_game("MYGAME")
steelseries.register_event("MYGAME", "HEALTH")
steelseries.send_event_data("MYGAME", "HEALTH", 75)
""")
