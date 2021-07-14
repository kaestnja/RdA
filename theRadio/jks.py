#!/usr/local/bin/python
r"""
Sample Classes

Holds the Sample Classes (base and inherited).

Some Informative Notes Goes Here ...
Revision: 1.0 $Date: 24/07/2007 21:00$

History
-------
v. 1.0 - Initial Class Creation
v. 1.1 - ...
"""

__version__ = '$Revision: $'

# Standard Python modules
import os, sys, math, string
# External Python modules
import numpy
# Extension modules
import extension
# Misc Definitions

# First Class
class Sample_Class(object):


    """
    Sample Class
    """

    def __init__(self, assign_input={}, *optional_value_input, **optional_dict_input):

        """
        Sample Class Initialization

        Keyword Arguments:
        ------------------
        self. -> STRING: Description. Default =
        self. -> OBJECT: Description. Default = 

        Input Attributes:
        -----------------
        self. -> SCALAR: Description. Default = 

        Additional Attributes:
        ----------------------
        self. -> BOOLEAN: Description. Default = 

        Documentation last updated: Month. Day, Year - Author
        """

        # Default Values

        # Input Checks

        # init ...
        self.attribute = assign_input

    def __Private_Method(self):

        """
        Private Module
        """

        # Inputs

        # Module Code

        # Output

    def Public_Method(self):

        """
        Private Module
        """

        # Inputs

        # Module Code

        # Output

# =============================================================================
# Second Class
# =============================================================================
class Inherited_Class(Sample_Class):

    """
    Sample Class
    """

    def __init__(self, assign_input={}, *optional_value_input, **optional_dict_input):

        """
        Sample Class Initialization

        Keyword Arguments:
        ------------------
        self. -> STRING: Description. Default = 

        Input Attributes:
        -----------------
        self. -> SCALAR: Description. Default = 

        Additional Attributes:
        ----------------------
        self. -> SCALAR: Description. Default = 

        Documentation last updated: Month. Day, Year - Author
        """

        # Default Values

        # Input Checks

        # init ...
        self = Sample_Class(assign_input={}, *optional_value_input, **optional_dict_input)
        self.inherited_exclusive_attribute = "from some input ..."

    def __Private_Method(self):

        """
        Private Module
        """

        # Inputs

        # Module Code

        # Output

    def Public_Method(self):

        """
        Private Module
        """

        # Inputs

        # Module Code

        # Output

    # =============================================================================
    # Private Functions
    # =============================================================================
    def __Private_Function(inputs):

        """
        Private Function
        """

        # Inputs

        # Function code ...

    # =============================================================================
    # Public Function
    # =============================================================================
    def Public_Function(inputs):

        """
        Public Function
        """

        # Inputs

        # Function code ...

# =============================================================================
# Private Functions
# =============================================================================
def __Private_Function(self):

    """
    Function
    """

    # Function code ...

    return outputs

# =============================================================================
# Public Functions
# =============================================================================
def Public_Function(self):

    """
    Function
    """

    # Function code ...

    return outputs

#==============================================================================
# Class Test
#==============================================================================
if __name__ == '__main__':

    # Test Parent
    parent = Sample_Class()
    parent.Public_Method()

    # Test Child
    child = Inherited_Class()
    child.Public_Method()