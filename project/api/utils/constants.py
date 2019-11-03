from enum import Enum

DaysForHarvestNotificationThreshold = 3

class IrrigationModes(Enum):
    ManualIrrigation = 1
    ScheduledIrrigation = 2
    SmartIrrigation = 3
