.subckt five_transistor_ota vbias vss vdd von vin vip
mn0 tail vbias vss vss nmos_rvt w=10.5e-7 l=150e-9 nf=10 m=1
mn1 vbias vbias vss vss nmos_rvt w=10.5e-7 l=150e-9 nf=10 m=1
mn2 von vin tail vss nmos_rvt w=21e-7 l=150e-9 nf=10 m=1
mn3 vop vip tail vss nmos_rvt w=21e-7 l=150e-9 nf=10 m=1
mp4 von vop vdd vdd pmos_rvt w=21e-7 l=150e-9 nf=10 m=1
mp5 vop vop vdd vdd pmos_rvt w=21e-7 l=150e-9 nf=10 m=1
.ends five_transistor_ota
