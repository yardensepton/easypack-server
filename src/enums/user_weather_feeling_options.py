from enum import Enum


class UserWeatherFeelingOptions(str, Enum):
    NORMAL = "Expect to feel pretty much the same as you're used to."
    COLD = "Expect to feel chillier than you're used to."
    HOT = "Expect to feel hotter than you're used to."
