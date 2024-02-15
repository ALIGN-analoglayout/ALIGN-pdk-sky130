.subckt test net1 net2 gnd is

M1 net1 net1 gnd gnd nmos_lvt L=100e-9 W=700e-9 nf=20 stack=3
M2 net2 net1 gnd gnd nmos_lvt L=100e-9 W=700e-9 nf=20 stack=3
M3 is net2 gnd gnd nmos_lvt L=250e-9 W=1175e-9 nf=20 stack=3

.end test 