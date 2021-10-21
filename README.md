# StageController

# Overview
(ENGLISH)  
Control BD6321F-E2 and DC motor via Serial communication using Rasberry Pi pico.
<br>
<br>
(JAPANESE)  
Rasberry Pi picoを使って、シリアル通信でBD6231F-E2を制御する  


# How to use
1. Assemble the board by referring to schematic(circuit\Circuit.pdf) and BOM(BOM\BOM.xlsx).
2. Printing a body(STL\base.stl and table.stl) with a 3D printer
3. Assemble the stage with reference to the photos() and BOM(BOM\BOM.xlsx).
4. Upload main.py to your Rasberry Pi pico.
5. Control the stage by typing command.


# Command
## Command structure
` XXX [YYY] [ZZZ]`   
XXX is command ID  
YYY is parameter1  
ZZZ is parameter2  
Use a space between XXX, YYY and ZZZ.

## Command example
` CCW 60 5`  
Rotate 60 degrees CCW direction at 5PRM

## Command list
| command ID | parameter1 | parameter2 |description |
| :--- | :--- | :--- |:--- |
| CW | degree | RPM | Rotate CW |
| CCW | degree | RPM |Rotate CCW |
| LON | - | - | Rasberry Pi pico LED ON(for debug) |
| LOFF | - | - | Rasberry Pi pico LED OFF(for debug) |