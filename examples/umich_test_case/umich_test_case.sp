* dcdcInst: AUX CELL DCDC_COMP
*ALIGN (SPICE syntax): undefined devices such as comp or power sources is not supported
*.subckt DCDC_COMP VGND VNB VPB VPWR clk neg_in pos_in out
*.model comp SW(Ron=0.1 Roff=1e12 Vt=0 Vh=0)
*S1 vvdd out pos_in neg_in comp
*v1 vvdd 0 1.8
*.ends DCDC_COMP

* 2:1 stage: PMOS SWITCH
.subckt DCDC_XSW_PMOS VPB clk clkb vIN vOUT0 vOUT1
*ALIGN (SPICE syntax): *all nmos/pmos starts with M thus changed the prefix here
*ALIGN (SPICE syntax): does not support floating ports (VGND is not connected to anything in this subckt)
*AssertionError (sizing): Width of device should be multiple of fin pitch (210e-9)
*AssertionError: align modification width should <= 2100e-9 larger size should be designed using m
M0 int_sw0 int_sw1 vIN VPB sky130_fd_pr__pfet_01v8 w=420e-9 l=150e-9
M1 int_sw1 int_sw0 vIN VPB sky130_fd_pr__pfet_01v8 w=420e-9 l=150e-9
M2 vOUT0 int_sw0 vIN VPB sky130_fd_pr__pfet_01v8 w=420e-9 l=150e-9 m=10
M3 vOUT1 int_sw1 vIN VPB sky130_fd_pr__pfet_01v8 w=420e-9 l=150e-9 m=10
M4 clkb int_sw0 clkb clkb sky130_fd_pr__pfet_01v8 w=420e-9 l=2000e-9 m=10
M5 clk int_sw1 clk clk sky130_fd_pr__pfet_01v8 w=420e-9 l=2000e-9 m=10
.ends DCDC_XSW_PMOS


* 2:1 stage: NMOS SWITCH
.subckt DCDC_XSW_NMOS VNB clk clkb vIN vOUT0 vOUT1
M0 int_sw0 int_sw1 vIN VNB sky130_fd_pr__nfet_01v8 w=420e-9 l=150e-9
M1 int_sw1 int_sw0 vIN VNB sky130_fd_pr__nfet_01v8 w=420e-9 l=150e-9
M2 vOUT0 int_sw0 vIN VNB sky130_fd_pr__nfet_01v8 w=420e-9 l=150e-9 m=2
M3 vOUT1 int_sw1 vIN VNB sky130_fd_pr__nfet_01v8 w=420e-9 l=150e-9 m=2
M4 clkb int_sw0 clkb clkb sky130_fd_pr__pfet_01v8 w=420e-9 l=200e-9 m=10
M5 clk int_sw1 clk clk sky130_fd_pr__pfet_01v8 w=420e-9 l=200e-9 m=10
.ends DCDC_XSW_NMOS


* 2:1 stage: unit cap
.subckt DCDC_CAP_UNIT bot top
*AssertionError: caps larger that 1000fF are not supported
c0 top bot 500f
.ends DCDC_CAP_UNIT


* power mux: DCDC_MUX_TGATE
.subckt DCDC_MUX_TGATE VGND VPWR SEL SEL_INV VIN VOUT
M1  VOUT SEL_INV VIN VPWR sky130_fd_pr__pfet_01v8 w=630e-9 l=150e-9 m=80
M2  VOUT SEL     VIN VGND sky130_fd_pr__nfet_01v8 w=630e-9 l=150e-9 m=80
.ends DCDC_MUX_TGATE

*align modification: a top level subcircuit need to be defined for which layout needs to be generated
.subckt umich_test_case VGND VNB VPB VPWR
x0 VPB clk clkb vIN vOUT0 vOUT1 DCDC_XSW_PMOS
x1 VNB clk clkb vIN vOUT0 vOUT1 DCDC_XSW_NMOS
x2 bot top DCDC_CAP_UNIT
x3 VGND VPWR SEL SEL_INV VIN VOUT DCDC_MUX_TGATE
.ends umich_test_case
