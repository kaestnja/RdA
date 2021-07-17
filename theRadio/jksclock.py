#!/usr/bin/python3
""" 
Die Klasse Clock dient der logischen Simulation einer Uhr. 
Die Uhrzeit kann mit einer Methode sekundenweise weiterbewegt 
werden. 
"""

class Clock(object):

    def __init__(self, hours, minutes, seconds):
        """
        Die Parameter hours, minutes, seconds müssen Ganzzahlen 
        sein, und es muss gelten:
        0 <= h < 24
        0 <= m < 60
        0 <= s < 60
        """

        self.set_Clock(hours, minutes, seconds)

    def set_Clock(self, hours, minutes, seconds):
        """
        Die Parameter hours, minutes, seconds müssen Ganzzahlen 
        sein, und es muss gelten:
        0 <= h < 24
        0 <= min < 60
        0 <= sec < 60
        """

        if type(hours) == int and 0 <= hours and hours < 24:
            self._hours = hours
        else:
            raise TypeError("Stunden müssen Ganzzahlen zwischen 0 und 23 sein!")
        if type(minutes) == int and 0 <= minutes and minutes < 60:
            self.__minutes = minutes 
        else:
            raise TypeError("Minuten müssen Ganzzahlen zwischen 0 und 59 sein!")
        if type(seconds) == int and 0 <= seconds and seconds < 60:
            self.__seconds = seconds
        else:
            raise TypeError("Sekunden müssen Ganzzahlen zwischen 0 und 59 sein!")

    def __str__(self):
        """ 
        Diese Methode überlädt die eingebaute Funktion str(),
        d.h. es wird eine Methode zur Verfügung gestellt, 
        um ein Objekt der Klasse Clock in einen String zu wandeln.
        Die Methode __str__ wird auch von der Print-Funktion
        genutzt, um ein Objekt der Klasse Clock auszugeben.
        """

        return "{0:02d}:{1:02d}:{2:02d}".format(self._hours,
                                                self.__minutes,
                                                self.__seconds)

    def tick(self):
        """
        Diese Methode lässt die Uhr 'ticken', d.h. die interne 
        Uhrzeit eines Objektes, d.h. die Stunden-, 
        Minuten- und Sekunden-Attribute werden um eine Sekunde
        weitergerechnet.

        Beispiele:
        >>> x = Clock(12,59,59)
        >>> print(x)
        12:59:59
        >>> x.tick()
        >>> print(x)
        13:00:00
        >>> x.tick()
        >>> print(x)
        13:00:01
        """

        if self.__seconds == 59:
            self.__seconds = 0
            if self.__minutes == 59:
                self.__minutes = 0
                if self._hours == 23:
                    self._hours = 0
                else:
                    self._hours += 1
            else:
                self.__minutes += 1
        else:
            self.__seconds += 1


if __name__ == "__main__":
    x = Clock(23,59,59)
    print(x)
    x.tick()
    print(x)
    y = str(x)
    print(type(y))
