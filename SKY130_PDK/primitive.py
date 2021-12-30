from align.primitive import default
from align.cell_fabric.generators import * 
from align.cell_fabric.grid import *

# Override default MOSGenerator._addMOS & _addBodyContact 
# (to add fin & LISD layers)

class MOSGenerator(default.MOSGenerator):

    def __init__(self, pdk, height, fin, gate, gateDummy, shared_diff, stack, bodyswitch): 
        super().__init__(pdk, height, fin, gate, gateDummy, shared_diff, stack, bodyswitch)
        
        stoppoint = self.pdk['Active']['activePolyExTracks']*self.pdk['M2']['Pitch']
        self.pl = self.addGen( Wire( 'pl', 'Poly', 'v',
                                     clg=UncoloredCenterLineGrid( pitch= self.pdk['Poly']['Pitch'], width= self.pdk['Poly']['Width'], offset= self.pdk['Poly']['Offset']),
                                     spg=EnclosureGrid( pitch=self.unitCellHeight, offset=self.pdk['M2']['Offset'], stoppoint=stoppoint, check=True)))

        '''offset = self.gateDummy*self.pdk['Poly']['Pitch']+self.pdk['Poly']['Offset'] - self.pdk['Poly']['Pitch']//2
        stoppoint = self.gateDummy*self.pdk['Poly']['Pitch'] + self.pdk['Poly']['Offset']-self.pdk['Rvt']['poly_enclosure']
        self.RVT = self.addGen( Wire( 'RVT', 'Rvt', 'h',
                                      clg=UncoloredCenterLineGrid( pitch=self.activePitch, width=self.RVTWidth, offset=self.activeOffset),
                                      spg=EnclosureGrid( pitch=self.unitCellLength, offset=offset*self.shared_diff, stoppoint=stoppoint-offset*self.shared_diff, check=True)))

        stoppoint = self.gateDummy*self.pdk['Poly']['Pitch'] + self.pdk['Poly']['Offset']-self.pdk['Lvt']['poly_enclosure']
        self.LVT = self.addGen( Wire( 'LVT', 'Lvt', 'h',
                                      clg=UncoloredCenterLineGrid( pitch=self.activePitch, width=self.RVTWidth, offset=self.activeOffset),
                                      spg=EnclosureGrid( pitch=self.unitCellLength, offset=offset*self.shared_diff, stoppoint=stoppoint-offset*self.shared_diff, check=True)))

        stoppoint = self.gateDummy*self.pdk['Poly']['Pitch'] + self.pdk['Poly']['Offset']-self.pdk['Hvt']['poly_enclosure']
        self.HVT = self.addGen( Wire( 'HVT', 'Hvt', 'h',
                                      clg=UncoloredCenterLineGrid( pitch=self.activePitch, width=self.RVTWidth, offset=self.activeOffset),
                                      spg=EnclosureGrid( pitch=self.unitCellLength, offset=offset*self.shared_diff, stoppoint=stoppoint-offset*self.shared_diff, check=True)))'''
 
        self.Tap = self.addGen( Wire( 'Tap', 'Tap', 'v',
                                     clg=UncoloredCenterLineGrid( pitch=self.pdk['M1']['Pitch'], width= self.pdk['Tap']['Width'], offset= self.pdk['M1']['Offset']),
                                     spg=EnclosureGrid( pitch=self.pdk['M2']['Pitch'], offset=0, stoppoint= self.pdk['M2']['Width']//2+self.pdk['V1']['VencA_L'], check=True)))

        offset = self.gateDummy*self.pdk['Poly']['Pitch']+self.pdk['Poly']['Offset'] - self.pdk['Poly']['Pitch']//2
        stoppoint = self.gateDummy*self.pdk['Poly']['Pitch'] + self.pdk['Poly']['Offset']-self.pdk['Npc']['Ext']-self.pdk['Poly']['Width']//2
        self.Npc = self.addGen( Wire( 'Npc', 'Npc', 'h',
                                         clg=UncoloredCenterLineGrid( pitch=self.pdk['M2']['Pitch'], width=self.pdk['Npc']['Width'], offset=self.pdk['M2']['Pitch']),
                                         spg=EnclosureGrid( pitch=self.unitCellLength, offset=offset*self.shared_diff, stoppoint=stoppoint-offset*self.shared_diff, check=True)))

    def _addMOS( self, x, y, x_cells, vt_type, name='M1', reflect=False, **parameters):

        # Draw default layers
        super()._addMOS(x, y, x_cells, vt_type, name, reflect, **parameters)
        for i in range(self.gatesPerUnitCell):
            self.addWire( self.pl, None, None, self.gatesPerUnitCell*x+self.gateDummy*self.shared_diff+i,   (y,1), (y+1,-1))

        def _addRVT(x, y, x_cells):
            pass
    
        def _addLVT(x, y, x_cells):
            self.addWire( self.LVT,  None, None, y,          (x, 1), (x+1, -1))    

        def _addHVT(x, y, x_cells):
            self.addWire( self.HVT,  None, None, y,          (x, 1), (x+1, -1))  
     
        if vt_type == 'RVT':
            _addRVT(x, y, x_cells)
        elif vt_type == 'LVT':
            _addLVT(x, y, x_cells)
        elif vt_type == 'HVT':
            _addHVT(x, y, x_cells)
        else:
            print("This VT type not supported")
            exit()    


    def _addBodyContact(self, x, y, x_cells, yloc=None, name='M1'):
        super()._addBodyContact(x, y, x_cells, yloc, name)
        if yloc is not None:
            y = yloc
        h = self.m2PerUnitCell
        gu = self.gatesPerUnitCell
        gate_x = self.gateDummy*self.shared_diff + x*gu + gu // 2
        self.addWire( self.Tap, None, None, gate_x, ((y+1)*h+self.pdk['Active']['Body_nfin']//4-1, -1), ((y+1)*h+self.pdk['Active']['Body_nfin']//4+1, 1))
#
# Default Cap & Res generators are good enough
#

CapGenerator = default.CapGenerator
ResGenerator = default.ResGenerator
RingGenerator = default.RingGenerator
# Default Via Array generator is good enough
ViaArrayGenerator = default.ViaArrayGenerator

