import math
from align.primitive.default.canvas import DefaultCanvas
from align.cell_fabric.generators import *
from align.cell_fabric.grid import *

import logging
logger = logging.getLogger(__name__)

class CapGenerator(DefaultCanvas):

    def __init__(self, pdk):
        super().__init__(pdk)

        # TODO: Generalize these !!!
        self.m1n = self.addGen( Wire( 'm1n', 'M1', 'v',
                                     clg=ColoredCenterLineGrid( colors=['c1','c2'], pitch=self.pdk['Cap']['m1Pitch'], width=self.pdk['Cap']['m1Width']),
                                     spg=EnclosureGrid( pitch=self.pdk['M2']['Pitch'], stoppoint=self.pdk['V1']['VencA_L'] +self.pdk['M2']['Width']//2, check=False)))
        self.m2n = self.addGen( Wire( 'm2n', 'M2', 'h',
                                      clg=ColoredCenterLineGrid( colors=['c1','c2'], pitch=self.pdk['Cap']['m2Pitch'], width=self.pdk['Cap']['m2Width']),
                                      spg=EnclosureGrid( pitch=self.pdk['M1']['Pitch'], stoppoint=self.pdk['V1']['VencA_H'] + self.pdk['M1']['Width']//2, check=False)))

        self.m3n = self.addGen( Wire( 'm3n', 'M3', 'v',
                                     clg=ColoredCenterLineGrid( colors=['c1','c2'], pitch=self.pdk['Cap']['m3Pitch'], width=self.pdk['Cap']['m3Width']),
                                     spg=EnclosureGrid(pitch=self.pdk['M2']['Pitch'], stoppoint=self.pdk['V2']['VencA_H'] + self.pdk['M2']['Width']//2, check=False)))
        
        m5_offset = self.pdk['MIMCap']['Enclosure'] + self.pdk['MIMCapC']['Enclosure'] + self.pdk['MIMCapC']['WidthX']//2
        self.m5n = self.addGen(Wire( 'm5n', 'M5', 'v',
                                     clg=ColoredCenterLineGrid( colors=[], pitch=2*self.pdk['Cap']['m5Width'], width=self.pdk['Cap']['m5Width'], offset=m5_offset),
                                     spg=EnclosureGrid(pitch=self.pdk['M4']['Pitch'], stoppoint=0, check=False)))

        self.Cboundary = self.addGen( Region( 'Cboundary', 'Cboundary', h_grid=self.m2.clg, v_grid=self.m1.clg))

        self.v_MIMCapC = self.addGen( Via( 'v_MIMCapC', 'MIMCapC',
                                        h_clg=self.m4.clg, v_clg=self.m5n.clg,
                                        WidthX=self.pdk['MIMCapC']['WidthX'], WidthY=self.pdk['MIMCapC']['WidthY'],
                                        h_ext=self.v4.h_ext, v_ext=self.v4.v_ext))

        self.v4_x = self.addGen( Via( 'v4_x', 'V4',
                                        h_clg=self.m4.clg, v_clg=self.m5n.clg,
                                        WidthX=self.v4.WidthX, WidthY=self.v4.WidthY,
                                        h_ext=self.v4.h_ext, v_ext=self.v4.v_ext))

    def addCap( self, unit_cap):

        x_length = float((math.sqrt(unit_cap/2))*1000)
        y_length = float((math.sqrt(unit_cap/2))*1000)  

        m1_p = self.pdk['M1']['Pitch']
        m2_p = self.pdk['M2']['Pitch']

        m4n_xwidth = x_length + 2*self.pdk['MIMCap']['Enclosure']
        m4n_ywidth = y_length + 2*self.pdk['MIMCap']['Enclosure']
        
        m4n = Wire( 'm4n', 'M4', 'v',
                                     clg=ColoredCenterLineGrid( colors=[], pitch=, width=m4n_width, offset=m4n_width//2),
                                     spg=EnclosureGrid(pitch=m4n_ywidth, stoppoint=self.pdk['MIMCap']['Enclosure'], check=False))
        #mimcap = Wire( 'mim', 'MIMCap', 'v',
        #                             clg=ColoredCenterLineGrid( colors=[], pitch=self.pdk['Cap']['m4Pitch'], width=x_length, offset=x_length//2),
        #                             spg=EnclosureGrid(pitch=y_length, stoppoint=0, check=False))

        '''def compute( l, p):
            return int( 2*round(  (l+p-w)/(2.0*p) ))'''

        x_number = ceil(m4n_xwidth/m1_p)
        y_number = ceil( m4n_ywidth/m2_p)

        logger.debug( f"Number of wires {x_number} {y_number}")

        self.addWire( self.m4n, 'Bottom', 0, (0, -1), (0, 1))

        '''grid_y0 = 0
        grid_y1 = grid_y0 + last_y1_track

        for i in range(x_number-1):
            grid_x = i
            net = 'PLUS' if i%2 == 1 else 'MINUS'
            self.addWire( self.m1n, net, grid_x, (grid_y0, -1), (grid_y1, 1))
            self.addWire( self.m3n, net, grid_x, (grid_y0, -1), (grid_y1, 1))

            grid_y = ((i+1)%2)*grid_y1

            self.addVia( self.v1_nx, net, grid_x, grid_y)
            self.addVia( self.v2_nx, net, grid_x, grid_y)

        pin = 'PLUS'
        # Don't port m1 per Yaguang instructions
        self.addWire( self.m1, 'PLUS', last_x1_track, (grid_y0, -1), (grid_y1, 1))
        # don't port m3 (or port one or the other)
        self.addWire( self.m3, 'PLUS', last_x1_track, (grid_y0, -1), (grid_y1, 1))

        grid_x0 = 0
        grid_x1 = grid_x0 + last_x1_track
        netType = 'drawing'
        for i in range(y_number-1):
            grid_x = ((i+1)%2)*grid_x1
            net = 'PLUS' if i%2 == 0 else 'MINUS'
            self.addVia( self.v1_xn, net, grid_x, i)
            self.addVia( self.v2_xn, net, grid_x, i)
            pin = 'PLUS' if i == 0 else None
            if i == 0:
                netType = 'pin'
            else:
                netType = 'drawing'
            self.addWire( self.m2n, net, i, (grid_x0, -1), (grid_x1, 1), netType = netType)

        pin = 'MINUS'
        self.addWire( self.m2, 'MINUS', last_y1_track, (grid_x0, -1), (grid_x1, 1), netType = 'pin')'''

        self.addRegion( self.boundary, 'Boundary', -2, -2,
                        x_number+2,
                        y_number+2)

        #self.addRegion( self.Cboundary, 'Cboundary', None,
        #                    -1, -1,
        #                    last_x_track  + x * grid_cell_x_pitch + 1 + p,
        #                    last_y1_track + y * grid_cell_y_pitch + 1)

        logger.debug( f"Computed Boundary: {self.terminals[-1]} {self.terminals[-1]['rect'][2]} {self.terminals[-1]['rect'][2]%80}")
