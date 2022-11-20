
from abc import ABC, abstractmethod


class BaseCalendarProvider(ABC):

    @abstractmethod
    def get_calendar_events(self):
        """
        Implement this method.
        Return a dictionary with calendar events, in this format:
        TBD
        """
        pass

