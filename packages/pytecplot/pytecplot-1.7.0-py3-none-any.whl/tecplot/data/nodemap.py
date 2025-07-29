from builtins import super

import contextlib
import itertools as it
import logging
import textwrap

from ctypes import addressof, cast, c_int32, c_int64, c_void_p, POINTER

from ..tecutil import _tecutil, _tecutil_connector
from ..constant import *
from ..exception import *
from .. import session, tecutil
from .fe_cell_type import FECellType


log = logging.getLogger(__name__)


@tecutil.lock_attributes
class Elementmap(c_void_p):
    """Nodemap reverse look-up."""
    def __init__(self, zone):
        self.zone = zone
        super().__init__(self._native_reference())

    @tecutil.lock()
    def _native_reference(self):
        with self.zone.dataset.frame.activated():
            return _tecutil.DataNodeToElemMapGetReadableRef(self.zone.index + 1)

    def num_elements(self, node):
        return _tecutil.DataNodeToElemMapGetNumElems(self, node + 1)

    def element(self, node, offset):
        return _tecutil.DataNodeToElemMapGetElem(self, node + 1, offset + 1) - 1


@tecutil.lock_attributes
class NodemapBase(c_void_p):
    def __init__(self, zone):
        self.zone = zone
        super().__init__(self._native_reference())

    @tecutil.lock()
    def _native_reference(self, writable=False):
        _dispatch = {
            True: _tecutil.DataNodeGetWritableRef,
            False: _tecutil.DataNodeGetReadableRef}
        with self.zone.dataset.frame.activated():
            return _dispatch[writable](self.zone.index + 1)

    def __eq__(self, other):
        self_addr = addressof(cast(self, POINTER(c_int64)).contents)
        other_addr = addressof(cast(other, POINTER(c_int64)).contents)
        return self_addr == other_addr

    def __ne__(self, other):
        return not (self == other)

    def __len__(self):
        return self.zone.num_sections

    @contextlib.contextmanager
    def assignment(self):
        """Context manager for assigning to the nodemap.

        When setting values to the nodemap, a `state change` is emitted to the
        engine after every statement. This can degrade performance if in the
        script the nodemap is being set many times. This context provides a way
        to suspend the state change notification until all assignments have
        been completed. In the following example, the state change is emitted
        only after the ``nodemap.assignment()`` context exits::

            >>> nodemap = dataset.zone('My Zone').nodemap
            >>> with nodemap.assignment():
            ...     nodemap[:] = node_data
        """
        with session.suspend():
            yield
            session.connectivity_altered(self.zone)

    @property
    def c_type(self):
        """`ctypes.c_int32` or `ctypes.c_int64`: The underlying data type for
        this nodemap.

        .. note:: This property is read-only.

        This is the `ctypes` integer type used by the Tecplot Engine to store
        the nodemap data. This is used internally and is not normally needed
        for simple nodemap access.
        """
        _ctypes = {
            OffsetDataType.OffsetDataType_32Bit: c_int32,
            OffsetDataType.OffsetDataType_64Bit: c_int64}
        data_type = _tecutil.DataNodeGetRawItemType(self)
        return _ctypes[data_type]

    def num_elements(self, node):
        """The number of elements that use a given node.

        Parameters:
            node: (`int`): Zero-based index of a node.

        Returns:
            `int` - The number of elements that use this node.

        Example usage::

            >>> nodemap = dataset.zone('My Zone').nodemap
            >>> nodemap.num_elements(3)
            8
        """
        return Elementmap(self.zone).num_elements(node)

    def element(self, node, offset):
        """The element containing a given node.

        Parameters:
            node (`int`): Zero-based index of a node.
            offset (`int`): Zero-based index of the element that uses
                the given node.

        Returns:
            `int` - Zero-based index of the element.

        Example usage::

            >>> nodemap = dataset.zone('My Zone').nodemap
            >>> print(nodemap.element(3, 7))
            324
        """
        return Elementmap(self.zone).element(node, offset)


class Nodemap(NodemapBase):
    """Element to node map for a mixed-FE zone.

    This object maps elements (cells) to specific nodes (points) in the
    dataset. The elements are grouped by cell type into sections and each
    section stores the corners (linear part of the cell) separate from the
    high-order nodes of the cells into two different arrays.

    For more details, see the "working with datasets" examples shipped with
    PyTecplot in the Tecplot 360 distribution.
    """
    def __len__(self):
        return self.zone.num_sections

    def section(self, index):
        """Returns a `NodemapSection` of the nodemap.

        Each section of a `Nodemap` consists of a mapping for a specific cell
        type. The data may be linear or higher-order.

        Parameters:
            index (`int`): The zero-based section index.

        Example usage::

            >>> zone = dataset.zone('My Zone')
            >>> nmap_section = zone.nodemap.section(0)
            >>> print(nmap_section.cell_shape)
            FECellShape.Tetrahedron
        """
        return NodemapSection(self, index)

    def __getitem__(self, section_index):
        return self.section(section_index)

    def __iter__(self):
        self._current_section = -1
        self._num_sections = len(self)
        return self

    def __next__(self):
        self._current_section += 1
        if self._current_section == self._num_sections:
            raise StopIteration
        return self.section(self._current_section)

    def section_element(self, element):
        """Returns the section and element within that section for a
        globally-indexed element.

        Parameters:
            element (`int`): The zero-based element index spanning all sections
                in the nodemap.

        Returns: `tuple` of `int` (zero-based) indices: ``(section, element)``.

        Example usage::

            >>> zone = dataset.zone('My Zone')
            >>> print(zone.nodemap.section_element(1))
            (0, 1)
        """
        cumulative_elements = 0
        for section in range(self.zone.num_sections):
            num_elements = self.zone.section_metrics(section).num_elements
            if element < (cumulative_elements + num_elements):
                return (section, element - cumulative_elements)
            else:
                cumulative_elements += num_elements

    def nodes(self, element, section=None):
        """Returns node values for a specific element.

        Parameters:
            element (`int`): Element index with in the section if specified,
                otherwise this is the element index across all sections.
            section (`int`, optional): Section index. If no section is
                speficied, the element index will span across all sections.

        Example usage::

            >>> zone = dataset.zone('My Zone')
            >>> print(zone.nodemap.nodes(1))
            (0, 1, 3, 4)
        """
        if section is None:
            section, element = self.section_element(element)
        return self.section(section).nodes(element)

    def num_elements(self, node):
        """The number of elements that use a given node.

        Parameters:
            node: (`int`): Zero-based index of a node.

        Returns:
            `int` - The number of elements that use this node.

        Example usage::

            >>> nodemap = dataset.zone('My Zone').nodemap
            >>> nodemap.num_elements(3)
            8
        """
        return Elementmap(self.zone).num_elements(node)

    def element(self, node, offset):
        """The element containing a given node.

        Parameters:
            node (`int`): Zero-based index of a node.
            offset (`int`): Zero-based index of the element that uses
                the given node.

        Returns:
            `int` - Zero-based index of the element.

        Example usage::

            >>> nodemap = dataset.zone('My Zone').nodemap
            >>> print(nodemap.element(3, 7))
            324
        """
        return Elementmap(self.zone).element(node, offset)


@tecutil.lock_attributes
class NodemapSection(object):
    """A section of uniform cell-type in a `Nodemap`.

    A `MixedFEZone` contains a `Nodemap` that is made of one or more sections
    of uniform cell type (`NodemapSection`). Within these sections, the nodemap
    data is stored in an array consisting of the node indices.

    For more details, see the "working with datasets" examples shipped with
    PyTecplot in the Tecplot 360 distribution.
    """
    def __init__(self, nodemap, index):
        self.nodemap = nodemap
        self.index = tecutil.Index(index)

    def __eq__(self, other):
        return (self.nodemap == other.nodemap) and (self.index == other.index)

    @property
    def _metrics(self):
        return self.nodemap.zone.section_metrics(self.index)

    @property
    def cell_shape(self):
        """`FECellShape`: The geometric shape of elements in this
        `NodemapSection`.

        .. note:: This property is read-only

        Example usage::

            >>> zone = dataset.zone('My Zone')
            >>> nmap_section = zone.nodemap.section(0)
            >>> print(nmap_section.cell_shape)
            FECellShape.Tetrahedron
        """
        return self._metrics.cell_shape

    @property
    def grid_order(self):
        """`int`: The grid order of the cell type in this `NodemapSection`.

        .. note:: This property is read-only.

        A grid order of 1 is the classic case with linear cells where the nodes
        are exclusively on the corners of the elements. Note that the
        **high_order_array** and high-order node data is only available for
        grid orders 2 or greater.

        Example usage::

            >>> zone = dataset.zone('My Zone')
            >>> nmap_section = zone.nodemap.section(0)
            >>> print(nmap_section.grid_order)
            2
        """
        return self._metrics.grid_order

    @property
    def basis_func(self):
        """`FECellBasisFunction`: The basis function used to determine the node
        winding for elements in this `NodemapSection`.

        .. note:: This property is read-only.

        Currently, Tecplot only supports the Lagrangian basis function.

        Example usage::

            >>> zone = dataset.zone('My Zone')
            >>> nmap_section = zone.nodemap.section(0)
            >>> print(nmap_section.basis_func)
            FECellBasisFunction.Lagrangian
        """
        return self._metrics.basis_func

    @property
    def num_elements(self):
        """`int`: The total number of elements in this `NodemapSection`.

        .. note:: This property is read-only.

        Example usage::

            >>> zone = dataset.zone('My Zone')
            >>> nmap_section = zone.nodemap.section(0)
            >>> print(nmap_section.num_elements)
            1024
        """
        return self._metrics.num_elements

    @property
    def cell_type(self):
        """`FECellType`: The cell type of this `NodemapSection`.

        .. note:: This property is read-only.

        The cell type encapsulates the shape, grid order and basis function
        for the elemens in the section of the zone.

        Example usage::

            >>> zone = dataset.zone('My Zone')
            >>> cell_type = zone.nodemap.section(0).cell_type
            >>> print(cell_type.shape)
            FECellShape.Tetrahedron
            >>> print(cell_type.grid_order)
            2
        """
        return FECellType(self.cell_shape, self.grid_order, self.basis_func)

    @property
    def num_points_per_element(self):
        r"""`int`: Points per element for this `NodemapSection`.

        .. note:: This property is read-only.

        The number of points (also known as nodes) per finite-element is
        determined from the cell shape, grid order and the basis function used.

        This example shows the output for a high-order Tet-10 section::

            >>> zone = dataset.zone('My Zone')
            >>> nmap_section = zone.nodemap.section(0)
            >>> print(nmap_section.cell_shape)
            FECellShape.Tetrahedron
            >>> print(nmap_section.grid_order)
            2
            >>> print(nmap_section.num_points_per_element)
            10
        """
        return self.cell_type.num_nodes

    @property
    def shape(self):
        r"""`tuple` of `integers <int>`: Shape of the nodemap array.

        .. note:: This property is read-only.

        This is defined by the zone type and is equal to :math:`(N_e, N_{npe})`
        where :math:`N_e` is the number of elements and :math:`N_{npe}` is the
        number of nodes per element. Example usage::

            >>> print(dataset.zone(0).nodemap.section(0).shape)
            (1024, 4)
        """
        return (self.num_elements, self.num_points_per_element)

    @property
    def size(self):
        r"""`int`: Total number of nodes stored in the nodemap array.

        .. note:: This property is read-only.

        This is defined by the cell type and is equal to :math:`N_e \times
        N_{npe}` where :math:`N_e` is the number of elements and
        :math:`N_{npe}` is the number of nodes per element. Example usage::

            >>> print(dataset.zone(0).nodemap.section(0).shape)
            (1024, 4)
            >>> print(dataset.zone(0).nodemap.section(0).size)
            4096
        """
        return self.num_elements * self.num_points_per_element

    @property
    def array(self):
        r"""`list`-like array: Flattened array accessor for node data.

        A section of the nodemap is normally dimensioned by :math:`(N_e, N_{npe})`
        where :math:`N_e` is the number of elements and :math:`N_{npe}` is the number
        of nodes per element. This property represents a flattened view into the array
        containing the nodes of each element.

        Standard Python list slicing works for both fetching values and assignments.
        Example usage::

            >>> nmap_section = dataset.zone('My Zone').nodemap.section(0)
            >>> nmap_section.array[:] = mydata
            >>> print(nmap_section.array[:10])
            [1, 10, 8, 0, 5, 18, 6, 12, 18, 11]
        """
        return NodemapSectionArray(self)

    def nodes(self, element):
        """Returns node values for a specific element in this section.

        Parameters:
            element (`int`): The element index.

        Example usage::

            >>> zone = dataset.zone('My Zone')
            >>> print(zone.nodemap.section(0).nodes(1))
            (0, 1, 3, 4)
        """
        return list(self.array.nodes(element))

    def __len__(self):
        return self.num_elements

    def __getitem__(self, index):
        """Array accessor for elements within this `NodemapSection`.

        The data is dimensioned by :math:`(N_e, N_{npe})` where :math:`N_e` is
        the number of elements and :math:`N_{npe}` is the number of nodes per
        element.

        Parameters:
            index (`int` or `slice`): Element index.
        """
        import numpy as np
        if isinstance(index, slice):
            elems = tecutil.as_slice(index, len(self))
            npe = self.num_points_per_element
            result = self.array[npe * elems.start:npe * elems.stop]
            result = result.reshape((-1, npe))
            return result[::elems.step]
        else:
            return self.nodes(index)

    def __setitem__(self, index, value):
        import numpy as np
        elems = tecutil.as_slice(index, len(self))
        if (elems.start + len(value)) < elems.stop:
            elems = slice(elems.start, elems.start + len(value), elems.step)
        npe = self.num_points_per_element
        nodes = slice(npe * elems.start, npe * elems.stop)
        if elems.step == 1:
            self.array[nodes] = np.asarray(value).ravel()
        else:
            data = self.array[nodes].reshape((-1, npe))
            data[::elems.step] = value
            self.array[nodes] = data

    def __iter__(self):
        self._current_element = -1
        self._num_elements = self.num_elements
        return self

    def __next__(self):
        self._current_element += 1
        if self._current_element == len(self):
            del self._num_elements
            del self._current_element
            raise StopIteration
        return self.nodes(self._current_element)


class NodemapSectionArray(NodemapSection):
    def __init__(self, section):
        super().__init__(section.nodemap, section.index)

        nmap_c_type = self.nodemap.c_type
        self._get_array = {
            c_int32: _tecutil.DataNodeSectionArrayGetByRef,
            c_int64: _tecutil.DataNodeSectionArrayGetByRef64,
        }[nmap_c_type]
        self._set_array = {
            c_int32: _tecutil.DataNodeSectionArraySetByRef,
            c_int64: _tecutil.DataNodeSectionArraySetByRef64,
        }[nmap_c_type]

    def __len__(self):
        return self.num_elements * self.num_points_per_element

    @tecutil.lock()
    def __getitem__(self, i):
        s = tecutil.as_slice(i, len(self))
        size = s.stop - s.start
        arr = (self.nodemap.c_type * size)()
        self._get_array(self.nodemap, self.index + 1, s.start + 1, size, arr)
        try:
            import numpy as np
            arr = np.asarray(arr) - 1
        except ImportError:
            for i in range(len(arr)):
                arr[i] -= 1
        return arr[::s.step]

    @tecutil.lock()
    def __setitem__(self, i, nodes):
        s = tecutil.as_slice(i, len(self))
        if (s.start + len(nodes)) < s.stop:
            s = slice(s.start, s.start + len(nodes), s.step)
        if s.step != 1:
            for ii, nn in zip(range(s), nodes):
                self[ii] = nn
        else:
            size = s.stop - s.start
            data_ctype = self.nodemap.c_type
            try:
                import numpy as np
                nparr = np.asarray(nodes, dtype=data_ctype) + 1
                ptarr = nparr.ctypes.data_as(POINTER(data_ctype))
                ptaddr = addressof(ptarr.contents)
                arr = (data_ctype * size).from_address(ptaddr)
            except ImportError:
                msg = textwrap.dedent('''\
                    Falling back to using basic Python for data operations.
                    If installed, PyTecplot will make use of Numpy where
                    appropriate for significant perfomance gains.
                ''')
                log.warning(msg)
                arr = (data_ctype * size)(*[nd + 1 for nd in nodes])
            self._set_array(self.nodemap, self.index + 1, s.start + 1, size, arr)

    def nodes(self, element):
        npe = self.num_points_per_element
        offset = npe * element
        return self[offset:offset + npe]


class ClassicNodemap(NodemapBase):
    r"""Connectivity list definition and control for classic FE zones.

    A nodemap holds the connectivity between nodes and elements for classic
    finite-element zones. It is nominally a two-dimensionaly array of shape
    :math:`(N_e, N_{npe})` where :math:`N_e` is the number of elements and
    :math:`N_{npe}` is the number of nodes per element. The nodemap interface
    has flat-array access through the `ClassicNodemap.array` property as well as
    reverse look-up with `Nodemap.num_elements()` and `Nodemap.element()`.

    The nodemap behaves mostly like a two-dimensional array and can be treated
    as such::

        >>> nodemap = dataset.zone('My Zone').nodemap
        >>> print('nodes in the first element:', nodemap[0])
        nodes in the first element: [0, 1, 2, 3]
        >>> print(nodemap[:3])
        [[0, 1, 2, 3], [2, 3, 4, 5], [4, 5, 6, 7]]
        >>> nodemap[0] = [6, 7, 8, 9]
        >>> print(nodemap[0])
        [6, 7, 8, 9]

    Just for clarity, the nodemap indexing is by element first, then offset
    within that element::

        >>> element = 6
        >>> offset = 2
        >>> node = nodemap[element][offset]
        >>> print(node)
        21

    Setting node indices must be done for an entire element because getting
    values out of the nodemap and into Python always creates a copy. For
    example, **this will not work**::

        >>> nodemap = dataset.zone('My Zone').nodemap
        >>> # Trying to set the 3rd node of the element 10
        >>> nodemap[10][2] = 5  # Error: nodemap[10] returns a copy

    To modify a single node in a nodemap, it is neccessary to do a round trip
    like so::

        nodemap = dataset.zone('My Zone').nodemap
        >>> nodes = nodemap[10]
        >>> nodes[2] = 5
        >>> nodemap[10] = nodes  # OK: setting whole element at a time
        >>> print(nodemap[10])
        [20, 21, 5, 22]

    The following script creates a quad of two triangles from scratch using the
    PyTecplot low-level data creation interface. The general steps are:

    1. Setup the data
    2. Create the tecplot dataset and variables
    3. Create the zone
    4. Set the node locations and connectivity lists
    5. Set the (scalar) data
    6. Write out data file
    7. Adjust plot style and export image

    The data created looks like this:

    .. code-block:: none

        Node positions (x,y,z):

                       (1,1,1)
                      3
                     / \
                    /   \
         (0,1,.5)  2-----1  (1,0,.5)
                    \   /
                     \ /
                      0
                       (0,0,0)

    Breaking up the two triangular elements, the faces look like this. Notice the
    first element (index: 0) is on the bottom:

    .. code-block:: none

        Element 1 Faces:
                           *
           (nodes 3-2)  1 / \ 0  (nodes 1-3)
                         /   \
                        *-----*
                           2
                            (nodes 2-1)

        Element 0 Faces:
                            (nodes 1-2)
                           1
                        *-----*
                         \   /
           (nodes 2-0)  2 \ / 0  (nodes 0-1)
                           *

    The nodes are created as a list of :math:`(x, y, z)` positions::

        [(x0, y0, z0), (x1, y1, z1)...]

    which are transposed to lists of :math:`x`, :math:`y` and :math:`z`-positions::

        [(x0, x1, x2...), (y0, y1, y2...)...]

    and passed to the :math:`(x, y, z)` arrays. The nodemap, or connectivity
    list, is given as an array of dimensions :math:`(N, D)` where :math:`N` is
    the number of elements and :math:`D` is the number of nodes per element.
    The order of the node locations determines the indices used when specifying
    the connectivity list. The Nodemap can be set individually and separately
    or all at once as shown here:

    .. code-block:: python
        :emphasize-lines: 39

        import tecplot as tp
        from tecplot.constant import *

        # Triangle 0
        nodes0 = (
            (0, 0, 0  ),
            (1, 0, 0.5),
            (0, 1, 0.5))
        scalar_data0 = (0, 1, 2)
        conn0 = ((0, 1, 2),)
        neighbors0 = ((None, 0, None),)
        neighbor_zones0 = ((None, 1, None),)

        # Triangle 1
        nodes1 = (
            (1, 0, 0.5),
            (0, 1, 0.5),
            (1, 1, 1  ))
        scalar_data1 = (1, 2, 3)
        conn1 = ((0, 1, 2),)
        neighbors1 = ((0, None, None),)
        neighbor_zones1 = ((0, None, None),)

        # Create the dataset and zones
        ds = tp.active_frame().create_dataset('Data', ['x','y','z','s'])
        z0 = ds.add_fe_zone(ZoneType.FETriangle,
                            name='FE Triangle Float (3,1) Nodal 0',
                            num_points=len(nodes0), num_elements=len(conn0),
                            face_neighbor_mode=FaceNeighborMode.GlobalOneToOne)
        z1 = ds.add_fe_zone(ZoneType.FETriangle,
                            name='FE Triangle Float (3,1) Nodal 1',
                            num_points=len(nodes1), num_elements=len(conn1),
                            face_neighbor_mode=FaceNeighborMode.GlobalOneToOne)

        # Fill in and connect first triangle
        z0.values('x')[:] = [n[0] for n in nodes0]
        z0.values('y')[:] = [n[1] for n in nodes0]
        z0.values('z')[:] = [n[2] for n in nodes0]
        z0.nodemap[:] = conn0
        z0.values('s')[:] = scalar_data0

        # Fill in and connect second triangle
        z1.values('x')[:] = [n[0] for n in nodes1]
        z1.values('y')[:] = [n[1] for n in nodes1]
        z1.values('z')[:] = [n[2] for n in nodes1]
        z1.nodemap[:] = conn1
        z1.values('s')[:] = scalar_data1

        # Set face neighbors
        z0.face_neighbors.set_neighbors(neighbors0, neighbor_zones0, obscures=True)
        z1.face_neighbors.set_neighbors(neighbors1, neighbor_zones1, obscures=True)


        ### Setup a view of the data
        plot = tp.active_frame().plot(PlotType.Cartesian3D)
        plot.activate()

        plot.contour(0).colormap_name = 'Sequential - Yellow/Green/Blue'
        plot.contour(0).colormap_filter.distribution = ColorMapDistribution.Continuous

        for ax in plot.axes:
            ax.show = True

        plot.show_mesh = False
        plot.show_contour = True
        plot.show_edge = True
        plot.use_translucency = True

        # View parameters obtained interactively from Tecplot 360
        plot.view.distance = 10
        plot.view.width = 2
        plot.view.psi = 80
        plot.view.theta = 30
        plot.view.alpha = 0
        plot.view.position = (-4.2, -8.0, 2.3)

        fmaps = plot.fieldmaps()
        fmaps.surfaces.surfaces_to_plot = SurfacesToPlot.All
        fmaps.effects.surface_translucency = 40

        # Turning on mesh, we can see all the individual triangles
        plot.show_mesh = True
        fmaps.mesh.line_pattern = LinePattern.Dashed

        plot.contour(0).levels.reset_to_nice()
        tp.export.save_png('fe_triangles1.png', 600, supersample=3)

    ..  figure:: /_static/images/fe_triangles1.png
        :width: 300px
        :figwidth: 300px
    """
    @tecutil.lock()
    def _raw_pointer(self, writable=False):
        if _tecutil_connector.connected:
            msg = 'raw pointer access only available in batch-mode'
            raise TecplotLogicError(msg)
        _dispatch = {
            True: {
                c_int32: _tecutil.DataNodeGetWritableRawPtrByRef,
                c_int64: _tecutil.DataNodeGetWritableRawPtrByRef64},
            False: {
                c_int32: _tecutil.DataNodeGetReadableRawPtrByRef,
                c_int64: _tecutil.DataNodeGetReadableRawPtrByRef64}
            }
        return _dispatch[writable][self.c_type](self)

    def _raw_array(self, writable=False):
        ptr = self._raw_pointer(writable)
        return cast(ptr, POINTER(self.c_type * self.size)).contents

    @tecutil.lock()
    def alloc(self):
        """Allocates the internal space needed to store the Nodemap.

        This method is used in conjunction with deferred nodemap creation and
        is not needed with load-on-demand or normal zone creation methods.
        """
        with self.zone.dataset.frame.activated():
            if not _tecutil.DataNodeAlloc(self.zone.index + 1):
                raise TecplotSystemError()

    @property
    def array(self):
        r"""`list`-like array: Flattened array accessor for this nodemap.

        The nodemap is normally dimensioned by :math:`(N_e, N_{npe})` where
        :math:`N_e` is the number of elements and :math:`N_{npe}` is the number
        of nodes per element. This property represents a flattened view into
        the array which is of length :math:`N_e \times N_{npe}`. This may be
        more convenient than flattening the array in your script using a
        looping construct.

        Standard Python list slicing works for both fetching values and
        assignments. Example usage::

            >>> nmap = dataset.zone('My Zone').nodemap
            >>> nmap.array[:] = mydata
            >>> print(nmap.array[:10])
            [1, 10, 8, 0, 5, 18, 6, 12, 18, 11]
        """
        return ClassicNodemapArray(self.zone)

    @property
    def shape(self):
        r"""`tuple` of `integers <int>`: Shape of the nodemap array.

        .. note:: This property is read-only.

        This is defined by the zone type and is equal to :math:`(N_e, N_{npe})`
        where :math:`N_e` is the number of elements and :math:`N_{npe}` is the
        number of nodes per element. Example usage::

            >>> print(dataset.zone(0).nodemap.shape)
            (1024, 4)
        """
        return (self.zone.num_elements, self.num_points_per_element)

    @property
    def size(self):
        r"""`int`: Total number of nodes stored in the nodemap array.

        .. note:: This property is read-only.

        This is defined by the zone type and is equal to :math:`N_e \times
        N_{npe}` where :math:`N_e` is the number of elements and
        :math:`N_{npe}` is the number of nodes per element. Example usage::

            >>> print(dataset.zone(0).nodemap.shape)
            (1024, 4)
            >>> print(dataset.zone(0).nodemap.size)
            4096
        """
        return self.zone.num_elements * self.num_points_per_element

    def __len__(self):
        return self.zone.num_elements

    @property
    def num_points_per_element(self):
        r"""`int`: Points per element for classic finite-element zones.

        .. note:: This property is read-only.

        The number of points (also known as nodes) per finite-element is
        determined from the ``zone_type`` parameter. The following table shows
        the number of points per element for the available zone types along
        with the resulting shape of the nodemap based on the number of points
        specified (:math:`N`):

            ============== ============== ================
            Zone Type      Points/Element Nodemap Shape
            ============== ============== ================
            ``FELineSeg``  2              :math:`(N, 2 N)`
            ``FETriangle`` 3              :math:`(N, 3 N)`
            ``FEQuad``     4              :math:`(N, 4 N)`
            ``FETetra``    4              :math:`(N, 4 N)`
            ``FEBrick``    8              :math:`(N, 8 N)`
            ============== ============== ================

        Example usage::

            >>> zone = dataset.zone('My Zone')
            >>> print(zone.zone_type)
            ZoneType.FETriangle
            >>> print(zone.nodemap.num_points_per_element)
            3
        """
        return _tecutil.DataNodeGetNodesPerElem(self)

    def nodes(self, element):
        """Returns node values for a specific element.

        Parameters:
            element (`int`): The element index.

        Example usage::

            >>> zone = dataset.zone('My Zone')
            >>> print(zone.nodemap.nodes(1))
            (0, 1, 3, 4)
        """
        return self.section(0).nodes(element)

    def __getitem__(self, i):
        """Access the nodemap by elements.

        Parameters:
            i (`int` or `slice`): Element(s) to fetch from the nodemap.
        """
        ppe = self.num_points_per_element
        if isinstance(i, slice):
            s = tecutil.filled_slice(i, len(self))
            nelems = s.stop - s.start
            start = (s.start * ppe)
            stop = (s.stop * ppe)
            arr = self.array[start:stop]
            elems = list(range(nelems))[::s.step]
            return [arr[e * ppe:(e  + 1) * ppe] for e in elems]
        else:
            return self.array[i * ppe:(i + 1) * ppe]

    def __setitem__(self, i, nodes):
        """Modify the nodemap by elements.

        Parameters:
            i (`int` or `slice`): Element(s) to modify in the nodemap.
        """
        ppe = self.num_points_per_element
        if isinstance(i, slice):
            s = tecutil.filled_slice(i, len(self))
            if s.step == 1:
                a = s.start * ppe
                b = s.stop * ppe
                self.array[a:b] = list(it.chain.from_iterable(nodes))
            else:
                with self.assignment():
                    for i, n in zip(range(s.start, s.stop, s.step), nodes):
                        self[i] = n
        else:
            self.array[i * ppe:(i + 1) * ppe] = nodes

    def __iter__(self):
        self._current_index = -1
        self._current_length = len(self)
        return self

    def __next__(self):
        self._current_index = self._current_index + 1
        if self._current_index < self._current_length:
            return self.__getitem__(self._current_index)
        else:
            del self._current_index
            del self._current_length
            raise StopIteration


class ClassicNodemapArray(ClassicNodemap):
    def __len__(self):
        return self.size

    @property
    def shape(self):
        return (len(self),)

    @tecutil.lock()
    def __getitem__(self, i):
        """Access the underlying nodemap as 1D array."""
        if isinstance(i, slice):
            s = tecutil.filled_slice(i, len(self))
            n = s.stop - s.start
            arr = (self.c_type * n)()
            _tecutil.DataNodeArrayGetByRef(self, s.start + 1, n, arr)
            for i in range(len(arr)):
                arr[i] -= 1
            return arr[::s.step]
        else:
            elem, node = divmod(i, self.num_points_per_element)
            return _tecutil.DataNodeGetByRef(self, elem + 1, node + 1) - 1

    @tecutil.lock()
    def __setitem__(self, i, nodes):
        """Modify the underlying nodemap as 1D array."""
        _dispatch = {
            c_int32: _tecutil.DataNodeArraySetByRef,
            c_int64: _tecutil.DataNodeArraySetByRef64}
        data_ctype = self.c_type
        ref = self._native_reference(writable=True)
        with self.assignment():
            if isinstance(i, slice):
                s = tecutil.filled_slice(i, len(self))
                if s.step == 1:
                    n = s.stop - s.start
                    try:
                        import numpy as np
                        nparr = np.asarray(nodes, dtype=data_ctype) + 1
                        ptarr = nparr.ctypes.data_as(POINTER(data_ctype))
                        ptaddr = addressof(ptarr.contents)
                        arr = (data_ctype * n).from_address(ptaddr)
                    except ImportError:
                        msg = textwrap.dedent('''\
                            Falling back to using basic Python for data
                            operations. If installed, PyTecplot will make use
                            of Numpy where appropriate for significant
                            perfomance gains.
                        ''')
                        log.warning(msg)
                        arr = (data_ctype * n)(*[nd + 1 for nd in nodes])

                    if __debug__:
                        if min(arr) < 1 or self.zone.num_points < max(arr):
                            raise TecplotIndexError
                        log.debug(textwrap.dedent('''\
                            Nodemap Assignment:
                                offset: {}
                                array({}): {}''').format(
                                    s.start + 1, n, tecutil.array_to_str(arr)))
                    _dispatch[data_ctype](ref, s.start + 1, n, arr)
                else:
                    ppe = self.num_points_per_element
                    for i, n in zip(range(s.start, s.stop, s.step), nodes):
                        elem, node = divmod(i, ppe)
                        _tecutil.DataNodeSetByRef(ref, elem + 1, node + 1,
                                                  n + 1)
            else:
                ppe = self.num_points_per_element
                elem, node = divmod(i, ppe)
                _tecutil.DataNodeSetByRef(ref, elem + 1, node + 1, nodes + 1)
