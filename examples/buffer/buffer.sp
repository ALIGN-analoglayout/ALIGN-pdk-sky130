.subckt buffer vss vdd in out
mn0 out1 in vss vss nmos_rvt w=10.5e-7 l=150e-9 nf=10 m=1
mn1 out out1 vss vss nmos_rvt w=10.5e-7 l=150e-9 nf=10 m=1
mp0 out1 in vdd vdd pmos_rvt w=21e-7 l=150e-9 nf=10 m=1
mp1 out out1 vdd vdd pmos_rvt w=21e-7 l=150e-9 nf=10 m=1
.ends buffer
