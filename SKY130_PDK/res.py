import logging
import math
from align.primitive.default.canvas import DefaultCanvas
from align.cell_fabric.generators import *
from align.cell_fabric.grid import *

logger = logging.getLogger(__name__)

class ResGenerator(DefaultCanvas):

    def __init__(self, pdk, fin=1, finDummy=0):
        super().__init__(pdk)
        self.finsPerUnitCell = fin + 2 * finDummy
        self.Rboundary = self.addGen(Region('Rboundary', 'Rboundary', h_grid=self.m2.clg, v_grid=self.m1.clg))
        self.poly = self.addGen(Region('poly', 'Poly', h_grid=self.m2.clg, v_grid=self.m1.clg))
        self.rpm = self.addGen(Region('rpm', 'Rpm', h_grid=self.m2.clg, v_grid=self.m1.clg))
        self.polyres = self.addGen(Region('polyres', 'Polyres', h_grid=self.m2.clg, v_grid=self.m1.clg))
        self.pselect = self.addGen(Region('pselect', 'Pselect', h_grid=self.m2.clg, v_grid=self.m1.clg))
        self.npc = self.addGen(Region('npc', 'Npc', h_grid=self.m2.clg, v_grid=self.m1.clg))
        self.v0 = self.addGen(Region('v0', 'V0', h_grid=self.m2.clg, v_grid=self.m1.clg))

    def addResArray(self, x_cells, y_cells, height, unit_res):
        for x in range(x_cells):
            for y in range(y_cells):
                self._addRes(x, y, height, unit_res, draw_boundary=(x == x_cells - 1) and (y == y_cells - 1))

    def _addRes(self, x, y, height, unit_res, draw_boundary=True):
        width_nm = 350
        r_sheet = 320.0
        res_val = float(unit_res) if (unit_res is not None and unit_res > 0) else 5000.0

        # Resistor body length in nm
        l_res = max(500, int(round((res_val / r_sheet) * width_nm)))
        l_res = int(round(l_res / 10.0) * 10)

        m1_p = self.pdk['M1']['Pitch']  # 460 nm
        m2_p = self.pdk['M2']['Pitch']  # 460 nm

        x_track_pitch = 4 * m1_p  # 1840 nm
        x_center = x * x_track_pitch + 2 * m1_p

        # Snap pad length to multiples of m2_p: >= 2.0 um to satisfy licon.1c
        pad_len = 5 * m2_p  # 2300 nm

        y_poly_start = 2 * m2_p  # 920 nm
        y_res_body_start = y_poly_start + pad_len
        y_res_body_end = y_res_body_start + l_res

        # Bottom M2 pin track
        y_bot_via = y_poly_start + 2 * m2_p  # 1840 nm (on grid)

        # Top M2 pin track
        y_top_track = int(math.ceil((y_res_body_end + m2_p) / float(m2_p)))
        y_top_via = y_top_track * m2_p  # on grid

        y_poly_end = max(y_res_body_end + pad_len, y_top_via + 2 * m2_p)

        # 1. Poly stripe (Layer 66/20)
        self.transform_and_add({
            'layer': 'Poly',
            'netName': None,
            'rect': [x_center - width_nm // 2, y_poly_start, x_center + width_nm // 2, y_poly_end],
            'netType': 'drawing'
        })

        # 2. RPM (Layer 86/20) covers all poly
        self.transform_and_add({
            'layer': 'Rpm',
            'netName': None,
            'rect': [x_center - 375, y_poly_start - 200, x_center + 375, y_poly_end + 200],
            'netType': 'drawing'
        })

        # 3. Polyres (Layer 66/13) marking the precision resistor body
        self.transform_and_add({
            'layer': 'Polyres',
            'netName': None,
            'rect': [x_center - width_nm // 2, y_res_body_start, x_center + width_nm // 2, y_res_body_end],
            'netType': 'drawing'
        })

        # 4. Pselect (94/20) and Npc (95/20)
        self.transform_and_add({
            'layer': 'Pselect',
            'netName': None,
            'rect': [x_center - 500, y_poly_start - 300, x_center + 500, y_poly_end + 300],
            'netType': 'drawing'
        })
        self.transform_and_add({
            'layer': 'Npc',
            'netName': None,
            'rect': [x_center - 375, y_poly_start - 200, x_center + 375, y_poly_end + 200],
            'netType': 'drawing'
        })

        # 5. Bottom contacts (MINUS terminal)
        y_bot_licon_start = y_poly_start + 40
        y_bot_licon_end = y_res_body_start - 40
        self.transform_and_add({
            'layer': 'V0',
            'netName': 'MINUS',
            'rect': [x_center - 95, y_bot_licon_start, x_center + 95, y_bot_licon_end],
            'netType': 'drawing'
        })
        self.transform_and_add({
            'layer': 'M1',
            'netName': 'MINUS',
            'rect': [x_center - 175, y_poly_start, x_center + 175, y_res_body_start],
            'netType': 'drawing'
        })
        self.transform_and_add({
            'layer': 'V1',
            'netName': 'MINUS',
            'rect': [x_center - 85, y_bot_via - 85, x_center + 85, y_bot_via + 85],
            'netType': 'drawing'
        })
        self.transform_and_add({
            'layer': 'M2',
            'netName': 'MINUS',
            'rect': [x_center - 230, y_bot_via - 130, x_center + 230, y_bot_via + 130],
            'netType': 'pin'
        })

        # 6. Top contacts (PLUS terminal)
        y_top_licon_start = y_res_body_end + 40
        y_top_licon_end = y_poly_end - 40
        self.transform_and_add({
            'layer': 'V0',
            'netName': 'PLUS',
            'rect': [x_center - 95, y_top_licon_start, x_center + 95, y_top_licon_end],
            'netType': 'drawing'
        })
        self.transform_and_add({
            'layer': 'M1',
            'netName': 'PLUS',
            'rect': [x_center - 175, y_res_body_end, x_center + 175, y_poly_end],
            'netType': 'drawing'
        })
        self.transform_and_add({
            'layer': 'V1',
            'netName': 'PLUS',
            'rect': [x_center - 85, y_top_via - 85, x_center + 85, y_top_via + 85],
            'netType': 'drawing'
        })
        self.transform_and_add({
            'layer': 'M2',
            'netName': 'PLUS',
            'rect': [x_center - 230, y_top_via - 130, x_center + 230, y_top_via + 130],
            'netType': 'pin'
        })

        # 7. Boundary
        if draw_boundary:
            total_width = (x + 1) * x_track_pitch
            total_height = int(math.ceil((y_poly_end + m2_p) / float(m2_p))) * m2_p
            self.transform_and_add({
                'layer': 'Boundary',
                'netName': 'Boundary',
                'rect': [0, 0, total_width, total_height],
                'netType': 'drawing'
            })
