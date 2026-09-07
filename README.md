# Jane Street 2026 ASIC Reverse Engineering puzzle #

## Overview

This is my attempt to solve the Jane Street 2026 ASIC Reverse Engineering puzzle.

The snarky answer to what it does is nothing: the layout is incomplete. There is a regular pattern for tap cells, but due to lack of fill cells, there are ranges of nwell that do not contact any taps.

The or4b_2 does not extract in-context. The nfets will be recognized as belonging to the cell but the pfets are flattened up and any node connected to them become treated as pins on the SuBCKT.

There is a moosehead in the bottom left corner that looks similar to the Jane Street logo, however there are 3 broken circles and no lambda.

The clock tree has four levels counting the clock pin. The clock pin only drives one buffer. That delayed clock fans out 16 clock buffers, which drive the flops. There is a further level of clock buffers, but they do not drive anything and their outputs are floating. 

There are layout-only via cells named VIA_viaX_Y_2000_1_480-* that do not connect layers X and Y but rather layers X-1 and y-1.     

## Reverse engineering flow

1. Use LVS to generated extracted netlist
2. Build "schematic" netlist by hand, matching subcircuit intantiations as I go. 
3. Convert SPICE with subcircuit instances to verilog with module instances
4. Simulate Verilog

     
## Extracting SPICE netlist by LVS

LVS extracts a netlist by converting layer overlaps into devices. The process can work hierarchically or flatten the layout.

I used KLayout as both my viewer and LVS engine.

Looking at the layout hierarchy in the warmup example, the subcells identified the process as sky130, so I installed the Efabless sky130 technology package for KLayout. It seems the puzzle.gds alread referenced that. The sky130 package included schematic netlists for the standard cells. Interestingly, several of the standard cells failed hierarchical LVS:

* a21boi_2: This cell has stacked nfets that in the layout are implemented as two stacks without the intermediate nodes on the shared diffusions shorted. This is a configuration that in general can be recognized by LVS engines, but I couldn't figure out how to get KLayout LVS to do this so I used by own netlist for the standard cell.
* conb_1: The schematic netlist for this cell is just two .connect cards. The extracted netlist used the | symbol to tie the upper level node togther. I had to turn off schemtic_simplify to get this to match
 * or2b_2: Only the nfets get extracted inside the .SUBCKT. The pfets are always extarcted flat in the top cell. Removed the >SUBCKT from teh schematic netlsit and forced the while thing to be extracted flat
* dfstp_2: Sometimes this wouldn't appear in the extracted netlist if it wasn't already in the schematic netlist.
* diode_2, tapvpwrvgnd_1, VIA_*: layout only cells with no contents extracted (just a .SUBCKT and and .ENDS). Remove .SUBCKT definition from schematic netlist and they'll get dropped rom the LVS comparisonf.

I disabled the 'purge' and 'purge_nets' flags to preserve everything in the extracted netlist.

If the `scale` option is not checked, the extracted device dimentions assume a unit of um, e.g a 0.1 micron is written as w=0.1. If checked, dimensions are multiplied by 1E6 in the extracted netlist: w=100000. However, when reading the schematic netlist, dimensions are assumed to be m, e.. a 0.1 micron width must be written w=0.1u. To use the extracted netlist to define the subcircuits, you must make one pass with `scale` not checked to produce the definitions and then run with it checked for actual comparison. 

## Building netlist by hand and verify by LVS

I went back and forth on using the subcell definitions from the extracted netlist or from the standard cell library. Copying over the extacted subcell netlists preserved the pin order aming it easy to grab the instances from the extracted netlist without translation. However, as noted above sometimes the extraction would not include the subcell if it wasn't in the schematic nelist. Mixing sources is a problem, since the standard cell definitions include the 'u' to scale dimensions to microns while the extacted netlist does not. If one source is used consistently then the 'scale' switch to the sky130 can be used to add the micron scaling or not, but if the sources are mixed then *something* will mismatch.

Working form the pins inward, I would identify connected instances in the extracted netlist and add them to the schematic netlist with comments about their function as I could derive it. I used an agentically generated script to translate auto-generated node numbers to more descriptive names.

## Convert SPICE netlist to Verilog
In theory the extracted netlsit could be used for teh conversion fromSPICE to Verilog. However, there are some subcells that cannot be extracted correctly and result in a flat set of transistors. By using a hand-writternreference netlist, the VLS engine itself can be used to flatten the reference netlist subcells while the cell names are used for maping to Verilog modules. 

## Simulate Verilog

## Reverse engineered Circuit description

The I pin drives the input of a 12 bit shift register. If Q[11:0] are the otput of the SR flops, only bits 0,9,10, and 11 are used by further logic. There are some paths to that logic from the I pin that do not poass through the shift register.

The success pin 


There is an 8-bit output bus from some additional logic block.


## Software used

### KLayout

#### Efabless sky130 technology plugin

### VS Code
#### LTspice for VSCode plugin
 