def scheduling(time, location, length, mandatory):
    if time:                                 # Business hours
        return (location and mandatory)      # In office and mandatory participation
    else:                                    # Outside business hours
        return ((not location) and length)   # Teleconference for a short duration
