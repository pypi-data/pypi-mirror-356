import steelseries as ss

ss.register_game("TESTING", "NEO", "TESTING DEMO", 1)
ss.register_event("TESTING", "HEALTH")
ss.send_event_data_interpolated("TESTING", "HEALTH", 0, 100, 2, 0.1, "linear", True) # 0 --> 100 and wait until done
ss.send_event_data_interpolated("TESTING", "HEALTH", 100, 0, 2, 0.1, "ease-in", True) # Bounce back  100 --> 0 
ss.send_event_data("TESTING", "HEALTH", 50, True) # wait until done to put 50%