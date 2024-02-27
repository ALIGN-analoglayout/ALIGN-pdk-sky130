.subckt test3 net0 net1 net2 net3 net4
M1 net0 net2 netx netx nmos_lvt L=1000e-9 W=900e-9 nf=10
M2 net1 net3 nety nety nmos_lvt L=1000e-9 W=900e-9 nf=10
R1 netx net4 10k
R2 nety net4 10k
.ends test3