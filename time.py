# Time Entities for Hourly Setpoints

class HourlySetpoints:
    """
    A class to represent hourly setpoints.
    """

    def __init__(self):
        self.setpoints = {}

    def set_hourly_setpoint(self, hour, value):
        if 0 <= hour < 24:
            self.setpoints[hour] = value
        else:
            raise ValueError("Hour must be between 0 and 23")

    def get_hourly_setpoint(self, hour):
        if 0 <= hour < 24:
            return self.setpoints.get(hour, None)
        else:
            raise ValueError("Hour must be between 0 and 23")

    def __repr__(self):
        return repr(self.setpoints)
