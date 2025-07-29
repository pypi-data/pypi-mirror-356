import Oasys.gRPC


# Metaclass for static properties and constants
class WindowType(type):
    _consts = {'CANCEL', 'NO', 'OK', 'YES'}

    def __getattr__(cls, name):
        if name in WindowType._consts:
            return Oasys.REPORTER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Window class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in WindowType._consts:
            raise AttributeError("Cannot set Window class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Window(Oasys.gRPC.OasysItem, metaclass=WindowType):


    def __del__(self):
        if not Oasys.REPORTER._connection:
            return

        if self._handle is None:
            return

        Oasys.REPORTER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If constructor for an item fails in program, then _handle will not be set and when
# __del__ is called to return the object we will call this to get the (undefined) value
        if name == "_handle":
            return None

        raise AttributeError("Window instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value


# Static methods
    def Error(title, error, buttons=Oasys.gRPC.defaultArg):
        """
        Show an error message in a window

        Parameters
        ----------
        title : string
            Title for window
        error : string
            Error message to show in window
        buttons : constant
            Optional. The buttons to use. Can be bitwise OR of Window.OK,
            Window.CANCEL,
            Window.YES or
            Window.NO. If this is omitted an OK button will be used

        Returns
        -------
        int
            Button pressed
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Error", title, error, buttons)

    def GetDirectory(initial=Oasys.gRPC.defaultArg):
        """
        Map the directory selector box native to your machine, allowing you to choose a directory

        Parameters
        ----------
        initial : string
            Optional. Initial directory to start from

        Returns
        -------
        str
            directory (string), (or None if cancel pressed)
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetDirectory", initial)

    def GetFile(extension=Oasys.gRPC.defaultArg, allow_new=Oasys.gRPC.defaultArg, initial=Oasys.gRPC.defaultArg):
        """
        Map a file selector box allowing you to choose a file.
        See also Window.GetFiles()

        Parameters
        ----------
        extension : string
            Optional. Extension to filter by
        allow_new : boolean
            Optional. Allow creation of new file
        initial : string
            Optional. Initial directory to start from

        Returns
        -------
        str
            filename (string), (or None if cancel pressed)
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetFile", extension, allow_new, initial)

    def GetFiles(extension=Oasys.gRPC.defaultArg):
        """
        Map a file selector box allowing you to choose multiple files.
        See also Window.GetFile()

        Parameters
        ----------
        extension : string
            Optional. Extension to filter by

        Returns
        -------
        str
            List of filenames (strings), or None if cancel pressed
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetFiles", extension)

    def GetInteger(title, message):
        """
        Map a window allowing you to input an integer. OK and Cancel buttons are shown

        Parameters
        ----------
        title : string
            Title for window
        message : string
            Message to show in window

        Returns
        -------
        int
            Integer. Value input, (or None if cancel pressed)
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetInteger", title, message)

    def GetNumber(title, message):
        """
        Map a window allowing you to input a number. OK and Cancel buttons are shown

        Parameters
        ----------
        title : string
            Title for window
        message : string
            Message to show in window

        Returns
        -------
        float
            Real. Value input, (or None if cancel pressed)
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetNumber", title, message)

    def GetOptions(title, message, options):
        """
        Map a window allowing you to input various options. OK and Cancel buttons are shown

        Parameters
        ----------
        title : string
            Title for window
        message : string
            Message to show in window
        options : list of dicts
            List of objects listing options that can be set. If OK is pressed the objects will be updated with
            the values from the widgets. If cancel is pressed they will not

        Returns
        -------
        bool
            False if cancel pressed, True if OK pressed
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetOptions", title, message, options)

    def GetString(title, message):
        """
        Map a window allowing you to input a string. OK and Cancel buttons are shown

        Parameters
        ----------
        title : string
            Title for window
        message : string
            Message to show in window

        Returns
        -------
        str
            String. Value input, (or None if cancel pressed)
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetString", title, message)

    def Information(title, info, buttons=Oasys.gRPC.defaultArg):
        """
        Show information in a window

        Parameters
        ----------
        title : string
            Title for window
        info : string
            Information to show in window
        buttons : constant
            Optional. The buttons to use. Can be bitwise OR of Window.OK,
            Window.CANCEL,
            Window.YES or
            Window.NO. If this is omitted an OK button will be used

        Returns
        -------
        int
            Button pressed
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Information", title, info, buttons)

    def Message(title, message, buttons=Oasys.gRPC.defaultArg):
        """
        Show a message in a window

        Parameters
        ----------
        title : string
            Title for window
        message : string
            Message to show in window
        buttons : constant
            Optional. The buttons to use. Can be bitwise OR of Window.OK,
            Window.CANCEL,
            Window.YES or
            Window.NO. If this is omitted an OK button will be used

        Returns
        -------
        int
            Button pressed
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Message", title, message, buttons)

    def Question(title, question, buttons=Oasys.gRPC.defaultArg):
        """
        Show a question in a window

        Parameters
        ----------
        title : string
            Title for window
        question : string
            Question to show in window
        buttons : constant
            Optional. The buttons to use. Can be bitwise OR of Window.OK,
            Window.CANCEL,
            Window.YES or
            Window.NO. If this is omitted Yes and No button will be
            used

        Returns
        -------
        int
            Button pressed
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Question", title, question, buttons)

    def Warning(title, warning, buttons=Oasys.gRPC.defaultArg):
        """
        Show a warning message in a window

        Parameters
        ----------
        title : string
            Title for window
        warning : string
            Warning message to show in window
        buttons : constant
            Optional. The buttons to use. Can be bitwise OR of Window.OK,
            Window.CANCEL,
            Window.YES or
            Window.NO. If this is omitted an OK button will be
            used

        Returns
        -------
        int
            Button pressed
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Warning", title, warning, buttons)

