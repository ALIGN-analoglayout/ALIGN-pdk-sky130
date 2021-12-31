.subckt telescopic_ota vbiasn vbiasp1 vbiasp2 vinn vinp voutn voutp vdd 0
m1 id id 0 0 nmos_rvt w=840e-9 l=150e-9 nf=2
m2 net10 id 0 0 nmos_rvt w=840e-9 l=150e-9 nf=2
m5 voutn vbiasn net8 0 nmos_rvt w=840e-9 l=150e-9 nf=2
m6 voutp vbiasn net014 0 nmos_rvt w=840e-9 l=150e-9 nf=2
m8 voutp vbiasp1 net012 vdd pmos_rvt w=840e-9 l=150e-9 nf=2
m7 voutn vbiasp1 net06 vdd pmos_rvt w=840e-9 l=150e-9 nf=2
m10 net012 vbiasp2 vdd vdd pmos_rvt w=840e-9 l=150e-9 nf=2
m9 net06 vbiasp2 vdd vdd pmos_rvt w=840e-9 l=150e-9 nf=2
m4 net014 vinn net10 0 nmos_rvt w=840e-9 l=150e-9 nf=4
m3 net8 vinp net10 0 nmos_rvt w=840e-9 l=150e-9 nf=4
.ends ota
** End of subcircuit definition.
