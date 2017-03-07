#  -*- coding: utf-8 -*-
#  vim: tabstop=4 shiftwidth=4 softtabstop=4

#  Copyright (c) 2017, GEM Foundation

#  OpenQuake is free software: you can redistribute it and/or modify it
#  under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  OpenQuake is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.

#  You should have received a copy of the GNU Affero General Public License
#  along with OpenQuake.  If not, see <http://www.gnu.org/licenses/>.
import unittest
import numpy
from openquake.hazardlib.sourcewriter import obj_to_node
from openquake.hazardlib.mfd.multi_mfd import MultiMFD
from openquake.hazardlib.source.multi import MultiPointSource
from openquake.hazardlib.geo.mesh import Mesh
from openquake.hazardlib.scalerel.peer import PeerMSR
from openquake.hazardlib.tom import PoissonTOM
from openquake.hazardlib.geo import NodalPlane
from openquake.hazardlib.pmf import PMF


class MultiPointTestCase(unittest.TestCase):
    def test(self):
        all_args = [(4.5, 2.0, [.3, .1, .05]), (4.5, 2.0, [.4, .2, .1])]
        npd = PMF([(0.5, NodalPlane(1, 20, 3)),
                   (0.5, NodalPlane(2, 2, 4))])
        hd = PMF([(1, 4)])
        mesh = Mesh(numpy.array([0, 1]), numpy.array([0.5, 1]))
        tom = PoissonTOM(50.)
        mmfd = MultiMFD('incrementalMFD', 3, all_args)
        mps = MultiPointSource('mp1', 'multi point source',
                               'Active Shallow Crust',
                               mmfd, 2.0, PeerMSR(), 1.0,
                               tom, 10, 20, npd, hd, mesh)
        self.assertEqual(obj_to_node(mps).to_str(), '''\
multiPointSource{id='mp1', name='multi point source', tectonicRegion='Active Shallow Crust'}
  multiPointGeometry
    gml:posList ['0 0.5', '1 1.0']
    upperSeismoDepth 10
    lowerSeismoDepth 20
  magScaleRel 'PeerMSR'
  ruptAspectRatio 1.0
  multiMFD{kind='incrementalMFD'}
    min_mag array([ 4.5,  4.5], dtype=float32)
    bin_width array([ 2.,  2.], dtype=float32)
    occurRates{cols=3, rows=2} array([ 0.30000001,  0.1       ,  0.05      ,  0.40000001,  0.2       ,
        0.1       ], dtype=float32)
  nodalPlaneDist
    nodalPlane{dip=20, probability=0.5, rake=3, strike=1}
    nodalPlane{dip=2, probability=0.5, rake=4, strike=2}
  hypoDepthDist
    hypoDepth{depth=4, probability=1.0}
''')
