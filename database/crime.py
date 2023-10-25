from datetime import datetime

class Crime:
    def __init__(self):
        self.arrest=False
        self.domestic=False
        self.date = datetime.now
        self.primary_type = ''
        self.description=''
        self.location_description=''
        self.year=2023
        self.latitude=0.0
        self.longitude=0.0