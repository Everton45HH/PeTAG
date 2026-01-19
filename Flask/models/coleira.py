class Device:
    def __init__(self, id,userId, deviceName, latitude, longitude):
        self.id = id
        self.userId = userId
        self.deviceName = deviceName
        self.latitude = latitude
        self.longitude = longitude
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'deviceName': self.deviceName,
            'latitude': self.latitude,
            'longitude': self.longitude
        }