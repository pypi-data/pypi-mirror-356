import ctypes
import itertools as it
import numpy as np
import os
import platform
import sys
import unittest

from collections import namedtuple
from contextlib import contextmanager
from ctypes import *
from os import path
from textwrap import dedent
from unittest.mock import patch, Mock, PropertyMock

import tecplot as tp
from tecplot.constant import *
from tecplot.exception import *
from tecplot import session

from test import patch_tecutil, skip_if_sdk_version_before


class TestNodemap(unittest.TestCase):
    @skip_if_sdk_version_before(2023, 1)
    def setUp(self):
        tp.new_layout()
        nodes = ((0, 0, 0), (2, 0, 0), (0, 2, 0), (0, 0, 2), (1, 0, 0),
                 (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (0, 1, 1),
                 (0, 0,-2), (0, 0,-1), (1, 0,-1), (0, 1,-1),)
        conn = np.array(((0, 1, 2,  3, 4, 5, 6,  7,  8,  9),
                         (0, 1, 2, 10, 4, 5, 6, 11, 12, 13)))
        scalar_data = (0, 4, 4, 4, 0, 1, 0, 0, 1, 1, 0, 0, -1, -1)
        sections = (
            # 2 elements of Tet-10s (grid order: 2)
            (2, FECellShape.Tetrahedron, 2),
        )
        ds = tp.active_frame().create_dataset('Data', ['x','y','z','s'])
        z = ds.add_fe_mixed_zone(name='FE Tetrahedron-10 Float (20, 2)',
                                 num_points=len(nodes),
                                 sections=sections)
        z.values('x')[:] = [n[0] for n in nodes]
        z.values('y')[:] = [n[1] for n in nodes]
        z.values('z')[:] = [n[2] for n in nodes]
        z.values('s')[:] = scalar_data

        nmapsec = z.nodemap.section(0)
        nmapsec.array[:] = conn.ravel()

        self.z = z
        self.nmap = self.z.nodemap

    def test_nodemap_instance(self):
        self.assertIsInstance(self.nmap, tp.data.Nodemap)

    def test_section(self):
        self.assertEqual(self.z.num_sections, 1)
        self.assertIsInstance(self.nmap.section(0), tp.data.NodemapSection)

    def test_eq(self):
        nm = self.nmap
        z2 = self.z.dataset.add_fe_zone(ZoneType.FETriangle, 'Z', 4, 2)
        self.assertTrue(nm == self.nmap)
        self.assertFalse(nm == z2.nodemap)
        self.assertFalse(nm != self.nmap)
        self.assertTrue(nm != z2.nodemap)

    def test_len(self):
        self.assertEqual(len(self.nmap), self.z.num_sections)

    def test_iter(self):
        self.assertEqual(len(self.nmap), self.z.num_sections)
        for i, section in enumerate(self.nmap):
            self.assertEqual(self.nmap.section(i), section)

    def test_getitem(self):
        self.assertIsInstance(self.nmap[0], tp.data.NodemapSection)

    def test_section_element(self):
        s, e = self.nmap.section_element(1)
        self.assertEqual(s, 0)
        self.assertEqual(e, 1)

        with patch('tecplot.data.MixedFEZone.num_sections',
                   PropertyMock(return_value=0)):
            self.assertIsNone(self.nmap.section_element(1))

    def test_nodes(self):
        e0 = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        e1 = (0, 1, 2, 10, 4, 5, 6, 11, 12, 13)
        self.assertAllClose(self.nmap.nodes(0), e0)
        self.assertAllClose(self.nmap.nodes(1), e1)
        self.assertAllClose(self.nmap.nodes(0, 0), e0)
        self.assertAllClose(self.nmap.nodes(1, 0), e1)


class TestNodemapSection(unittest.TestCase):
    @skip_if_sdk_version_before(2023, 1)
    def setUp(self):
        tp.new_layout()
        nodes = ((0, 0, 0), (2, 0, 0), (0, 2, 0), (0, 0, 2), (1, 0, 0),
                 (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (0, 1, 1),
                 (0, 0,-2), (0, 0,-1), (1, 0,-1), (0, 1,-1),)
        self.conn = np.array(((0, 1, 2,  3, 4, 5, 6,  7,  8,  9),
                              (0, 1, 2, 10, 4, 5, 6, 11, 12, 13)))
        scalar_data = (0, 4, 4, 4, 0, 1, 0, 0, 1, 1, 0, 0, -1, -1)
        sections = (
            # 2 elements of Tet-10s (grid order: 2)
            (2, FECellShape.Tetrahedron, 2),
        )
        ds = tp.active_frame().create_dataset('Data', ['x','y','z','s'])
        z = ds.add_fe_mixed_zone(name='FE Tetrahedron-10 Float (20, 2)',
                                 num_points=len(nodes),
                                 sections=sections)
        z.values('x')[:] = [n[0] for n in nodes]
        z.values('y')[:] = [n[1] for n in nodes]
        z.values('z')[:] = [n[2] for n in nodes]
        z.values('s')[:] = scalar_data

        nmapsec = z.nodemap.section(0)
        nmapsec[:] = self.conn

        self.z = z
        self.nmap = self.z.nodemap
        self.sec = self.nmap.section(0)

    def test_metrics(self):
        m = self.sec._metrics
        self.assertEqual(m.num_elements, 2)
        self.assertEqual(m.cell_shape, FECellShape.Tetrahedron)
        self.assertEqual(m.grid_order, 2)
        self.assertEqual(m.basis_func, FECellBasisFunction.Lagrangian)

    def test_cell_shape(self):
        self.assertEqual(self.sec.cell_shape, FECellShape.Tetrahedron)

    def test_grid_order(self):
        self.assertEqual(self.sec.grid_order, 2)

    def test_basis_func(self):
        self.assertEqual(self.sec.basis_func, FECellBasisFunction.Lagrangian)

    def test_num_elements(self):
        self.assertEqual(self.sec.num_elements, 2)

    def test_cell_type(self):
        cell_type = self.sec.cell_type
        self.assertEqual(cell_type.shape, FECellShape.Tetrahedron)
        self.assertEqual(cell_type.grid_order, 2)
        self.assertEqual(cell_type.basis_func, FECellBasisFunction.Lagrangian)

    def test_num_points_per_element(self):
        self.assertEqual(self.sec.num_points_per_element, 10)

    def shape(self):
        self.assertEqual(self.sec.shape, (2, 10))
        self.assertEqual(
            self.sec.shape,
            (self.sec.num_elements, self.sec.num_points_per_element))

    def size(self):
        self.assertEqual(self.sec.size, 2 * 10)
        self.assertEqual(
            self.sec.size,
            self.sec.num_elements * self.sec.num_points_per_element)

    def test_array(self):
        self.assertIsInstance(self.sec.array, tp.data.NodemapSectionArray)

    def test_nodes(self):
        self.assertAllClose(self.sec.nodes(0), self.conn[0])
        self.assertAllClose(self.sec.nodes(1), self.conn[1])

    def test_len(self):
        self.assertEqual(len(self.sec), self.sec.num_elements)
        self.assertEqual(len(self.sec), 2)

    def test_getitem(self):
        self.assertAllClose(self.sec[0], self.conn[0])
        self.assertAllClose(self.sec[1], self.conn[1])
        conn = self.sec[:]
        self.assertEqual(len(conn), 2)
        self.assertAllClose(conn[0], self.conn[0])
        self.assertAllClose(conn[1], self.conn[1])

    def test_setitem(self):
        conn = ((4, 3, 2,  1, 0, 5, 6,  7,  8,  9),
                (10, 2, 1, 0, 4, 5, 6, 11, 12, 13))
        self.sec[:1] = conn[:1]
        self.assertAllClose(self.sec[0], conn[0])
        self.assertAllClose(self.sec[1], self.conn[1])
        self.sec[1] = conn[1]
        self.assertAllClose(self.sec[0], conn[0])
        self.assertAllClose(self.sec[1], conn[1])
        self.sec[:] = self.conn
        self.assertAllClose(self.sec[0], self.conn[0])
        self.assertAllClose(self.sec[1], self.conn[1])

    def test_iter(self):
        for nodes, expected in zip(self.sec, self.conn):
            self.assertAllClose(nodes, expected)


class TestClassicNodemap(unittest.TestCase):
    def setUp(self):
        tp.new_layout()
        nodes = ((0, 0, 0), (1, 0, 0.5), (0, 1, 0.5), (1, 1, 1))
        self.conn = np.array(((0, 1, 2), (1, 3, 2)))
        ds = tp.active_frame().create_dataset('Data', ['x','y','z'])
        z = ds.add_fe_zone(ZoneType.FETriangle,
                           name='FE Triangle Float (4,2) Nodal',
                           num_points=len(nodes), num_elements=len(self.conn))

        z.values('x')[:] = [n[0] for n in nodes]
        z.values('y')[:] = [n[1] for n in nodes]
        z.values('z')[:] = [n[2] for n in nodes]

        self.z = z

    def test_nodemap_instance(self):
        self.assertIsInstance(self.z.nodemap, tp.data.ClassicNodemap)

    def test_access(self):
        self.z.nodemap[:] = self.conn
        self.assertEqual(self.z.nodemap[0], [0, 1, 2])
        self.assertEqual(self.z.nodemap[1], [1, 3, 2])
        self.assertEqual(self.z.nodemap[:], [[0, 1, 2], [1, 3, 2]])
        self.assertEqual(self.z.nodemap[::2], [[0, 1, 2]])

    def test_raw_array(self):
        if tp.tecutil._tecutil_connector.connected:
            with self.assertRaises(TecplotLogicError):
                _ = self.z.nodemap._raw_array(False)
            with self.assertRaises(TecplotLogicError):
                _ = self.z.nodemap._raw_array(True)
        else:
            self.z.nodemap[:] = self.conn
            ro = self.z.nodemap._raw_array(False)
            self.assertEqual(list(ro), [0, 1, 2, 1, 3, 2])
            rw = self.z.nodemap._raw_array(True)
            self.assertEqual(list(rw), [0, 1, 2, 1, 3, 2])

    def test_alloc(self):
        self.z.nodemap.alloc()

        with patch_tecutil('DataNodeAlloc', return_value=False):
            with self.assertRaises(TecplotSystemError):
                self.z.nodemap.alloc()

    def test_eq(self):
        nm = self.z.nodemap
        z2 = self.z.dataset.add_fe_zone(ZoneType.FETriangle, 'Z', 4, 2)
        self.assertTrue(nm == self.z.nodemap)
        self.assertFalse(nm == z2.nodemap)
        self.assertFalse(nm != self.z.nodemap)
        self.assertTrue(nm != z2.nodemap)

    def test_len(self):
        self.assertEqual(len(self.z.nodemap), self.z.num_elements)

    def test_iter(self):
        self.z.nodemap[:] = self.conn
        self.assertEqual(len(self.z.nodemap), len(self.conn))
        for i, nmap in enumerate(self.z.nodemap):
            self.assertEqual(list(nmap), list(self.conn[i]))

    def test_shape(self):
        self.z.nodemap[:] = self.conn
        self.assertEqual(self.z.nodemap.shape,
                         (len(self.conn), len(self.conn[0])))

    def test_setitem(self):
        for i, nodes in enumerate(self.conn):
            self.z.nodemap[i] = nodes
        for i, nmap in enumerate(self.z.nodemap):
            self.assertEqual(list(nmap), list(self.conn[i]))

    def test_setitem_partial(self):
        self.z.nodemap.array[:] = [0] * self.z.nodemap.size
        self.z.nodemap[:1] = self.conn[:1]
        self.z.nodemap[1:] = self.conn[1:]
        for i, nmap in enumerate(self.z.nodemap):
            self.assertEqual(list(nmap), list(self.conn[i]))

    def test_num_elements(self):
        self.z.nodemap[:] = self.conn
        self.assertEqual(self.z.nodemap.num_elements(0), 1)
        self.assertEqual(self.z.nodemap.num_elements(1), 2)

    def test_element(self):
        nmap = self.z.nodemap
        nmap[:] = self.conn
        self.assertEqual(nmap.element(0, 0), 0)
        self.assertEqual(nmap.element(1, 0), 0)
        self.assertEqual(nmap.element(1, 1), 1)
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            nmap.element(0, 1)
        with self.assertRaises((TecplotLogicError, TecplotSystemError)):
            nmap.element(4, 0)

    def test_array(self):
        nmap = self.z.nodemap
        nmap[:] = self.conn
        arr = nmap.array
        self.assertEqual(arr[0], self.conn[0][0])
        self.assertEqual(arr[3], self.conn[1][0])
        self.assertEqual(len(arr), nmap.size)

        if __debug__:
            with self.assertRaises(TecplotIndexError):
                arr[:1] = [-1]

        arr[0] = 3
        self.assertEqual(arr[0], 3)

        self.assertEqual(arr.shape, (len(arr),))

    def test_slicing(self):
        nmap = self.z.nodemap
        nmap[:] = self.conn
        arr = nmap.array
        nmap[::2] = [[2,1,0]]
        self.assertEqual(list(nmap[0]), [2, 1, 0])

        arr[:] = [0]*6
        self.assertEqual(list(arr), [0]*6)
        arr[::2] = [1]*3
        self.assertEqual(arr[::2], [1]*3)



if __name__ == '__main__':
    import test
    test.main()
