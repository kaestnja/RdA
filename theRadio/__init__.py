#!/usr/bin/python3
r"""
#sys.path.append(os.path.dirname(os.path.realpath(__file__)))

#print (sys.path);
todo http://mfcabrera.com/blog/using-mypy-for-improving-your-codebase.html #DevSkim: ignore DS137138 
import scripts.config_parser as config_parser
from . import config_parser  # explicit relative import

PACKAGE_PARENT = '..'
SCRIPT_DIR1 = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
SCRIPT_DIR3 = os.path.realpath(os.path.dirname(__file__))

sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR1, PACKAGE_PARENT)))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR3, PACKAGE_PARENT)))

https://www.programcreek.com/python/example/431/yaml.load
https://pypi.org/project/deepmerge/
"""
import os, sys, yaml
import pathlib
from deepmerge import always_merger

#os.path.append(os.path.join((os.path.dirname(os.path.realpath(__file__)),'..','scripts')))
#sys.path.insert(0, '../scripts')

PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)))
SAMPLESPATH = os.path.join(os.path.join(os.path.join(os.path.join(os.path.dirname(PATH)),".."),"development"),"samples")
BATCHPATH = os.path.dirname(PATH)
#print (SAMPLESPATH)
if not os.path.isdir(SAMPLESPATH):
    SAMPLESPATH = PATH
if not pathlib.Path(SAMPLESPATH).exists:
    SAMPLESPATH = PATH
if not pathlib.Path(SAMPLESPATH).is_dir:
    SAMPLESPATH = PATH

#os.path.join(SAMPLESPATH,"results.yml"

CONFIGFILE = os.path.join(os.path.join(PATH, ".."),"config.yml")
_CONFIG = dict (
    database = dict(
        host = "127.0.0.1",
        port = 27017,
        username = "Administrator",
        password = "P@ssw0rd",
        auth = False
        ),
    app = dict(
        name = "Comparateur D Avant-Garde (CdA)",
        version = "0.9.6"
        ),
    paths = dict(
        defaultResults = SAMPLESPATH,
        lastusedResult = os.path.join(SAMPLESPATH,"results_small")
        )
    )

def read_config(file):
    try:
        with open(file, 'r') as config_file:
            try:
                #return (yaml.load(config_file))
                return (yaml.load(config_file, Loader=yaml.FullLoader)) #https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
            except yaml.YAMLError as exc:
                print("[EE] Error while reading the config file :", str(exc))
            except Exception as exc:
                print("[EE] Error while reading the config file :", str(exc))
        print("[II] Running with following config:", yaml.dump(_CONFIG))
    except FileExistsError as e:
        print("[WW] Warning while reading the config file :", str(e))
    except Exception as e:
        print("[EE] Error while reading the config file :", str(e))
    #return (yaml.dump(emergency_config, encoding=('utf-8'), default_flow_style=False, allow_unicode=True))
    return (_CONFIG)

def complete_config(content,completingcontent):
    try:
        if not ("host" in content): content["database"]["host"] = completingcontent["database"]["host"]
        if not ("port" in content): content["database"]["port"] = completingcontent["database"]["port"]
        if not ("username" in content): content["database"]["username"] = completingcontent["database"]["username"]
        if not ("password" in content): content["database"]["password"] = completingcontent["database"]["password"]
        if not ("name" in content): content["app"]["name"] = completingcontent["app"]["name"]
        if not ("version" in content): content["app"]["version"] = completingcontent["app"]["version"]
        if not ("defaultResults" in content): content["paths"]["defaultResults"] = completingcontent["paths"]["defaultResults"]
        if not ("lastusedResult" in content): content["paths"]["lastusedResult"] = completingcontent["paths"]["lastusedResult"]
        print("[II] Completed with following content:", yaml.dump(content))
        return (content)
    except yaml.YAMLError as exc:
        print("[EE] Error while completing the content :", str(exc))
    except Exception as e:
        print("[EE] Error while completing the content :", str(e))
    return (_CONFIG)

def write_config(file, content):
    try:
        with open(file, 'wb') as yaml_file:
            try:
                yaml_file.write(yaml.dump(content, encoding=('utf-8'), default_flow_style=False, allow_unicode=True))
            except yaml.YAMLError as exc:
                print("[EE] Error while writing the config file :", str(exc))
            except Exception as exc:
                print("[EE] Error while writing the config file :", str(exc))
    except FileExistsError as e:
        print("[WW] Warning while writing the config file :", str(e))
    except Exception as e:
        print("[EE] Error while writing the config file :", str(e))


CONFIG = read_config(CONFIGFILE)
#CONFIG = complete_config(CONFIG,_CONFIG)
CONFIG = always_merger.merge(_CONFIG, CONFIG)
CONFIG = always_merger.merge(CONFIG, _CONFIG)
write_config(CONFIGFILE,CONFIG)

#host = CONFIG["database"]["host"]
#CONFIG["database"]["host"] = "128.0.0.1"
#print("[i] host: {0}.".format(str(CONFIG["database"]["host"])))
#print (yaml.dump(CONFIG, encoding=('utf-8'), default_flow_style=False, allow_unicode=True))