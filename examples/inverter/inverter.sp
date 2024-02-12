.subckt inverter vss vdd in out
mn0 out in vss vss nmos_lvt w=14.5e-7 L=250e-9 nf=20 stack=3
mp0 out in vdd vdd pmos_lvt w=14.5e-7 L=250e-9 nf=20 stack=3
.ends inverter
