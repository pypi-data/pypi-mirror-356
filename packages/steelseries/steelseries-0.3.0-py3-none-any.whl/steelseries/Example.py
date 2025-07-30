import __init__ as ss
import time
# register game and events
ss.register_game("TESTING", "NEO", "TESTING DEMO", 1)
ss.register_event("TESTING", "HEALTH")
ss.register_event("TESTING", "ICON", iconcolorid=10)

# animate the lighting - make sure to have the lighting setup in the engine!!!
ss.send_event_data_interpolated("TESTING", "HEALTH", 0, 100, 0.5, 0.01, "quad_out", True) # 0 --> 100 and wait until done
ss.send_event_data_async("TESTING", "HEALTH", 12) # send in background to not halt app
time.sleep(1) # wait one second

# send in background to not halt app - will flicker because of below command
ss.send_event_data_interpolated_async("TESTING", "HEALTH", 100, 50, 0.5, 0.01, "ease-in", True) 
ss.send_event_data_interpolated("TESTING", "HEALTH", 100, 0, 0.5, 0.01, "ease-in", True) # Bounce back  100 --> 0 
ss.send_event_data("TESTING", "HEALTH", 50, True) # wait until done to put 50%
time.sleep(1)
#bouncing
ss.send_event_data_interpolated("TESTING", "HEALTH", 50, 0, 1, 0.01, "bounce_out", True)
ss.send_event_data_interpolated("TESTING", "HEALTH", 0, 100, 1, 0.01, "bounce_in", True) # 0 --> 100 and wait until done