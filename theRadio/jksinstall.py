#!/usr/bin/python3
#cd C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64
#cd C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_86
#python -c "import sys; print('\n'.join(sys.path))"
#in Powershell:  pip freeze | %{$_.split('==')[0]} | %{echo "pip install --upgrade $_"}
#in Powershell:  pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}

#https://www.digitalocean.com/community/tutorials/how-to-use-logging-in-python-3
#https://docs.python.org/3/howto/logging-cookbook.html
#https://docs.python.org/3/howto/logging.html

import pip
import pkg_resources
import subprocess
import sys
import os
import pprint
#from pprint import pprint
#from subprocess import call

class Install(object):
    """description of class"""
    local_pythonpaths = []

    def __init__(self, command):
        self.pip_version = tuple([int(x) for x in pip.__version__.split('.')[:3]])
        print("init class")
        if sys.platform == "win32":
            import ntpath
            self.pathmodule = ntpath
        else:
            import posixpath
            self.pathmodule = posixpath
        print ('jk-pathmodule: %s' % str(self.pathmodule))
        self.find_local_pythonpaths(self)
        #self.getsitepackages(self)
        #if sys.platform == "win32":
        #if 'all' in command:
        #    self.update_all()
        #else:
        #    self.install(command)

    def find_local_pythonpaths(self, placeholder):
        #https://leemendelowitz.github.io/blog/how-does-python-find-packages.html
        self.pypath1 = self.pathmodule.normpath("C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python36_64/python.exe")
        self.pypath1w = self.pathmodule.normpath("C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python36_64/pythonw.exe")
        self.pypath2 = self.pathmodule.normpath("C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python36_86/python.exe")
        self.pypath2w = self.pathmodule.normpath("C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python36_86/pythonw.exe")
        print(sys.path)
        #pprint(sys.path)
        print(sys.executable)
        print(sys.exec_prefix)
        try:
            user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
            print(user_paths)
        except KeyError:
            user_paths = []

    def getsitepackages(self, placeholder):
        """Returns a list containing all global site-packages directories (and possibly site-python).
        For each directory present in the global ``PREFIXES``, this function will find its `site-packages` subdirectory depending on the system environment, and will return a list of full paths.
        """
        sitepackages = []
        seen = set()

        for prefix in PREFIXES:
            if not prefix or prefix in seen:
                continue
            seen.add(prefix)

            if sys.platform in ('os2emx', 'riscos'):
                sitepackages.append(os.path.join(prefix, "Lib", "site-packages"))
            elif os.sep == '/':
                sitepackages.append(os.path.join(prefix, "local/lib", "python" + sys.version[:3], "dist-packages"))
                sitepackages.append(os.path.join(prefix, "lib", "python" + sys.version[:3], "dist-packages"))
            else:
                sitepackages.append(prefix)
                sitepackages.append(os.path.join(prefix, "lib", "site-packages"))
            if sys.platform == "darwin":
                # for framework builds *only* we add the standard Apple
                # locations.
                from sysconfig import get_config_var
                framework = get_config_var("PYTHONFRAMEWORK")
                if framework:
                    sitepackages.append(
                            os.path.join("/Library", framework,
                                sys.version[:3], "site-packages"))
        return sitepackages
    
    def install(self, package):
        #pip_version = tuple([int(x) for x in pip.__version__.split('.')[:3]])
        print("install pip version: %s" % str(self.pip_version))
        import imp
        imp.find_module(package)

        if self.pip_version < (10, 0, 0):
            pip.main(['install', package])
            #packages = [dist.project_name for dist in pip.get_installed_distributions()]
            #subprocess.check_call("pip install --upgrade " + ' '.join(packages), shell=True)
        else:
            subprocess.check_call(["python", '-m', 'pip', 'install', package]) # install pkg
            subprocess.check_call(["python", '-m', 'pip', 'install',"--upgrade", package]) # upgrade pkg
        

    def update_all(self, command):#
        print("update pip version: %s" % str(self.pip_version))
        if 'all' in command:
            dists = [d for d in pkg_resources.working_set]
            #subprocess.call("sudo pip install --upgrade " + ' '.join(dists), shell=True)
            for dist in dists:
                if not sys.platform == "win32":
                    print ("sudo pip install --upgrade " + dist.project_name)
                    subprocess.call("sudo pip install --upgrade " + dist.project_name, shell=True)
                else:
                    #subprocess.call('dir', shell=True)
                    #os.path.join(sys.path[0],'bImages')
                    #os.path.join(sys.path[0],'bImages')
                    print (sys.executable + " -m pip install --upgrade " + dist.project_name)
                    subprocess.call(sys.executable + " -m pip install --upgrade " + dist.project_name, shell=True)

    #subprocess.check_call(["python", '-m', 'pip', 'install', "-U"]) # update all pkg
    #packages = [dist.project_name for dist in pip.get_installed_distributions()]
    #call("pip install --upgrade " + ' '.join(packages), shell=True)
    # Filter out distributions you don't care about and use.
    #pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
    #sudo python -m pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 sudo python -m pip install -U > ~/pip.log
    #sudo python3 -m pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 sudo python3 -m pip install -U > ~/pip3.log
    #pip list --outdated --format=freeze
    #pip install -U
    #sudo python -m pip list --outdated --format=freeze
    #sudo python3 -m pip list --outdated --format=freeze

    #python 2.x: sudo python -m pip install [package]
    #python 3.x: sudo python3 -m pip install [package]
    #https://pypi.org/search/?q=rpi&o=-created
    #https://www.raspberrypi.org/search/


if __name__ == "__main__":
    #x = Install('all')
    #print("x pip version: %s" % str(x.pip_version))
    #x.update_all ('all')
    #x.update_all ('psutil')
    y = Install('all')
    y.install('resource')

#1
#cd  ~/aRadio/
#git clone https://github.com/thilaire/rpi-TM1638.git
#sudo chmod -R 6777 ~/aRadio/rpi-TM1638/
##chown -R root:root /root && sudo chmod -R 6777 /root
##sed -i -e 's/raw_input/input/g' /root/katoolin/katoolin.py
##cd katoolin
#cd ~/aRadio/rpi-TM1638/
#sudo python3 ./setup.py

##2a1
#cd ~/aRadio/
#wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.55.tar.gz;
#tar xvfz bcm2835-1.55.tar.gz;
#cd bcm2835-1.55;
#./configure;
#make;
#sudo make install
##2a2
##cd ~/aRadio/
##sudo apt-get install html-xml-utils
##mkdir -p bcm2835 && (wget -qO - `curl -sL http://www.airspayce.com/mikem/bcm2835 | hxnormalize -x -e | hxselect -s '\n' -c "div.textblock>p:nth-child(4)>a:nth-child(1)"` | tar xz --strip-components=1 -C bcm2835 )
##cd bcm2835
##./configure
##make
##sudo make install
##2b1
#cd ~/aRadio/
#wget https://github.com/downloads/mjoldfield/pi-tm1638/pi-tm1638-1.0.tar.gz
#tar xzvf pi-tm1638-1.0.tar.gz
#cd ~/aRadio/
#cd pi-tm1638-1.0
#./configure
#make
#sudo make install
##2b2
##cd ~/aRadio/
##git clone https://github.com/mjoldfield/pi-tm1638.git
##autoreconf -vfi
##./configure
##make
##sudo make install
