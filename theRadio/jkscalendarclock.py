#!/usr/bin/python3
""" 
Modul, das die Klasse CalendarClock implementiert.
"""

from jksclock import Clock
from jkscalendar import Calendar


class CalendarClock(Clock, Calendar):
    """ 
        Die Klasse CalendarClock implementiert eine Uhr mit integrierter
        Kalenderfunktion.  Die Klasse erbt sowohl von der Klasse Clock 
        als auch von der Klasse Calendar.
    """

    def __init__(self,day, month, year, hour, minute, second):
        """
        Zur Initialisierung der Uhrzeit wird der Konstruktor der Clock-Klasse
        aufgerufen. Zur Initialisierung des Kalenders wird der Konstruktor der 
        Calendar-Klasse aufgerufen.

        CalendarClock enthält dann die vereinigten Attribute der Clock- und 
        Calendar-Klasse:
        self.day, self.month, self.year, self.hour, self.minute, self.second
        """

        Clock.__init__(self,hour, minute, second)
        Calendar.__init__(self,day, month, year)


    def tick(self):
        """
        Die Position der Uhr wird um eine Sekunde weiterbewegt,
        der Kalender wird, falls Mitternacht überschritten wird, 
        um einen Tag weiterbewegt.
        """

        previous_hour = self._hours
        Clock.tick(self)
        if (self._hours < previous_hour): 
            self.advance()

    def __str__(self):
        """
        Erzeugt die Stringdarstellung eines CalendarClock-Objekts
        """
        return Calendar.__str__(self) + ", " + Clock.__str__(self)


if __name__ == "__main__":
    x = CalendarClock(31,12,2013,23,59,59)
    #print("One tick from ",x, end=" ")
    x.tick()
    print("to ", x)

    x = CalendarClock(28,2,1900,23,59,59)
    #print("One tick from ",x, end=" ")
    x.tick()
    print("to ", x)

    x = CalendarClock(28,2,2000,23,59,59)
    #print("One tick from ",x, end=" ")
    x.tick()
    print("to ", x)

    x = CalendarClock(7,2,2013,13,55,40)
    #print("One tick from ",x, end=" ")
    x.tick()
    print("to ", x)
