#!/usr/bin/python3
r"""
rem to apply dark theme to QT Creator you need go to "Tools" -> "Options" -> "Environment" -> "Interface" tab,
and there you need to change "Theme" to dark...

python3 -i package/standalone.py
python3 -m mypackage.myothermodule

in case:
sys.path.append('../../')
sys.path.append('../')
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))

"""
import sys
#sys.path.insert(0, './scripts')
#import scripts
from theRadio import main_qt #as main_qt
#import scripts.main_qt #as main_qt

if __name__ == "__main__":
    if __debug__:
        print ('Debug ON')
    else:
        print ('Debug OFF')
    #scripts.main_qt.run()
    main_qt.run()
