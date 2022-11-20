
from abc import ABC, abstractmethod
import typing
from typing import NamedTuple

class CalendarEvent(NamedTuple):
    summary: str
    start: any
    end: any
    all_day_event: bool


class BaseCalendarProvider(ABC):

    @abstractmethod
    def get_calendar_events(self) -> typing.List[CalendarEvent]:
        """
        Implement this method.
        Return a list of `CalendarEvent` which contains summary, start date, end date, and all day event
        """
        pass


    