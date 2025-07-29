from builtins import super, int

from ..tecutil import sv
from .. import session


class FieldPlotHOESettings(session.Style):
    def __init__(self, frame):
        self.frame = frame
        super().__init__(sv.HOESETTINGS, uniqueid=frame.uid)

    @property
    def num_subdivision_levels(self):
        """`int`: Refine element decomposition.

        With a default setting of 1, the elements are subdivided using only the
        natural nodes. A value of 2 subdivides elements one level below the
        natural nodes. Greater than 2 further refines the element decomposition
        and is more accurate, using the basis functions to compute the
        manufactured sub-element node values. Each level of subdivisions
        increases accuracy and time required to render. As a special case, a
        value of zero is permitted, instructing Tecplot to ignore the high order
        natural nodes using only the corner nodes for rendering. Example usage::

            >>> plot.hoe_settings.num_subdivision_levels = 3
        """
        return self._get_style(int, sv.NUMSUBDIVISIONLEVELS)

    @num_subdivision_levels.setter
    def num_subdivision_levels(self, value):
        self._set_style(int(value), sv.NUMSUBDIVISIONLEVELS)

    @property
    def minmax_scaling_factor(self):
        """`float`: Widens or narrows the buffer around sub-element filtering.

        The default value is 1.0. When filtering sub-elements, the extrema
        (min/max) of an iso-surface or probe variable for the nodes of an
        sub-element is multiplied by the factor and added as a buffer around the
        variable min/max range. Example usage::

            >>> plot.hoe_settings.minmax_scaling_factor = 4.0
        """
        return self._get_style(float, sv.MINMAXSCALINGFACTOR)

    @minmax_scaling_factor.setter
    def minmax_scaling_factor(self, value):
        self._set_style(float(value), sv.MINMAXSCALINGFACTOR)
