.subckt test2 net2 vdd1 vb gnd is vs vout vdd2
M1 net1 net1 gnd gnd nmos_lvt L=100e-9   W=700e-9   nf=20 stack=3
M2 net2 net1 gnd gnd nmos_lvt L=100e-9   W=700e-9   nf=20 stack=3
M3 is is vdd1 vdd1 pmos_lvt   L=250e-9   W=1174e-9  nf=20 stack=3
M4 net3 is vdd1 vdd1 pmos_lvt L=250e-9   W=1174e-9  nf=20 stack=3
M5 net4 net7 net3 net3 pmos_lvt L=660e-9 W=3300e-9  nf=20 stack=3
M6 net5 net8 net3 net3 pmos_lvt L=660e-9 W=3300e-9  nf=20 stack=3
M7 net4 net4 gnd gnd nmos_lvt L=350e-9   W=1238e-9 nf=20 stack=3
M8 net5 net4 gnd gnd nmos_lvt L=350e-9   W=1238e-9 nf=20 stack=3
M9 vout is vdd1 vdd1 pmos_lvt L=250e-9   W=2350e-9  nf=20 stack=3
M10 vout net5 gnd gnd nmos_lvt L=350e-9  W=4950e-9  nf=20 stack=3
R1 net5 vout 1.4k
R2 vs net7 17k
R3 vb vdd2 4k
R4 vs vdd2 4k
R5 net1 vdd2 8.5k
R6 net8 vb 17.14k
R7 net7 vout 50k
.end test2 