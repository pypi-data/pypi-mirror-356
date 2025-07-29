import os
import subprocess
import time
import importlib.metadata
import Oasys.gRPC


_connection = None
_debug      = False


def start(abspath, args=None, port=50053, memory=25, license=None, debug=False, wait=5):
    if debug:
        print("Starting {}, listening on port {}".format(abspath, port))

    environ = os.environ.copy()
    if license:
        environ[ARUP_LICENSE_PATH] = license

    try:
        portnum = int(port)
        if portnum < 1:
            raise ValueError("Negative port number {} for REPORTER. Cannot continue".format(portnum))
    except:
        raise ValueError("Invalid port number {} for REPORTER. Cannot continue".format(port))

    # args must be a list of strings, not a string
    pargs = [abspath, "-grpc=-{}".format(portnum)]
    if args:
        pargs.extend(args)

    proc = subprocess.Popen(pargs, env=environ)

    proc.poll()
    if proc.returncode == 99:
        raise ValueError("Failed to start REPORTER. Port {} already in use. Cannot continue".format(portnum))
    elif proc.returncode == 98:
        raise ValueError("Failed to start gRPC server in REPORTER. Cannot continue")
    elif proc.returncode:
        raise ValueError("Failed to start REPORTER. Cannot continue")

# Sleep to give time for REPORTER to start
    time.sleep(wait)

    return connect(portnum, memory, 'localhost', debug)


def connect(port=50053, memory=25, hostname='localhost', debug=False):
    if debug:
        print("Called connect with port {} and memory {}".format(port, memory))

    Oasys.REPORTER._debug      = debug
    Oasys.REPORTER._connection = Oasys.gRPC.Connection("REPORTER", port, memory, hostname, debug)

# Check version
    version  = importlib.metadata.version('Oasys.REPORTER')
    modMajor = int(version.split('.')[0]);
    exeMajor = int(Oasys.REPORTER._connection.version);

    if debug:
        print("Oasys.REPORTER module version {} ({})".format(modMajor, version))
        print("REPORTER executable version {} ({})".format(exeMajor, Oasys.REPORTER._connection.version))

    if exeMajor != modMajor:
        raise ValueError("Major version ({}) of REPORTER executable {} != major version ({}) of Oasys.REPORTER module {}. Cannot continue".format(exeMajor, Oasys.REPORTER._connection.version, modMajor, version))

    return Oasys.REPORTER._connection


def disconnect(connection):
    if Oasys.REPORTER._debug:
        print("Called disconnect")

    connection.finalise()
    Oasys.REPORTER._connection = None


def terminate(connection):
    if Oasys.REPORTER._debug:
        print("Called terminate")

    connection.terminate()
    Oasys.REPORTER._connection = None


def createInstance(t, h):
# Classes in REPORTER
    if t == "Colour":
        instance = object.__new__(Oasys.REPORTER.Colour)
    elif t == "Image":
        instance = object.__new__(Oasys.REPORTER.Image)
    elif t == "Item":
        instance = object.__new__(Oasys.REPORTER.Item)
    elif t == "Options":
        instance = object.__new__(Oasys.REPORTER.Options)
    elif t == "Page":
        instance = object.__new__(Oasys.REPORTER.Page)
    elif t == "Reporter":
        instance = object.__new__(Oasys.REPORTER.Reporter)
    elif t == "Template":
        instance = object.__new__(Oasys.REPORTER.Template)
    elif t == "Utils":
        instance = object.__new__(Oasys.REPORTER.Utils)
    elif t == "Variable":
        instance = object.__new__(Oasys.REPORTER.Variable)
    elif t == "Window":
        instance = object.__new__(Oasys.REPORTER.Window)

# Generic object
    elif t == "ItemObject":
        instance = object.__new__(Oasys.REPORTER.ItemObject)

# Unsupported
    else:
        raise NotImplementedError("Instance type '{}' not implemented".format(t))

    instance.__dict__['_handle']  = h;
    instance.__dict__['_objtype'] = t;

    return instance

