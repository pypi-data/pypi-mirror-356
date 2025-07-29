from builtins import str, super

from ..tecutil import sv
from .. import session, constant, tecutil, text
from . import legend

class LegendHeader(session.Style):
    """
    """
    def __init__(self, legend, *svargs):
        self.legend = legend
        super().__init__(legend._sv, sv.HEADER, **legend._kw)

    @property
    def show(self):
        """`bool`: Show or hide the contour legend header.

        .. note::

            The header text will display the name of the variable assigned to
            the contour group or a custom text if the `use_custom_text` is set
            to True.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> plot = frame.plot(PlotType.Cartesian3D)
            >>> legend_header = plot.contour(0).legend.header
            >>> legend_header.show = True
        """
        return self._get_style(bool, sv.SHOW)

    @show.setter
    def show(self, value):
        self._set_style(bool(value), sv.SHOW)

    @property
    def font(self):
        """`text.Font`: Font used to display the legend header.

        .. note::

            The font `size_units <tecplot.text.Font.size_units>` property
            may only be set to `Units.Frame` or `Units.Point`.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> legend = frame.plot(PlotType.Cartesian3D).contour(0).legend
            >>> legend.header.font.italic = True
        """
        return text.LegendFont(self, sv.TEXTSHAPE)

    @property
    def use_custom_text(self):
        """ `bool`: Use custom text on the contour legend header.

        If set to `True`, the legend header will be set by the `custom_text`
        property instead of the variable name assigned to the contour group.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> plot = frame.plot(PlotType.Cartesian3D)
            >>> header = plot.contour(0).legend.header
            >>> header.use_custom_text = True
            >>> header.custom_text = 'Solution time: &(SOLUTIONTIME) ms'

        See also: `LegendHeader.custom_text`

        .. versionadded:: 2021.2

            The ability to specify custom contour legend header text requires
            Tecplot 360 2021 R2 or later.

        .. versionadded:: 1.4.2
        """
        return self._get_style(bool, sv.USECUSTOMTEXT)

    @use_custom_text.setter
    def use_custom_text(self, value):
        self._set_style(bool(value), sv.USECUSTOMTEXT)

    @property
    def custom_text(self):
        """ `str`: A string to be used in the contour legend header.

        If the `use_custom_text` property is set to `True`, the legend header
        will contain this text instead of the name of the variable assigned to
        the contour group. The text may contain Dynamic Text and formatting
        tags (see User Manual).

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> plot = frame.plot(PlotType.Cartesian3D)
            >>> header = plot.contour(0).legend.header
            >>> header.use_custom_text = True
            >>> header.custom_text = 'time: &(SOLUTIONTIME) <greek>ms</greek>'

        See also: `LegendHeader.use_custom_text`

        .. versionadded:: 2021.2

            The ability to specify custom contour legend header text requires
            Tecplot 360 2021 R2 or later.

        .. versionadded:: 1.4.2
        """
        return self._get_style(str, sv.CUSTOMTEXT)

    @custom_text.setter
    def custom_text(self, value):
        self._set_style(str(value), sv.CUSTOMTEXT)

    @property
    def text_type(self):
        r"""`TextType`: Typesetter for the contour legend header.

        This determines how the header text for the contour legend
        is rendered. Options are `TextType.Regular` or `TextType.LaTeX`.
        When using ``LaTeX``, make sure to use Python raw strings so
        that literal back-slashes are preserved.

        Example usage::

            >>> from tecplot.constant import PlotType, TextType
            >>> plot = frame.plot(PlotType.Cartesian3D)
            >>> header = plot.contour(0).legend.header
            >>> header.text_type = TextType.LaTeX
            >>> header.use_custom_text = True
            >>> header.custom_text = r'\LaTeX'

        .. versionadded:: 2022.1

            The ability to use LaTeX for contour legend header text requires
            Tecplot 360 2022 R1 or later.

        .. versionadded:: 1.5.0
        """
        return self._get_style(constant.TextType, sv.TEXTTYPE)

    @text_type.setter
    def text_type(self, value):
        self._set_style(constant.TextType(value), sv.TEXTTYPE)


class ContourLegend(legend.TabularLegend):
    """Contour legend attributes.

    This class allows you to customize the appearance of the contour legend.
    The contour legend can be positioned anywhere inside the frame using the
    `position` attribute of this class.  Example usage:

    .. code-block:: python
        :emphasize-lines: 21-36

        import os
        import numpy as np

        import tecplot
        from tecplot.constant import *

        # By loading a layout many style and view properties are set up already
        examples_dir = tecplot.session.tecplot_examples_directory()
        datafile = os.path.join(examples_dir, 'SimpleData', 'RainierElevation.lay')
        tecplot.load_layout(datafile)

        frame = tecplot.active_frame()
        plot = frame.plot()

        # Rename the elevation variable
        frame.dataset.variable('E').name = "Elevation (m)"

        # Set the levels to nice values
        plot.contour(0).levels.reset_levels(np.linspace(200,4400,22))

        legend = plot.contour(0).legend
        legend.show = True
        legend.vertical = False  # Horizontal
        legend.auto_resize = False
        legend.label_step = 5

        legend.overlay_bar_grid = False
        legend.position = (55, 94)  # Frame percentages

        legend.box.box_type = TextBox.None_ # Remove Text box

        legend.header.font.typeface = 'Courier'
        legend.header.font.bold = True

        legend.number_font.typeface = 'Courier'
        legend.number_font.bold = True

        tecplot.export.save_png('legend_contour.png', 600, supersample=3)

    .. figure:: /_static/images/legend_contour.png
        :width: 300px
        :figwidth: 300px
    """
    def __init__(self, contour, *svargs):
        self.contour = contour
        super().__init__(contour._sv, sv.LEGEND, **contour._kw)

    @tecutil.inherited_property(legend.Legend)
    def show(self):
        """`bool`: Show or hide the legend.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> legend = frame.plot(PlotType.Cartesian3D).contour(0).legend
            >>> legend.show = True
        """

    @tecutil.inherited_property(legend.Legend)
    def anchor_alignment(self):
        """`AnchorAlignment`: Anchor location of the legend.

        Example usage::

            >>> from tecplot.constant import PlotType, AnchorAlignment
            >>> legend = frame.plot(PlotType.Cartesian3D).contour(0).legend
            >>> legend.anchor_alignment = AnchorAlignment.BottomCenter
        """

    @tecutil.inherited_property(legend.Legend)
    def text_color(self):
        """`Color`: Color of legend text.

        Example usage::

            >>> from tecplot.constant import PlotType, Color
            >>> legend = frame.plot(PlotType.Cartesian3D).contour(0).legend
            >>> legend.text_color = Color.Blue
        """

    @tecutil.inherited_property(legend.Legend)
    def position(self):
        """`tuple`: Position as a percentage of frame width/height.

        The legend is automatically placed for you. You may specify the
        :math:`(x,y)` position of the legend by setting this value, where
        :math:`x` is the percentage of frame width, and :math:`y` is a
        percentage of frame height.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> legend = frame.plot(PlotType.Cartesian3D).contour(0).legend
            >>> legend.position = (.1, .3)
            >>> pos = legend.position
            >>> pos.x  # == position[0]
            .1
            >>> pos.y  # == position[1]
            .3
        """

    @tecutil.inherited_property(legend.Legend)
    def box(self):
        """`text.TextBox`: Legend box attributes.

        Example usage::

            >>> from tecplot.constant import PlotType, Color
            >>> legend = frame.plot(PlotType.Cartesian3D).contour(0).legend
            >>> legend.box.color = Color.Blue
        """

    @tecutil.inherited_property(legend.TabularLegend)
    def row_spacing(self):
        """`float`: Spacing between rows in the legend.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> legend = frame.plot(PlotType.Cartesian3D).contour(0).legend
            >>> legend.row_spacing = 1.5
        """

    @property
    def auto_resize(self):
        """`bool`: Skip levels to create a reasonably sized legend.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> legend = frame.plot(PlotType.Cartesian3D).contour(0).legend
            >>> legend.auto_resize = True
        """
        return self._get_style(bool, sv.AUTORESIZE)

    @auto_resize.setter
    def auto_resize(self, value):
        self._set_style(bool(value), sv.AUTORESIZE)

    @property
    def header_font(self):
        if __debug__:
            tecutil.api_moved('ContourLegend.header_font',
                              'ContourLegend.header.font',
                              '1.4.2', '2021 R1', warning=True)
        return text.LegendFont(self, sv.HEADERTEXTSHAPE)

    @property
    def number_font(self):
        """`text.Font`: Font used to display numbers in the legend.

        .. note::
            The font `size_units <tecplot.text.Font.size_units>` property
            may only be set to `Units.Frame` or `Units.Point`.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> legend = frame.plot(PlotType.Cartesian3D).contour(0).legend
            >>> legend.number_font.italic = True
        """
        return text.LegendFont(self, sv.NUMBERTEXTSHAPE)

    @property
    def show_cutoff_levels(self):
        """`bool`: Show color bands for levels affected by color cutoff.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> legend = frame.plot(PlotType.Cartesian3D).contour(0).legend
            >>> legend.show_cutoff_levels = True
        """
        return self._get_style(bool, sv.INCLUDECUTOFFLEVELS)

    @show_cutoff_levels.setter
    def show_cutoff_levels(self, value):
        self._set_style(bool(value), sv.INCLUDECUTOFFLEVELS)

    @property
    def include_cutoff_levels(self):
        tecutil.api_moved('ContourLegend.include_cutoff_levels',
                          'ContourLegend.show_cutoff_levels',
                          '0.13', '2018 R2')

    @include_cutoff_levels.setter
    def include_cutoff_levels(self, value):
        tecutil.api_moved('ContourLegend.include_cutoff_levels',
                          'ContourLegend.show_cutoff_levels',
                          '0.13', '2018 R2')

    @property
    def vertical(self):
        """`bool`: Orientation of the legend.

        When set to `True`, the legend is vertical. When set to `False`, the
        legend is horizontal.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> legend = frame.plot(PlotType.Cartesian3D).contour(0).legend
            >>> legend.vertical = False  # Show horizontal legend
        """
        return self._get_style(bool, sv.ISVERTICAL)

    @vertical.setter
    def vertical(self, value):
        self._set_style(bool(value), sv.ISVERTICAL)

    @property
    def label_increment(self):
        """`float`: Spacing between labels along the contour legend.

        Labels will be placed on the contour variable range from min to max.
        The smaller the increment value the more legend labels will be created.
        If the `label_location` is `ContLegendLabelLocation.Increment`, labels
        are incremented by this value. For example, a `label_increment` value
        of .5 will show labels at .5, 1.0, 1.5, etc.

        .. Note::

            This value is only used if `label_location` is set to
            `ContLegendLabelLocation.Increment`. Otherwise it is ignored.

        Example usage::

            >>> from tecplot.constant import PlotType, ContLegendLabelLocation
            >>> legend = frame.plot(PlotType.Cartesian3D).contour(0).legend
            >>> legend.label_location = ContLegendLabelLocation.Increment
            >>> legend.label_increment = .5

        .. seealso:: `label_location`
        """
        return self._get_style(float, sv.LABELINCREMENT)

    @label_increment.setter
    def label_increment(self, value):
        self._set_style(float(value), sv.LABELINCREMENT)

    @property
    def label_location(self):
        """`ContLegendLabelLocation`: Placement of labels on the legend.

        If you have selected `ColorMapDistribution.Continuous` for the contour
        colormap filter distribution, you have three options for placement of
        labels on the legend:

        * `ContLegendLabelLocation.ContourLevels` - This option places one
          label for each contour level. See Contour Levels and Color.
        * `ContLegendLabelLocation.Increment` - Set `label_increment` to the
          increment value.
        * `ContLegendLabelLocation.ColorMapDivisions` - Places one label for
          each control point on the color map.

        Example usage::

            >>> from tecplot.constant import PlotType, ContLegendLabelLocation
            >>> legend = frame.plot(PlotType.Cartesian3D).contour(0).legend
            >>> legend.label_location = ContourLevelLabelLocation.Increment
            >>> legend.label_increment = .5

        .. seealso:: `label_increment`
        """
        return self._get_style(constant.ContLegendLabelLocation,
                               sv.LABELLOCATION)

    @label_location.setter
    def label_location(self, value):
        self._set_style(constant.ContLegendLabelLocation(value),
                        sv.LABELLOCATION)

    @property
    def overlay_bar_grid(self):
        """`bool`: Draw a line around each band in the legend color bar.

        Example usage::

            >>> from tecplot.constant import PlotType
            >>> legend = frame.plot(PlotType.Cartesian3D).contour(0).legend
            >>> legend.overlay_bar_grid = False
        """
        return self._get_style(bool, sv.OVERLAYBARGRID)

    @overlay_bar_grid.setter
    def overlay_bar_grid(self, value):
        self._set_style(bool(value), sv.OVERLAYBARGRID)

    @property
    def header(self):
        """`LegendHeader`: `LegendHeader` associated with a `ContourLegend`.

        This object controls the attributes of the contour legend header.

        .. versionadded:: 1.4.2

            The contour legend header style control has been moved into a new
            namespace `header`:

            ============================== ==============================
            Old API                        New API
            ============================== ==============================
            ``contour.legend.show_header`` ``contour.legend.header.show``
            ``contour.legend.header_font`` ``contour.legend.header.font``
            ============================== ==============================

        Example usage::

            >>> plot.contour(0).legend.header.show = True
        """
        return LegendHeader(self)

    @property
    def show_header(self):
        if __debug__:
            tecutil.api_moved('ContourLegend.show_header',
                              'ContourLegend.header.show',
                              '1.4.2', '2021 R1', warning=True)
        return self._get_style(bool, sv.SHOWHEADER)

    @show_header.setter
    def show_header(self, value):
        if __debug__:
            tecutil.api_moved('ContourLegend.show_header',
                              'ContourLegend.header.show',
                              '1.4.2', '2021 R1', warning=True)
        self._set_style(bool(value), sv.SHOWHEADER)

    @property
    def label_step(self):
        """`int`: Step size between labels along the legend.

        This is an alias for `ContourLegend.contour.labels.step
        <ContourLabels.step>`::

            >>> contour = frame.plot().contour(0)
            >>> contour.legend.label_step = 3
            >>> print(contour.labels.step)
            3
        """
        return self.contour.labels.step

    @label_step.setter
    def label_step(self, step):
        self.contour.labels.step = step

    @property
    def label_format(self):
        """`LabelFormat`: Number formatting for labels along the legend.

        This is an alias for `ContourLegend.contour.labels.format
        <ContourLabels.format>`::

            >>> contour = frame.plot().contour(0)
            >>> contour.legend.label_format.precision = 3
            >>> print(contour.labels.format.precision)
            3
        """
        return self.contour.labels.format
