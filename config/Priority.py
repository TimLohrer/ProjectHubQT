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

    @staticmethod
    def parse(status):
        match status:
            case Priority.VERY_LOW_STRING:
                return Priority.VERY_LOW
            case Priority.LOW_STRING:
                return Priority.LOW
            case Priority.MEDIUM_STRING:
                return Priority.MEDIUM
            case Priority.HIGH_STRING:
                return Priority.HIGH
            case Priority.VERY_HIGH_STRING:
                return Priority.VERY_HIGH
            case _:
                return "UNKNOWN"

    @staticmethod
    def stringify(status):
        match status:
            case Priority.VERY_LOW:
                return Priority.VERY_LOW_STRING
            case Priority.LOW:
                return Priority.LOW_STRING
            case Priority.MEDIUM:
                return Priority.MEDIUM_STRING
            case Priority.HIGH:
                return Priority.HIGH_STRING
            case Priority.VERY_HIGH:
                return Priority.VERY_HIGH_STRING
            case _:
                return "UNKNOWN"

    @staticmethod
    def emojify(status):
        match status:
            case Priority.VERY_LOW:
                return "🔵"
            case Priority.LOW:
                return "🟣"
            case Priority.MEDIUM:
                return "🟡"
            case Priority.HIGH:
                return "🟠"
            case Priority.VERY_HIGH:
                return "🔴"
            case _:
                return "❓"
