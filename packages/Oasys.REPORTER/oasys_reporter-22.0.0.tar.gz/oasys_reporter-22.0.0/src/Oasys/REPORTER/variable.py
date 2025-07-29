import Oasys.gRPC


# Metaclass for static properties and constants
class VariableType(type):
    _consts = {'DESCRIPTION', 'FORMAT', 'FORMAT_FLOAT', 'FORMAT_GENERAL', 'FORMAT_INTEGER', 'FORMAT_LOWERCASE', 'FORMAT_NONE', 'FORMAT_SCIENTIFIC', 'FORMAT_UPPERCASE', 'NAME', 'PRECISION', 'READONLY', 'TEMPORARY', 'TYPE', 'VALUE'}

    def __getattr__(cls, name):
        if name in VariableType._consts:
            return Oasys.REPORTER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Variable class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in VariableType._consts:
            raise AttributeError("Cannot set Variable class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Variable(Oasys.gRPC.OasysItem, metaclass=VariableType):
    _props = {'description', 'format', 'name', 'precision', 'readonly', 'temporary', 'type', 'value'}


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

# If one of the properties we define then get it
        if name in Variable._props:
            return Oasys.REPORTER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Variable instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Variable._props:
            Oasys.REPORTER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, template, name, description=Oasys.gRPC.defaultArg, value=Oasys.gRPC.defaultArg, type=Oasys.gRPC.defaultArg, readonly=Oasys.gRPC.defaultArg, temporary=Oasys.gRPC.defaultArg):
        handle = Oasys.REPORTER._connection.constructor(self.__class__.__name__, template, name, description, value, type, readonly, temporary)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Variable.
        The template and name arguments MUST be given, all others are optional

        Parameters
        ----------
        template : Template
            Template object to create variable in
        name : string
            Name of variable
        description : string
            Optional. Description of variable
        value : string
            Optional. Variable value
        type : string
            Optional. Type of variable. Predefined types are "Directory", "File(absolute)", "File(basename)",
            "File(extension)", "File(tail)", "General", "Number" and "String". Alternatively give your own type. e.g. "NODE ID". If
            omitted default is "General"
        readonly : boolean
            Optional. If variable is readonly or not. If omitted default is false
        temporary : boolean
            Optional. If variable is temporary or not. If omitted default is true

        Returns
        -------
        Variable
            Variable object
        """


# Static methods
    def GetAll(template):
        """
        Returns a list of Variable objects for all of the variables in a Template

        Parameters
        ----------
        template : Template
            Template to get the variables from

        Returns
        -------
        list
            List of Variable objects
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetAll", template)

    def GetFromName(template, name):
        """
        Returns the Variable object for a variable name

        Parameters
        ----------
        template : Template
            Template to find the variable in
        name : string
            name of the variable you want the Variable object for

        Returns
        -------
        Variable
            Variable object (or None if variable does not exist)
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetFromName", template, name)



# Instance methods
    def Remove(self):
        """
        Remove a variable
        Note that if you call this function for a Variable object,
        the Variable data will be deleted, so you should not try to use it afterwards!

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Remove")

