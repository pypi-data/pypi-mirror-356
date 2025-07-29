from enum import StrEnum, auto


class AWSRegion(StrEnum):
    @staticmethod
    def _generate_next_value_(
            name: str, start: int, count: int, last_values: list[str]
    ):
        """
        Return the lower-cased region name.
        """
        return name.replace("_", "-").lower()

    US_EAST_1 = auto()
    US_EAST_2 = auto()
    US_WEST_1 = auto()
    US_WEST_2 = auto()
