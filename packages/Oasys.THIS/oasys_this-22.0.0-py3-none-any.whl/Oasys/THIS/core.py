import os
import subprocess
import time
import importlib.metadata
import Oasys.gRPC


_connection = None
_debug      = False


def start(abspath, args=None, port=50052, memory=25, license=None, debug=False, batch=False, wait=5):
    if debug:
        print("Starting {}, listening on port {}".format(abspath, port))

    environ = os.environ.copy()
    if license:
        environ[ARUP_LICENSE_PATH] = license

    try:
        portnum = int(port)
        if portnum < 1:
            raise ValueError("Negative port number {} for T/HIS. Cannot continue".format(portnum))
    except:
        raise ValueError("Invalid port number {} for T/HIS. Cannot continue".format(port))

    pargs = [abspath, "-grpc=-{}".format(portnum)]
    if args:
        pargs.extend(args)
    if batch:
        pargs.append("-batch")

    proc = subprocess.Popen(pargs, env=environ)

# Sleep to give time for T/HIS to start
    time.sleep(wait)

    proc.poll()
    if proc.returncode == 99:
        raise ValueError("Failed to start T/HIS. Port {} already in use. Cannot continue".format(portnum))
    elif proc.returncode == 98:
        raise ValueError("Failed to start gRPC server in T/HIS. Cannot continue")
    elif proc.returncode:
        raise ValueError("Failed to start T/HIS. Cannot continue")

    return connect(portnum, memory, 'localhost', debug)


def connect(port=50052, memory=25, hostname='localhost', debug=False):
    if debug:
        print("Called connect with port {} and memory {}".format(port, memory))

    Oasys.THIS._debug      = debug
    Oasys.THIS._connection = Oasys.gRPC.Connection("T/HIS", port, memory, hostname, debug)

# Check version
    version  = importlib.metadata.version('Oasys.THIS')
    modMajor = int(version.split('.')[0]);
    exeMajor = int(Oasys.THIS._connection.version);

    if debug:
        print("Oasys.THIS module version {} ({})".format(modMajor, version))
        print("THIS executable version {} ({})".format(exeMajor, Oasys.THIS._connection.version))

    if exeMajor != modMajor:
        raise ValueError("Major version ({}) of T/HIS executable {} != major version ({}) of Oasys.THIS module {}. Cannot continue".format(exeMajor, Oasys.THIS._connection.version, modMajor, version))

    return Oasys.THIS._connection


def disconnect(connection):
    if Oasys.THIS._debug:
        print("Called disconnect")

    connection.finalise()
    Oasys.THIS._connection = None


def terminate(connection):
    if Oasys.THIS._debug:
        print("Called terminate")

    connection.terminate()
    Oasys.THIS._connection = None


def createInstance(t, h):
# Classes in T/HIS
    if t == "Colour":
        instance = object.__new__(Oasys.THIS.Colour)
    elif t == "Component":
        instance = object.__new__(Oasys.THIS.Component)
    elif t == "Constant":
        instance = object.__new__(Oasys.THIS.Constant)
    elif t == "Curve":
        instance = object.__new__(Oasys.THIS.Curve)
    elif t == "Datum":
        instance = object.__new__(Oasys.THIS.Datum)
    elif t == "Entity":
        instance = object.__new__(Oasys.THIS.Entity)
    elif t == "Graph":
        instance = object.__new__(Oasys.THIS.Graph)
    elif t == "Group":
        instance = object.__new__(Oasys.THIS.Group)
    elif t == "LineStyle":
        instance = object.__new__(Oasys.THIS.LineStyle)
    elif t == "LineWidth":
        instance = object.__new__(Oasys.THIS.LineWidth)
    elif t == "Model":
        instance = object.__new__(Oasys.THIS.Model)
    elif t == "Operate":
        instance = object.__new__(Oasys.THIS.Operate)
    elif t == "Options":
        instance = object.__new__(Oasys.THIS.Options)
    elif t == "Page":
        instance = object.__new__(Oasys.THIS.Page)
    elif t == "Read":
        instance = object.__new__(Oasys.THIS.Read)
    elif t == "Symbol":
        instance = object.__new__(Oasys.THIS.Symbol)
    elif t == "UnitSystem":
        instance = object.__new__(Oasys.THIS.UnitSystem)
    elif t == "Units":
        instance = object.__new__(Oasys.THIS.Units)
    elif t == "Utils":
        instance = object.__new__(Oasys.THIS.Utils)
    elif t == "Window":
        instance = object.__new__(Oasys.THIS.Window)
    elif t == "Workflow":
        instance = object.__new__(Oasys.THIS.Workflow)

# Generic object
    elif t == "ItemObject":
        instance = object.__new__(Oasys.THIS.ItemObject)

# Unsupported
    else:
        raise NotImplementedError("Instance type '{}' not implemented".format(t))

    instance.__dict__['_handle']  = h;
    instance.__dict__['_objtype'] = t;

    return instance

