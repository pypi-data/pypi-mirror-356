import Oasys.gRPC


def Batch():
    """
    This method can be used to test whether REPORTER is running in batch mode or not

    Returns
    -------
    bool
        True/False
    """
    return Oasys.REPORTER._connection.functionCall("Batch")


def Debug(string):
    """
    Print a string to log file for debugging. Anything that you call the debug method on will
    be 'printed' to the log file window. Note that a carriage return will automatically be added

    Parameters
    ----------
    string : Any valid javascript type
        The string/item that you want to debug

    Returns
    -------
    None
        No return value
    """
    return Oasys.REPORTER._connection.functionCall("Debug", string)


def GetCurrentDirectory():
    """
    Return the current working directory for REPORTER

    Returns
    -------
    str
        string
    """
    return Oasys.REPORTER._connection.functionCall("GetCurrentDirectory")


def LogError(message):
    """
    Print an error to log file. Anything that you print will be output
    to the log file window in bold red text. Note that a carriage return will automatically be
    added

    Parameters
    ----------
    message : Any valid javascript type
        The
        string/item that you want to print

    Returns
    -------
    None
        No return value
    """
    return Oasys.REPORTER._connection.functionCall("LogError", message)


def LogPrint(message):
    """
    Print a string to log file. Anything that you print will be output
    to the log file window. Note that a carriage return will automatically be added

    Parameters
    ----------
    message : Any valid javascript type
        The string/item that you want to print

    Returns
    -------
    None
        No return value
    """
    return Oasys.REPORTER._connection.functionCall("LogPrint", message)


def LogWarning(message):
    """
    Print a warning to log file. Anything that you print will be output
    to the log file window in red text. Note that a carriage return will automatically be added

    Parameters
    ----------
    message : Any valid javascript type
        The string/item that you want to print

    Returns
    -------
    None
        No return value
    """
    return Oasys.REPORTER._connection.functionCall("LogWarning", message)


def SetCurrentDirectory(directory):
    """
    Set the current working directory for REPORTER

    Parameters
    ----------
    directory : string
        The directory that you want to change to

    Returns
    -------
    bool
        True if successful, False if not
    """
    return Oasys.REPORTER._connection.functionCall("SetCurrentDirectory", directory)


def System(string):
    """
    Do a system command outside REPORTER

    Parameters
    ----------
    string : Any valid javascript type
        The system command that you want to do

    Returns
    -------
    int
        integer (probably zero if command successful but is implementation-dependant)
    """
    return Oasys.REPORTER._connection.functionCall("System", string)


def Unix():
    """
    Test whether script is running on a Unix/Linux operating system. See also
    Windows()

    Returns
    -------
    bool
        True if Unix/Linux, False if not
    """
    return Oasys.REPORTER._connection.functionCall("Unix")


def Windows():
    """
    Test whether script is running on a Windows operating system. See also
    Unix()

    Returns
    -------
    bool
        True if Windows, False if not
    """
    return Oasys.REPORTER._connection.functionCall("Windows")
