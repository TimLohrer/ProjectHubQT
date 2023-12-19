class Priority():
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"

    def beautify(self, priority):
        if priority == self.VERY_HIGH:
            return "Very High"
        elif priority == self.HIGH:
            return "High"
        elif priority == self.MEDIUM:
            return "Medium"
        elif priority == self.LOW:
            return "Low"
        elif priority == self.VERY_LOW:
            return "Very Low"
        else:
            return "UNKNOWN"