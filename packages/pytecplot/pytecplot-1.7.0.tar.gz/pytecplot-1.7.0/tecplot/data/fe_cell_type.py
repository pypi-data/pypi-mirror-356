from ..constant import FECellShape, FECellBasisFunction


class FECellType:
    def __init__(self, cell_shape, grid_order, basis_func):
        self._num_corners = None
        self._num_nodes = None
        self._num_high_order_nodes = None
        self.shape = cell_shape
        self.grid_order = grid_order
        self.basis_func = basis_func

    @property
    def shape(self):
        """`FECellShape`: Geometric shape of the cell."""
        return self._shape

    @shape.setter
    def shape(self, value):
        value = FECellShape(value)
        if value != getattr(self, '_shape', None):
            self._num_corners = None
            self._num_nodes = None
            self._num_high_order_nodes = None
            self._shape = value

    @property
    def grid_order(self):
        """`int`: Grid order of the nodes in the cell (order 1 is the linear case)."""
        return self._grid_order

    @grid_order.setter
    def grid_order(self, value):
        value = int(value)
        if value != getattr(self, '_grid_order', None):
            self._num_nodes = None
            self._num_high_order_nodes = None
            self._grid_order = value

    @property
    def basis_func(self):
        """`FECellBasisFunction`: The basis function used for this cell."""
        return self._basis_func

    @basis_func.setter
    def basis_func(self, value):
        value = FECellBasisFunction(value)
        if value != getattr(self, '_basis_func', None):
            self._num_nodes = None
            self._num_high_order_nodes = None
            self._basis_func = value

    @property
    def num_corners(self):
        """`int`: Number of nodes at the corners of the cell."""
        if self._num_corners is None:
            self._num_corners = {
                FECellShape.Bar: 2,
                FECellShape.Triangle: 3,
                FECellShape.Quadrilateral: 4,
                FECellShape.Tetrahedron: 4,
                FECellShape.Pyramid: 5,
                FECellShape.Prism: 6,
                FECellShape.Hexahedron: 8,
            }[self.shape]
        return self._num_corners

    @property
    def num_nodes(self):
        """`int`: Total number of nodes for the cell including corners and high-order nodes."""
        if self._num_nodes is None:
            assert (
                self.grid_order == 1 or
                self.basis_func == FECellBasisFunction.Lagrangian
            ), 'Non-Lagrangian basis functions are not yet supported.'
            self._num_nodes = {
                FECellShape.Bar:
                    self.grid_order + 1,
                FECellShape.Triangle:
                    (self.grid_order + 1) *
                    (self.grid_order + 2) // 2,
                FECellShape.Quadrilateral:
                    (self.grid_order + 1) *
                    (self.grid_order + 1),
                FECellShape.Tetrahedron:
                    (self.grid_order + 1) *
                    (self.grid_order + 2) *
                    (self.grid_order + 3) // 6,
                FECellShape.Pyramid:
                    (    self.grid_order + 1) *
                    (    self.grid_order + 2) *
                    (2 * self.grid_order + 3) // 6,
                FECellShape.Prism:
                    (self.grid_order + 1) *
                    (self.grid_order + 1) *
                    (self.grid_order + 2) // 2,
                FECellShape.Hexahedron:
                    (self.grid_order + 1) *
                    (self.grid_order + 1) *
                    (self.grid_order + 1),
            }[self.shape]
        return self._num_nodes

    @property
    def num_high_order_nodes(self):
        """`int`: Number of high-order nodes for the cell (not the corners)."""
        if self._num_high_order_nodes is None:
            self._num_high_order_nodes = self.num_nodes - self.num_corners
        return self._num_high_order_nodes
