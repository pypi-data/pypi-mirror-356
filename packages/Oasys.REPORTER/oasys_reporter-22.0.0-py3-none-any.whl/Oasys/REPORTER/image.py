import Oasys.gRPC


# Metaclass for static properties and constants
class ImageType(type):
    _consts = {'BMP', 'JPG', 'PNG'}

    def __getattr__(cls, name):
        if name in ImageType._consts:
            return Oasys.REPORTER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Image class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in ImageType._consts:
            raise AttributeError("Cannot set Image class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Image(Oasys.gRPC.OasysItem, metaclass=ImageType):
    _props = {'antialiasing', 'fillColour', 'font', 'fontAngle', 'fontColour', 'fontJustify', 'fontSize', 'fontStyle', 'height', 'lineCapStyle', 'lineColour', 'lineJoinStyle', 'lineStyle', 'lineWidth', 'width'}


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
        if name in Image._props:
            return Oasys.REPORTER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Image instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Image._props:
            Oasys.REPORTER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, width, height, backgroundcolour=Oasys.gRPC.defaultArg):
        handle = Oasys.REPORTER._connection.constructor(self.__class__.__name__, width, height, backgroundcolour)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Image object for creating an image.
        If only 2 arguments are given they are used as the width and height of the image.
        The third argument can be used to define the initial background colour (the default is white)

        Parameters
        ----------
        width : integer
            Width of image
        height : integer
            Height of image
        backgroundcolour : string
            Optional. Initial background colour for the image (default is white). Can be "none", a valid
            colour from the X colour database (For Linux users, see /etc/X11/rgb.txt) e.g. "Blue", or #RRGGBB (each of R, G
            and B is a single hex digit) e.g. "#0000FF" for blue

        Returns
        -------
        Image
            Image object
        """


# Instance methods
    def Ellipse(self, x1, y1, x2, y2):
        """
        Draw an ellipse on an image

        Parameters
        ----------
        x1 : integer
            X coordinate of start position for ellipse
        y1 : integer
            Y coordinate of start position for ellipse
        x2 : integer
            X coordinate of end position for ellipse
        y2 : integer
            Y coordinate of end position for ellipse

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Ellipse", x1, y1, x2, y2)

    def Fill(self, x, y, tol=Oasys.gRPC.defaultArg):
        """
        Fill an area in an image with a colour

        Parameters
        ----------
        x : integer
            X coordinate of start position for fill
        y : integer
            Y coordinate of start position for fill
        tol : integer
            Optional. Tolerance for colour matching (0-255). Default is 0. When filling
            a shape if the red, green and blue components are within tol of the colour of
            pixel (x, y) the pixel will be filled with the current fill colour

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Fill", x, y, tol)

    def Line(self, x1, y1, x2, y2):
        """
        Draw a line on an image

        Parameters
        ----------
        x1 : integer
            X coordinate of start position for line
        y1 : integer
            Y coordinate of start position for line
        x2 : integer
            X coordinate of end position for line
        y2 : integer
            Y coordinate of end position for line

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Line", x1, y1, x2, y2)

    def Load(self, filename):
        """
        Load an image file (gif, png, bmp or jpeg)

        Parameters
        ----------
        filename : string
            Imagename you want to load

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Load", filename)

    def PixelCount(self, colour, tol=Oasys.gRPC.defaultArg):
        """
        Count the number of pixels in an image that have a specific colour

        Parameters
        ----------
        colour : string
            A valid colour from the X colour database (For Linux users, see /etc/X11/rgb.txt) e.g. "Blue", or
            #RRGGBB (each of R, G and B is a single hex digit) e.g. "#0000FF" for blue
        tol : integer
            Optional. Tolerance for colour matching (0-255). Default is 0. When looking
            at pixels if the red, green and blue components are within tol of the colour of
            pixel (x, y) the pixel will be counted

        Returns
        -------
        int
            Number of pixels (integer) with the colour
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "PixelCount", colour, tol)

    def Polygon(self, points):
        """
        Draw a polygon on an image. The last point is always connected back to the first point

        Parameters
        ----------
        points : list
            List of point coordinates

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Polygon", points)

    def Polyline(self, points):
        """
        Draw a line with multiple straight segments on an image

        Parameters
        ----------
        points : list
            List of point coordinates

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Polyline", points)

    def Rectangle(self, x1, y1, x2, y2):
        """
        Draw a rectangle on an image

        Parameters
        ----------
        x1 : integer
            X coordinate of start position for rectangle
        y1 : integer
            Y coordinate of start position for rectangle
        x2 : integer
            X coordinate of end position for rectangle
        y2 : integer
            Y coordinate of end position for rectangle

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Rectangle", x1, y1, x2, y2)

    def Save(self, filename, filetype):
        """
        Save an image to file (png, bmp or jpeg)

        Parameters
        ----------
        filename : string
            Imagename you want to save
        filetype : constant
            Type you want to save as. Can be:
            Image.BMP,
            Image.JPG or
            Image.PNG

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Save", filename, filetype)

    def Star(self, x, y, r):
        """
        Draw a star on an image

        Parameters
        ----------
        x : integer
            X coordinate of centre of star
        y : integer
            Y coordinate of centre of star
        r : integer
            Radius of star

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Star", x, y, r)

    def Text(self, x, y, text):
        """
        Draw text on an image

        Parameters
        ----------
        x : integer
            X position for text
        y : integer
            Y position for text
        text : string
            Text to write on image

        Returns
        -------
        None
            no return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Text", x, y, text)

