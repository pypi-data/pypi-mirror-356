# steelseries.py
import os
import json
import re
import requests
import time
import math

#####################################################
# Read SteelSeries Engine address from coreProps.json
#####################################################
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

#####################################################
# Store address once at module level
#####################################################
sse_address = get_sse_address(silent=True)

#####################################################
# Helper to sanitize names and make them valid
#####################################################
def sanitize_name(name, label="name", silent=False):
    original = name
    name = re.sub(r"[^A-Z0-9_-]", "_", name.upper())
    if name != original and not silent:
        print(f"[WARNING] Invalid {label} '{original}' auto-fixed to '{name}'")
        print("[WARNING] Allowed characters: uppercase A-Z, 0-9, hyphen (-), underscore (_)")
    return name

#####################################################
# Register a game/app with SteelSeries Engine
#####################################################
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

#####################################################
# Register an event for the game
#####################################################
def register_event(gamename="DEMO", eventname="EVENT", silent=False, iconcolorid=1):
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
        "icon_id": iconcolorid, 
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

#####################################################
# Send data to a registered event
#####################################################
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





#####################################################
# helper function for easing
#####################################################
def apply_easing(t, easing="linear"):
    """
    Apply easing function to normalized time value.
    
    Args:
        t (float): Time value normalized between 0 and 1
        easing (str): Easing function name
    
    Returns:
        float: Eased value between 0 and 1
    """
    # Clamp t to [0, 1] range for safety
    t = max(0.0, min(1.0, t))
    
    easing = easing.lower().replace("-", "_").replace(" ", "_")
    
    # Linear
    if easing == "linear":
        return t
    
    # Quadratic
    elif easing == "ease_in" or easing == "quad_in":
        return t * t
    elif easing == "ease_out" or easing == "quad_out":
        return 1 - (1 - t) * (1 - t)
    elif easing == "ease_in_out" or easing == "quad_in_out":
        return 2 * t * t if t < 0.5 else 1 - 2 * (1 - t) * (1 - t)
    
    # Cubic
    elif easing == "cubic_in":
        return t * t * t
    elif easing == "cubic_out":
        return 1 - (1 - t) ** 3
    elif easing == "cubic_in_out":
        return 4 * t * t * t if t < 0.5 else 1 - 4 * (1 - t) ** 3
    
    # Quartic
    elif easing == "quart_in":
        return t * t * t * t
    elif easing == "quart_out":
        return 1 - (1 - t) ** 4
    elif easing == "quart_in_out":
        return 8 * t * t * t * t if t < 0.5 else 1 - 8 * (1 - t) ** 4
    
    # Quintic
    elif easing == "quint_in":
        return t * t * t * t * t
    elif easing == "quint_out":
        return 1 - (1 - t) ** 5
    elif easing == "quint_in_out":
        return 16 * t ** 5 if t < 0.5 else 1 - 16 * (1 - t) ** 5
    
    # Sine
    elif easing == "sine_in":
        return 1 - math.cos(t * math.pi / 2)
    elif easing == "sine_out":
        return math.sin(t * math.pi / 2)
    elif easing == "sine_in_out":
        return 0.5 * (1 - math.cos(t * math.pi))
    
    # Exponential
    elif easing == "expo_in":
        return 0 if t == 0 else 2 ** (10 * (t - 1))
    elif easing == "expo_out":
        return 1 if t == 1 else 1 - 2 ** (-10 * t)
    elif easing == "expo_in_out":
        if t == 0:
            return 0
        elif t == 1:
            return 1
        elif t < 0.5:
            return 0.5 * 2 ** (20 * t - 10)
        else:
            return 1 - 0.5 * 2 ** (-20 * t + 10)
    
    # Circular
    elif easing == "circ_in":
        return 1 - math.sqrt(1 - t * t)
    elif easing == "circ_out":
        return math.sqrt(1 - (t - 1) * (t - 1))
    elif easing == "circ_in_out":
        if t < 0.5:
            return 0.5 * (1 - math.sqrt(1 - 4 * t * t))
        else:
            return 0.5 * (math.sqrt(1 - 4 * (t - 1) * (t - 1)) + 1)
    
    # Back (overshoot)
    elif easing == "back_in":
        c1 = 1.70158
        c3 = c1 + 1
        return c3 * t * t * t - c1 * t * t
    elif easing == "back_out":
        c1 = 1.70158
        c3 = c1 + 1
        return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
    elif easing == "back_in_out":
        c1 = 1.70158
        c2 = c1 * 1.525
        if t < 0.5:
            return (2 * t) ** 2 * ((c2 + 1) * 2 * t - c2) / 2
        else:
            return ((2 * t - 2) ** 2 * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2
    
    # Elastic
    elif easing == "elastic_in":
        c4 = (2 * math.pi) / 3
        if t == 0:
            return 0
        elif t == 1:
            return 1
        else:
            return -(2 ** (10 * (t - 1))) * math.sin((t - 1.1) * c4)
    elif easing == "elastic_out":
        c4 = (2 * math.pi) / 3
        if t == 0:
            return 0
        elif t == 1:
            return 1
        else:
            return 2 ** (-10 * t) * math.sin((t - 0.1) * c4) + 1
    elif easing == "elastic_in_out":
        c5 = (2 * math.pi) / 4.5
        if t == 0:
            return 0
        elif t == 1:
            return 1
        elif t < 0.5:
            return -(2 ** (20 * t - 10) * math.sin((20 * t - 11.125) * c5)) / 2
        else:
            return (2 ** (-20 * t + 10) * math.sin((20 * t - 11.125) * c5)) / 2 + 1
    
    # Bounce
    elif easing == "bounce_in":
        return 1 - _bounce_out(1 - t)
    elif easing == "bounce_out":
        return _bounce_out(t)
    elif easing == "bounce_in_out":
        if t < 0.5:
            return (1 - _bounce_out(1 - 2 * t)) / 2
        else:
            return (1 + _bounce_out(2 * t - 1)) / 2
    
    else:
        # Fallback to linear with warning
        print(f"Warning: Unknown easing '{easing}', using linear")
        return t

def _bounce_out(t):
    """Helper function for bounce easing"""
    n1 = 7.5625
    d1 = 2.75
    
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375

# Convenience function to list all available easing types
def get_available_easings():
    """Return list of all available easing function names"""
    return [
        "linear",
        "ease_in", "ease_out", "ease_in_out",
        "quad_in", "quad_out", "quad_in_out",
        "cubic_in", "cubic_out", "cubic_in_out",
        "quart_in", "quart_out", "quart_in_out",
        "quint_in", "quint_out", "quint_in_out",
        "sine_in", "sine_out", "sine_in_out",
        "expo_in", "expo_out", "expo_in_out",
        "circ_in", "circ_out", "circ_in_out",
        "back_in", "back_out", "back_in_out",
        "elastic_in", "elastic_out", "elastic_in_out",
        "bounce_in", "bounce_out", "bounce_in_out"
    ]

#####################################################
# Send interpolated data to a registered event
#####################################################
import time

def send_event_data_interpolated(
    gamename="DEMO",
    eventname="EVENT",
    start_value=0,
    end_value=100,
    duration=5.0,
    interval=0.5,
    easing="linear",
    silent=False
):
    """
    Send interpolated event data to SteelSeries Engine with easing animation.
    
    Args:
        gamename (str): Name of the target game
        eventname (str): Name of the animation event
        start_value (float): Starting value for interpolation
        end_value (float): Ending value for interpolation
        duration (float): Total animation duration in seconds
        interval (float): Time between updates in seconds
        easing (str): Animation easing style
        silent (bool): Suppress console output messages
    
    Available Easing Styles:
        Basic: linear
        Quadratic: ease_in, ease_out, ease_in_out, quad_in, quad_out, quad_in_out
        Cubic: cubic_in, cubic_out, cubic_in_out
        Quartic: quart_in, quart_out, quart_in_out
        Quintic: quint_in, quint_out, quint_in_out
        Sine: sine_in, sine_out, sine_in_out
        Exponential: expo_in, expo_out, expo_in_out
        Circular: circ_in, circ_out, circ_in_out
        Special: back_in, back_out, back_in_out, elastic_in, elastic_out, 
                 elastic_in_out, bounce_in, bounce_out, bounce_in_out
    
    Returns:
        bool: True if animation completed successfully, False otherwise
    """
    # Validate SteelSeries Engine connection
    if not sse_address:
        if not silent:
            print("❌ SteelSeries Engine address not found.")
        return False
    
    # Validate and sanitize inputs
    try:
        gamename = sanitize_name(gamename, "gamename", silent=silent)
        eventname = sanitize_name(eventname, "eventname", silent=silent)
        
        # Validate numeric inputs
        if duration <= 0:
            if not silent:
                print("❌ Duration must be greater than 0")
            return False
            
        if interval <= 0:
            if not silent:
                print("❌ Interval must be greater than 0")
            return False
            
        if interval > duration:
            if not silent:
                print("⚠️  Interval is larger than duration, adjusting...")
            interval = duration / 2
            
    except Exception as e:
        if not silent:
            print(f"❌ Input validation error: {e}")
        return False
    
    # Calculate animation steps
    steps = max(int(duration / interval), 1)
    actual_duration = steps * interval
    
    # Show animation info
    if not silent:
        print(f"🎬 Starting animation: {gamename}.{eventname}")
        print(f"   Range: {start_value} → {end_value}")
        print(f"   Duration: {actual_duration:.2f}s ({steps + 1} steps)")
        print(f"   Easing: {easing}")
        print(f"   Interval: {interval:.3f}s")
    
    # Animation loop with error handling
    successful_sends = 0
    start_time = time.time()
    
    try:
        for i in range(steps + 1):
            # Calculate normalized time and apply easing
            t = i / steps if steps > 0 else 1.0
            eased_t = apply_easing(t, easing)
            
            # Interpolate value
            value = start_value + (end_value - start_value) * eased_t
            
            # Send data (handle both int and float values appropriately)
            if isinstance(start_value, int) and isinstance(end_value, int):
                final_value = int(round(value))
            else:
                final_value = round(value, 3)  # Keep some precision for floats
            
            # Send the event
            success = send_event_data(gamename, eventname, final_value, silent=True)
            if success:
                successful_sends += 1
            
            # Progress indicator (only show every 10% or if less than 10 steps)
            if not silent and (steps <= 10 or i % max(1, steps // 10) == 0 or i == steps):
                progress = (i / steps) * 100
                print(f"   {progress:3.0f}% | t={t:.2f} → {final_value}")
            
            # Sleep between updates (except for the last step)
            if i < steps:
                time.sleep(interval)
                
    except KeyboardInterrupt:
        if not silent:
            print(f"\n⏸️  Animation interrupted at step {i + 1}/{steps + 1}")
        return False
        
    except Exception as e:
        if not silent:
            print(f"❌ Animation error at step {i + 1}: {e}")
        return False
    
    # Final report
    elapsed_time = time.time() - start_time
    success_rate = (successful_sends / (steps + 1)) * 100
    
    if not silent:
        if successful_sends == steps + 1:
            print(f"✅ Animation completed successfully!")
        else:
            print(f"⚠️  Animation completed with {successful_sends}/{steps + 1} successful sends")
        
        print(f"   Actual duration: {elapsed_time:.2f}s")
        print(f"   Success rate: {success_rate:.1f}%")
        print(f"   Final value: {start_value + (end_value - start_value) * apply_easing(1.0, easing)}")
    
    return successful_sends == steps + 1



import threading
def send_event_data_async(*args, **kwargs):
    threading.Thread(target=send_event_data, args=args, kwargs=kwargs).start()

def send_event_data_interpolated_async(*args, **kwargs):
    threading.Thread(target=send_event_data_interpolated, args=args, kwargs=kwargs).start()

'''
def unregister_game(gamename="DEMO", silent=False):
    if not sse_address:
        if not silent:
            print("SteelSeries Engine address not found.")
        return

    gamename = sanitize_name(gamename, "gamename", silent=silent)

    try:
        response = requests.delete(
            f"http://{sse_address}/game_metadata",
            json={"game": gamename}
        )
        response.raise_for_status()
        if not silent:
            print(f"[OK] Game '{gamename}' unregistered.")
    except requests.exceptions.HTTPError as http_err:
        if not silent:
            print(f"[HTTP Error] {http_err.response.status_code}: {http_err.response.text}")
    except Exception as e:
        if not silent:
            print(f"[Error] Failed to unregister game: {e}")
'''




#####################################################
# Show help for available functions
#####################################################
def help(silent=False):
    if silent:
        return
    print("""
[SteelSeries Python API] Available Commands
-------------------------------------------

Help:
    help() or list_commands()
    list_icons()
    example()

Game/App:
    register_game(gamename, developer, displayname, iconcolorid)

Events:
    register_event(gamename, eventname)

Sending Data:
    send_event_data(...)                  # Send value 0–100
    send_event_data_async(...)            # Non-blocking background send
    send_event_data_interpolated(...)     # Smooth animation from a→b

Utility:
    sanitize_name(name)                   # Fix naming convention
    get_sse_address()                     # Get Steelseries Address
""")

# Alias
list_commands = help

# Icon list
icon_list = {
    0:  "Default (Blank display)",
    1:  "Health",              2:  "Armor",               3:  "Ammo",
    4:  "Money",               5:  "Flashbang / Explosion", 6:  "Kills",
    7:  "Headshot",            8:  "Helmet",              10: "Hunger",
    11: "Air / Breath",        12: "Compass",             13: "Tool / Pickaxe",
    14: "Mana / Potion",       15: "Clock",               16: "Lightning",
    17: "Item / Backpack",     18: "@ Symbol",            19: "Muted",
    20: "Talking",             21: "Connect",             22: "Disconnect",
    23: "Music",               24: "Play",                25: "Pause",
    27: "CPU",                 28: "GPU",                 29: "RAM",
    30: "Assists",             31: "Creep Score",         32: "Dead",
    33: "Dragon",              35: "Enemies",             36: "Game Start",
    37: "Gold",                38: "Health (2)",          39: "Kills (2)",
    40: "Mana (2)",            41: "Teammates",           42: "Timer",
    43: "Temperature"
}
 
def list_icons():
    print("[Available SteelSeries Icons]")
    for i in sorted(icon_list.keys()):
        print(f"{i:2}: {icon_list[i]}")

# Alias
icons_help = list_icons

# Full example
def example():
    print("""
[SteelSeries API Example Usage]
-------------------------------
# Register your game
register_game("MYGAME", "Neo", "Cool App", iconcolorid=1)

# Register event
register_event("MYGAME", "HEALTH")

# Send basic data
send_event_data("MYGAME", "HEALTH", 88)

# Send animated data
send_event_data_interpolated("MYGAME", "HEALTH", 0, 100, duration=3.0, interval=0.2, easing="ease-out")

# Use gradient color mapping (auto-registers with color range)
register_gradient_event("MYGAME", "MANA")
send_event_data("MYGAME", "MANA", 60)

# Flash color event
register_timed_event("MYGAME", "DAMAGE", duration_ms=600, red=255, green=64, blue=64)
send_event_data("MYGAME", "DAMAGE", 1)

# Clean up
unregister_game("MYGAME")
""")
