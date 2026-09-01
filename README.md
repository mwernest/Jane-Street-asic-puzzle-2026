

# Jane Street 2026 ASIC Reverse Engineering puzzle #

## Overview

This is my entry for the Jane Street 2026 ASIC Reverse Engineering puzzle.


## Reverse engineering flow flow

     1. Use LVS to generated extracted netlist
     2. Build "schematic" netlist by hand, matching subcircuit intantiations as I go. 
     3. Convert SPICE with subcircuit instances to verilog with module instances
     4. Simulate Verilog
     
     
## Extracting SPICE netlist by LVS
LVS extracts a netlist by converting layer overlaps into devices. The process can work hierarchically or flatten the layout.

I used KLayout as both my viewer and LVS engine.

Looking at the layout hierarchy, the subcells identified the process as sky130, so I installed the Efabless sky130 tecjnology package for KLayout. The sky130 package included schematic netlists for the standard cells. Interestingly, several of the standard cells failed hierarchical LVS when I tested against the warmup exercise:

    * sky130_fd_sc_hd__a21boi_2: This cell has stacked nfets that in the layout are implemented as two stacks without the intermediate nodes on the shared diffusions shorted. This is a configuration that can be recognized by LVS engines, but I couldn't figure out how to KLayout LVS to do this so I used by own netlist for the standard cell.
    * sky130_fd_sc_hd__tapvpwrvgnd_1: This looks like a layout-only cell that has no pins. No sure why it doesn't match, so I just dropped it from the master include file
    * sky130_fd_sc_hd__conb_1: The schematic netlist for this cell is just two .connect cards. The extracted netlist used the | symbol to tie the upper level node togther. I had to turn off schemtic_simplify to get this to match
    * or2b_2
    * dfstp_2: Sometimes this wouldn't appear in the extracted netlist if it wasn't already in teh schematic netlist.
    * diode_2

I disabled the 'purge' and 'purge_nets' flags to preserve everything in the extarcted netlist.

## Building netlist by hand

I went back and forth on using the subcell definitions from the extracted netlist or from the standard cell library. Copying over the extacted subcell netlists preserved the pin order aming it easy to grap the instances from teh extracted netlist without translation. However, as noted above sometimes the extraction would not include hte subcell if it wasn't in the schematic nelist. Mixing sources is a b=roblem, since the standard cell definitions include the 'u' to scale dimensions to microns while the extacted netlist does not. If one source is used consistently then the 'scale' switch to the sky130 can be used to add the micron scaling or not, but if the sources are mized then *something* will mismatch.

Working form the pins inward, I would identify connected instances in the extracted netlist and add them to the schematic netlist with comments about their function as I could derive it. I used an agentically generated script to translate auto-generated node numbers to more descriptive names. 

## Convert SPICE netlist to Verilog

## Simulate Verilog

## Reverse engineered Circuit description

The I pin drives the input of a 12 bit shift register.

The success pin 
There is an 8-bit output bus.

## Software used

### KLayout

#### Efabless sky130 technology plugin

### VS Code
#### LTspice for VSCode plugin
 