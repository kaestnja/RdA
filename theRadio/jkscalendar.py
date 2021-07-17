#!/usr/bin/python3
""" 
Die Klasse Calendar implementiert einen Kalender. 
Ein Kalenderdatum kann auf ein bestimmtes Datum gesetzt werden
oder kann um einen Tag weitergeschaltet werden.  
"""

class Calendar(object):

    months = (31,28,31,30,31,30,31,31,30,31,30,31)

    @staticmethod
    def leapyear(jahr):
        """ 
        Die Methode leapyear liefert True zurück, wenn jahr
        ein Schaltjahr ist, und False, wenn nicht.
        """

        if jahr % 4 == 0:
            if jahr % 100 == 0:
                if jahr % 400 == 0:
                    schaltjahr = True
                else:
                    schaltjahr = False
            else:
                schaltjahr = True
        else:
            schaltjahr = False

        return schaltjahr


    def __init__(self, d, m, y):
        """
        d, m, y müssen ganze Integer-Werte sein und y muss ein vierstelliger Wert sein
        """

        self.set_Calendar(d,m,y)


    def set_Calendar(self, d, m, y):
        """
        d, m, y müssen ganze Integer-Werte sein und y muss ein vierstelliger Wert sein
        """

        if type(d) == int and type(m) == int and type(y) == int:
            self.__days = d
            self.__months = m
            self.__years = y
        else:
            raise TypeError("d, m, y müssen ganze Zahlen sein!")


    def __str__(self):

        """ 
        Diese Methode überlädt die eingebaute Funktion str(),
        d.h. es wird eine Methode zur Verfügung gestellt, 
        um ein Objekt der Klasse Calendar in einen String zu 
        wandeln.
        Die Methode __str__ wird auch von der Print-Funktion
        genutzt, um ein Objekt der Klasse Calendar auszugeben.

        """

        return "{0:02d}.{1:02d}.{2:4d}".format(self.__days,
                                               self.__months,
                                               self.__years)


    def advance(self):
        """
        setzt den Kalender auf den nächsten Tag
        unter Berücksichtigung von Schaltjahren
        """

        max_days = Calendar.months[self.__months-1]
        if self.__months == 2 and Calendar.leapyear(self.__years):
            max_days += 1
        if self.__days == max_days:
            self.__days= 1
            if self.__months == 12:
                self.__months = 1
                self.__years += 1
            else:
                self.__months += 1
        else:
            self.__days += 1


if __name__ == "__main__":
    x = Calendar(31,12,2012)
    #print(x, end=" ")
    x.advance()
    print("nach advance: ", x)
    print("2012 war ein Schaltjahr:")
    x = Calendar(28,2,2012)
    #print(x, end=" ")
    x.advance()
    print("nach advance: ", x)
    x = Calendar(28,2,2013)
    #print(x, end=" ")
    x.advance()
    print("nach advance: ", x)
    print("1900 war kein Schaltjahr: Zahl durch 100, aber nicht durch 400 teilbar:")
    x = Calendar(28,2,1900)
    #print(x, end=" ")
    x.advance()
    print("nach advance: ", x)
    print("2000 war ein Schaltjahr, weil die Zahl durch 400 teilbar ist:")
    x = Calendar(28,2,2000)
    #print(x, end=" ")
    x.advance()
    print("nach advance: ", x)
