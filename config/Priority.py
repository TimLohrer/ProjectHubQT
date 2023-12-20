class Priority():
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"

    VERY_LOW_STRING = "Very Low"
    LOW_STRING = "Low"
    MEDIUM_STRING = "Medium"
    HIGH_STRING = "High"
    VERY_HIGH_STRING = "Very High"

    def parse(self, status):
        match status:
            case self.VERY_LOW_STRING:
                return self.VERY_LOW
            case self.LOW_STRING:
                return self.LOW
            case self.MEDIUM_STRING:
                return self.MEDIUM
            case self.HIGH_STRING:
                return self.HIGH
            case self.VERY_HIGH_STRING:
                return self.VERY_HIGH
            case _:
                return "UNKNOWN"

    def stringify(self, status):
        match status:
            case self.VERY_LOW:
                return self.VERY_LOW_STRING
            case self.LOW:
                return self.LOW_STRING
            case self.MEDIUM:
                return self.MEDIUM_STRING
            case self.HIGH:
                return self.HIGH_STRING
            case self.VERY_HIGH:
                return self.VERY_HIGH_STRING
            case _:
                return "UNKNOWN"