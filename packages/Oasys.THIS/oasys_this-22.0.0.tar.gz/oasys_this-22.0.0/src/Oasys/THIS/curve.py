import Oasys.gRPC


# Metaclass for static properties and constants
class CurveType(type):
    _consts = {'AFTER', 'BEFORE', 'Y1_AXIS', 'Y2_AXIS'}

    def __getattr__(cls, name):
        if name in CurveType._consts:
            return Oasys.THIS._connection.classGetter(cls.__name__, name)

        raise AttributeError("Curve class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in CurveType._consts:
            raise AttributeError("Cannot set Curve class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Curve(Oasys.gRPC.OasysItem, metaclass=CurveType):
    _props = {'colour', 'directory', 'entity_id', 'entity_type', 'file', 'label', 'model', 'style', 'symbol', 'tag', 'title', 'unit_system', 'width', 'x_axis_label', 'x_axis_unit', 'y_axis', 'y_axis_label', 'y_axis_unit'}
    _rprops = {'average', 'hic', 'hic_tmax', 'hic_tmin', 'hicd', 'hicd_tmax', 'hicd_tmin', 'id', 'is_null', 'npoints', 'regr_rsq', 'regr_sdgrad', 'regr_sdicpt', 'regr_sdyx', 'rms', 'tms', 'tms_tmax', 'tms_tmin', 'x_at_ymax', 'x_at_ymin', 'xmax', 'xmin', 'ymax', 'ymin'}


    def __del__(self):
        if not Oasys.THIS._connection:
            return

        if self._handle is None:
            return

        Oasys.THIS._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If constructor for an item fails in program, then _handle will not be set and when
# __del__ is called to return the object we will call this to get the (undefined) value
        if name == "_handle":
            return None

# If one of the properties we define then get it
        if name in Curve._props:
            return Oasys.THIS._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Curve._rprops:
            return Oasys.THIS._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError("Curve instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Curve._props:
            Oasys.THIS._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Curve._rprops:
            raise AttributeError("Cannot set read-only Curve instance attribute '{}'".format(name))

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, lcid, tag=Oasys.gRPC.defaultArg, line_label=Oasys.gRPC.defaultArg, x_axis_label=Oasys.gRPC.defaultArg, y_axis_label=Oasys.gRPC.defaultArg):
        handle = Oasys.THIS._connection.constructor(self.__class__.__name__, lcid, tag, line_label, x_axis_label, y_axis_label)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Create a new Curve object. 
        The curve will be added to all the currently active graphs

        Parameters
        ----------
        lcid : integer
            Curve number
        tag : string
            Optional. Tag used to reference the curve in FAST-TCF scripts
        line_label : string
            Optional. Line label for the curve
        x_axis_label : string
            Optional. X-axis label for the curve
        y_axis_label : string
            Optional. Y-axis label for the curve

        Returns
        -------
        Curve
            Curve object
        """


# Static methods
    def AddFlaggedToGraph(flag, *graph):
        """
        Adds flagged curves to a graph

        Parameters
        ----------
        flag : Flag
            Flag to check on the curve
        *graph : int
            Graph to add the curve to. If undefined then the curve is added to all graphs
            This argument can be repeated if required.
            Alternatively a single array argument containing the multiple values can be given

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "AddFlaggedToGraph", flag, graph)

    def Copy(source, target):
        """
        Copies a curve

        Parameters
        ----------
        source : integer
            ID of curve to copy from
        target : integer
            ID of curve to copy to

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Copy", source, target)

    def Delete(curve):
        """
        Deletes a curve

        Parameters
        ----------
        curve : integer
            ID of curve to delete

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Delete", curve)

    def DeleteFlagged(flag):
        """
        Deletes flagged curves

        Parameters
        ----------
        flag : Flag
            Flag to check on the curve

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "DeleteFlagged", flag)

    def Exists(curve):
        """
        Checks if a curve exists

        Parameters
        ----------
        curve : integer
            ID of curve to check

        Returns
        -------
        bool
            True if the curve exists, otherwise False
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Exists", curve)

    def First():
        """
        Returns the first curve

        Returns
        -------
        Curve
            Curve object (or None if there are no more curves in the model)
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "First")

    def FirstFreeID():
        """
        Returns the ID of the first free curve

        Returns
        -------
        int
            ID of first unsued curve
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "FirstFreeID")

    def FirstID():
        """
        Returns the ID of the first curve

        Returns
        -------
        int
            ID of the first curve defined
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "FirstID")

    def FlagAll(flag):
        """
        Flags all of the curves with a defined flag

        Parameters
        ----------
        flag : integer
            Flag to set on the curves

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "FlagAll", flag)

    def GetFlagged(flag):
        """
        Returns a list of all curves flagged with a given flag

        Parameters
        ----------
        flag : Flag
            Flag for which to return flagged objects

        Returns
        -------
        list
            List of Curve objects (or None if no curves are flagged)
        """
        return Oasys.THIS._connection.classMethodStream(__class__.__name__, "GetFlagged", flag)

    def GetFromID(id):
        """
        Returns the curve object for a curve ID

        Parameters
        ----------
        id : integer
            ID of curve to return object for

        Returns
        -------
        Curve
            Curve object (or None if the curve does not exist
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "GetFromID", id)

    def HighestID():
        """
        Returns the ID of the highest curve currently being used

        Returns
        -------
        int
            ID of highest curve currently being used
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "HighestID")

    def Pick(prompt, modal=Oasys.gRPC.defaultArg):
        """
        Picks a single curve

        Parameters
        ----------
        prompt : string
            Text to display as a prompt to the user
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in T/HIS
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        Curve
            Curve object (or None if the user cancels the pick operation)
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Pick", prompt, modal)

    def RemoveFlaggedFromGraph(flag, *graph):
        """
        Removes flagged curves from a graph

        Parameters
        ----------
        flag : Flag
            Flag to check on the curve
        *graph : int
            Graph to remove the curve from. If undefined then the curve is removed from all graphs
            This argument can be repeated if required.
            Alternatively a single array argument containing the multiple values can be given

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "RemoveFlaggedFromGraph", flag, graph)

    def Select(flag, prompt, modal=Oasys.gRPC.defaultArg):
        """
        Allows the user to select curves

        Parameters
        ----------
        flag : integer
            Flag to use when selecting curves
        prompt : string
            Text to display as a prompt to the user
        modal : boolean
            Optional. If selection is modal (blocks the user from doing anything else in T/HIS
            until this window is dismissed). If omitted the selection will be modal

        Returns
        -------
        int
            Number of items selected or None if menu cancelled
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Select", flag, prompt, modal)

    def UnflagAll(flag):
        """
        Unsets a defined flag on all of the curves

        Parameters
        ----------
        flag : integer
            Flag to unset on the curves

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "UnflagAll", flag)



# Instance methods
    def AddPoint(self, xvalue, yvalue):
        """
        Adds a point at the end of the curve

        Parameters
        ----------
        xvalue : real
            The x value of the point
        yvalue : real
            The y value of the point

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "AddPoint", xvalue, yvalue)

    def AddToGraph(self, *graph):
        """
        Adds a curve to a graph

        Parameters
        ----------
        *graph : int
            Graph to add the curve to. If undefined then the curve is added to all graphs
            This argument can be repeated if required.
            Alternatively a single array argument containing the multiple values can be given

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "AddToGraph", graph)

    def ClearFlag(self, flag):
        """
        Clears a flag on the curve

        Parameters
        ----------
        flag : integer
            Flag to clear on the curve

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def DeletePoint(self, ipt):
        """
        Deletes a point in a curve. The input
        for the point number should start at 1 for the 1st point not zero

        Parameters
        ----------
        ipt : integer
            The point you want to insert the data before or after

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "DeletePoint", ipt)

    def Flagged(self, flag):
        """
        Checks if the curve is flagged or not

        Parameters
        ----------
        flag : integer
            Flag to check on the curve

        Returns
        -------
        bool
            True if flagged, False if not
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def Freeze(self, graph, freeze_option):
        """
        Freezes an unblanked curve on one or all graphs

        Parameters
        ----------
        graph : integer
            Graph number to freeze curve on or 0 for all graphs
        freeze_option : integer
            No argument or 1 to freeze the curve, 0 to unfreeze

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "Freeze", graph, freeze_option)

    def GetPoint(self, row):
        """
        Returns x and y data for a point in a curve. The input
        for the point number should start at 1 for the 1st point not zero. In the list
        returned list[0] contains the x axis value and list[1] contains the y-axis value

        Parameters
        ----------
        row : integer
            The point you want the data for

        Returns
        -------
        list
            Array of point values
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "GetPoint", row)

    def InsertPoint(self, ipt, xvalue, yvalue, position):
        """
        Inserts a new point before or after the specified point

        Parameters
        ----------
        ipt : integer
            The point you want to insert the data before or after
        xvalue : real
            The x value of the point
        yvalue : real
            The y value of the point
        position : integer
            Specify either before or after the selected pioint. Use 'Curve.BEFORE' for before, and 'Curve.AFTER' for after

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "InsertPoint", ipt, xvalue, yvalue, position)

    def Next(self):
        """
        Returns the next curve in the model

        Returns
        -------
        Curve
            Curve object (or None if there are no more curves in the model)
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous curve in the model

        Returns
        -------
        Curve
            Curve object (or None if there are no more curves in the model)
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def RemoveFromGraph(self, *graph):
        """
        Removes a curve from a graph

        Parameters
        ----------
        *graph : int
            Graph to remove the curve from, If undefined then the curve is removed from all graphs
            This argument can be repeated if required.
            Alternatively a single array argument containing the multiple values can be given

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "RemoveFromGraph", graph)

    def SetFlag(self, flag):
        """
        Sets a flag on the curve

        Parameters
        ----------
        flag : integer
            Flag to set on the curve

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def SetPoint(self, ipt, xvalue, yvalue):
        """
        Sets the x and y values for a specified point in a curve

        Parameters
        ----------
        ipt : integer
            The point to set the data for
        xvalue : real
            The x value of the point
        yvalue : real
            The y value of the point

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "SetPoint", ipt, xvalue, yvalue)

    def Update(self):
        """
        Updates a curve properties (min,max, average values etc)

        Returns
        -------
        None
            No return value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "Update")

    def YatX(self, xvalue):
        """
        Returns the y value of the curve at a given x value, interpolating if requested x value lies between data points

        Parameters
        ----------
        xvalue : real
            The x value

        Returns
        -------
        float
            Y value
        """
        return Oasys.THIS._connection.instanceMethod(self.__class__.__name__, self._handle, "YatX", xvalue)

