EESchema Schematic File Version 4
EELAYER 26 0
EELAYER END
$Descr USLedger 17000 11000
encoding utf-8
Sheet 1 1
Title "Scorzonera"
Date "2019-05-05"
Rev ""
Comp "Copyright 2015 Great Scott Gadgets, 2019 Mike Walters"
Comment1 "License: BSD-3-Clause"
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text Label 9350 3500 0    40   ~ 0
P2_8
$Comp
L Connector_Generic:Conn_02x20_Odd_Even J2
U 1 1 55EAB4B7
P 9750 3800
F 0 "J2" H 9750 4850 50  0000 C CNN
F 1 "NEIGHBOR2" V 9750 3800 50  0000 C CNN
F 2 "gsg-modules:HEADER-2x20" H 9750 2850 60  0001 C CNN
F 3 "" H 9750 2850 60  0000 C CNN
F 4 "Samtec" H 9750 3800 60  0001 C CNN "Manufacturer"
F 5 "SSQ-120-23-G-D" H 9750 3800 60  0001 C CNN "Part Number"
F 6 "CONN RCPT .100\" 40POS DUAL-ROW STACKING GOLD" H 9750 3800 60  0001 C CNN "Description"
F 7 "Alternate: https://www.adafruit.com/products/2223" H 9750 3800 60  0001 C CNN "Note"
	1    9750 3800
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR059
U 1 1 55EACE84
P 9350 2900
F 0 "#PWR059" H 9350 2650 50  0001 C CNN
F 1 "GND" H 9350 2750 50  0000 C CNN
F 2 "" H 9350 2900 60  0000 C CNN
F 3 "" H 9350 2900 60  0000 C CNN
	1    9350 2900
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR060
U 1 1 55EAECD0
P 9350 5250
F 0 "#PWR060" H 9350 5000 50  0001 C CNN
F 1 "GND" H 9350 5100 50  0000 C CNN
F 2 "" H 9350 5250 60  0000 C CNN
F 3 "" H 9350 5250 60  0000 C CNN
	1    9350 5250
	0    1    1    0   
$EndComp
$Comp
L power:VCC #PWR061
U 1 1 55EAF03E
P 10250 5250
F 0 "#PWR061" H 10250 5100 50  0001 C CNN
F 1 "VCC" H 10250 5400 50  0000 C CNN
F 2 "" H 10250 5250 60  0000 C CNN
F 3 "" H 10250 5250 60  0000 C CNN
	1    10250 5250
	0    1    1    0   
$EndComp
$Comp
L Connector_Generic:Conn_02x20_Odd_Even J1
U 1 1 55FB1D52
P 9750 6150
F 0 "J1" H 9750 7200 50  0000 C CNN
F 1 "NEIGHBOR1" V 9750 6150 50  0000 C CNN
F 2 "gsg-modules:HEADER-2x20" H 9750 5200 60  0001 C CNN
F 3 "" H 9750 5200 60  0000 C CNN
F 4 "Samtec" H 9750 6150 60  0001 C CNN "Manufacturer"
F 5 "SSQ-120-23-G-D" H 9750 6150 60  0001 C CNN "Part Number"
F 6 "CONN RCPT .100\" 40POS DUAL-ROW STACKING GOLD" H 9750 6150 60  0001 C CNN "Description"
F 7 "Alternate: https://www.adafruit.com/products/2223" H 9750 6150 60  0001 C CNN "Note"
	1    9750 6150
	1    0    0    -1  
$EndComp
Text Label 10250 5350 2    40   ~ 0
SGPIO0
Text Label 9350 5350 0    40   ~ 0
SGPIO14
Text Label 10250 5450 2    40   ~ 0
SGPIO1
Text Label 9350 5450 0    40   ~ 0
SGPIO15
Text Label 10250 5550 2    40   ~ 0
P5_0
Text Label 9350 5550 0    40   ~ 0
P1_0
Text Label 9350 5650 0    40   ~ 0
P5_1
Text Label 10250 5650 2    40   ~ 0
P1_1
Text Label 10250 5750 2    40   ~ 0
P1_2
Text Label 10250 7150 2    40   ~ 0
P1_3
Text Label 10250 5850 2    40   ~ 0
P5_2
Text Label 9350 7150 0    40   ~ 0
P1_4
Text Label 9350 5850 0    40   ~ 0
P1_5
Text Label 10250 5950 2    40   ~ 0
P1_6
Text Label 9350 5950 0    40   ~ 0
P1_7
Text Label 10250 6050 2    40   ~ 0
P1_8
Text Label 9350 6050 0    40   ~ 0
P1_9
Text Label 10250 6150 2    40   ~ 0
P1_10
Text Label 9350 6150 0    40   ~ 0
P5_3
Text Label 10250 6250 2    40   ~ 0
P1_11
Text Label 9350 6250 0    40   ~ 0
P1_12
Text Label 10250 6350 2    40   ~ 0
P5_4
Text Label 9350 6350 0    40   ~ 0
P5_5
Text Label 10250 6450 2    40   ~ 0
P1_13
Text Label 9350 6450 0    40   ~ 0
P1_14
Text Label 10250 6550 2    40   ~ 0
SGPIO2
Text Label 9350 6550 0    40   ~ 0
P5_6
Text Label 10250 6650 2    40   ~ 0
SGPIO3
Text Label 9350 6650 0    40   ~ 0
P5_7
Text Label 10250 6750 2    40   ~ 0
P1_17
Text Label 9350 6750 0    40   ~ 0
P1_18
Text Label 10250 7050 2    40   ~ 0
P1_19
Text Label 9350 6850 0    40   ~ 0
P9_5
Text Label 9350 7050 0    40   ~ 0
P1_20
Text Label 10250 6850 2    40   ~ 0
P9_6
Text Label 9350 5750 0    40   ~ 0
CLK0
Text Label 10250 6950 2    40   ~ 0
P6_0
Text Label 9350 6950 0    40   ~ 0
P2_0
Text Notes 10300 7150 0    40   ~ 0
MISO
Text Notes 9300 7150 2    40   ~ 0
MOSI
Text Notes 10300 7050 0    40   ~ 0
SCK
Text Notes 9300 7050 2    40   ~ 0
SSEL
Text Label 10350 4800 2    40   ~ 0
I2C0_SCL
Text Label 9250 4800 0    40   ~ 0
I2C0_SDA
Text Label 10250 4600 2    40   ~ 0
P6_3
Text Label 9350 4600 0    40   ~ 0
P2_1
Text Label 10250 4500 2    40   ~ 0
SGPIO5
Text Label 9350 4500 0    40   ~ 0
P2_2
Text Label 9350 4400 0    40   ~ 0
SGPIO6
Text Label 9350 4300 0    40   ~ 0
SGPIO7
Text Label 10250 3800 2    40   ~ 0
P2_3
Text Label 9350 3800 0    40   ~ 0
P2_4
Text Label 10250 3700 2    40   ~ 0
P2_5
Text Label 9350 3600 0    40   ~ 0
P2_6
Text Label 10250 3400 2    40   ~ 0
CLK2
Text Label 9350 4200 0    40   ~ 0
SGPIO4
Text Label 10250 4100 2    40   ~ 0
P3_0
Text Label 9350 4100 0    40   ~ 0
P7_1
Text Label 10250 4000 2    40   ~ 0
P3_1
Text Label 9350 4000 0    40   ~ 0
P7_2
Text Label 10250 3900 2    40   ~ 0
P3_2
Text Label 10250 4400 2    40   ~ 0
P3_3
Text Label 10250 4200 2    40   ~ 0
P3_4
Text Label 9350 3900 0    40   ~ 0
PF_4
Text Label 9350 4700 0    40   ~ 0
P3_5
Text Label 10250 4700 2    40   ~ 0
P3_6
Text Label 10250 4300 2    40   ~ 0
P3_7
Text Label 10250 3600 2    40   ~ 0
P7_7
Text Label 10250 3000 2    40   ~ 0
P4_0
Text Label 9300 3100 0    40   ~ 0
ADC0_0
Text Label 9350 3300 0    40   ~ 0
SGPIO9
Text Label 10250 3200 2    40   ~ 0
SGPIO8
Text Label 9350 3200 0    40   ~ 0
SGPIO10
Text Label 10250 3100 2    40   ~ 0
SGPIO11
Text Label 10250 3300 2    40   ~ 0
SGPIO12
Text Label 9350 3400 0    40   ~ 0
P4_7
Text Label 9350 3000 0    40   ~ 0
SGPIO13
Text Label 9250 3700 0    40   ~ 0
WAKEUP0
Text Label 10250 3500 2    40   ~ 0
P2_7
Text Notes 10400 3500 2    40   ~ 0
ISP
Text Notes 9200 3500 0    40   ~ 0
DFU
Text Notes 10300 5650 0    40   ~ 0
BOOT
Text Notes 10450 5750 2    40   ~ 0
BOOT
Text Label 15950 7550 1    40   ~ 0
P6_1
Text Label 15850 7550 1    40   ~ 0
P6_2
Text Label 14350 7550 1    40   ~ 0
P6_4
Text Label 14450 7550 1    40   ~ 0
P6_5
Text Label 15750 7550 1    40   ~ 0
P6_9
Text Label 15650 7550 1    40   ~ 0
P6_10
Text Label 14750 7550 1    40   ~ 0
P2_9
Text Label 15550 7550 1    40   ~ 0
P2_10
Text Label 15450 7550 1    40   ~ 0
P2_11
Text Label 14850 7550 1    40   ~ 0
P2_12
Text Label 14950 7550 1    40   ~ 0
P2_13
$Comp
L power:GND #PWR075
U 1 1 560E00A9
P 14250 7550
F 0 "#PWR075" H 14250 7300 50  0001 C CNN
F 1 "GND" H 14250 7400 50  0000 C CNN
F 2 "" H 14250 7550 60  0000 C CNN
F 3 "" H 14250 7550 60  0000 C CNN
	1    14250 7550
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR076
U 1 1 560E046D
P 16150 7400
F 0 "#PWR076" H 16150 7250 50  0001 C CNN
F 1 "VCC" H 16150 7550 50  0000 C CNN
F 2 "" H 16150 7400 60  0000 C CNN
F 3 "" H 16150 7400 60  0000 C CNN
	1    16150 7400
	-1   0    0    1   
$EndComp
Text Notes 14750 7750 1    40   ~ 0
BOOT
Wire Wire Line
	9350 5250 9550 5250
Wire Wire Line
	10050 5250 10250 5250
Wire Wire Line
	10250 5350 10050 5350
Wire Wire Line
	9350 5350 9550 5350
Wire Wire Line
	9350 2900 9450 2900
Wire Wire Line
	9350 5450 9550 5450
Wire Wire Line
	9350 5550 9550 5550
Wire Wire Line
	9350 5650 9550 5650
Wire Wire Line
	9350 5750 9550 5750
Wire Wire Line
	9350 5850 9550 5850
Wire Wire Line
	9350 5950 9550 5950
Wire Wire Line
	9350 6050 9550 6050
Wire Wire Line
	9350 6150 9550 6150
Wire Wire Line
	9350 6250 9550 6250
Wire Wire Line
	9350 6350 9550 6350
Wire Wire Line
	9350 6450 9550 6450
Wire Wire Line
	9350 6550 9550 6550
Wire Wire Line
	9350 6650 9550 6650
Wire Wire Line
	9350 6750 9550 6750
Wire Wire Line
	9350 6850 9550 6850
Wire Wire Line
	9350 6950 9550 6950
Wire Wire Line
	10250 6950 10050 6950
Wire Wire Line
	10050 6850 10250 6850
Wire Wire Line
	10250 6750 10050 6750
Wire Wire Line
	10050 6650 10250 6650
Wire Wire Line
	10250 6550 10050 6550
Wire Wire Line
	10050 6450 10250 6450
Wire Wire Line
	10250 6350 10050 6350
Wire Wire Line
	10050 6250 10250 6250
Wire Wire Line
	10250 6150 10050 6150
Wire Wire Line
	10050 6050 10250 6050
Wire Wire Line
	10250 5950 10050 5950
Wire Wire Line
	10050 5850 10250 5850
Wire Wire Line
	10250 5750 10050 5750
Wire Wire Line
	10050 5650 10250 5650
Wire Wire Line
	10250 5550 10050 5550
Wire Wire Line
	10050 5450 10250 5450
Wire Wire Line
	9350 7050 9550 7050
Wire Wire Line
	9550 7150 9350 7150
Wire Wire Line
	10050 7150 10250 7150
Wire Wire Line
	10250 7050 10050 7050
Wire Wire Line
	9350 4700 9550 4700
Wire Wire Line
	10050 4700 10250 4700
Wire Wire Line
	10250 4600 10050 4600
Wire Wire Line
	9550 4600 9350 4600
Wire Wire Line
	9350 4500 9550 4500
Wire Wire Line
	10250 4500 10050 4500
Wire Wire Line
	10250 4400 10050 4400
Wire Wire Line
	10250 4300 10050 4300
Wire Wire Line
	9550 4400 9350 4400
Wire Wire Line
	9350 4300 9550 4300
Wire Wire Line
	9550 4200 9350 4200
Wire Wire Line
	10250 4100 10050 4100
Wire Wire Line
	10350 4800 10050 4800
Wire Wire Line
	9550 4800 9250 4800
Wire Wire Line
	10250 4200 10050 4200
Wire Wire Line
	9350 4100 9550 4100
Wire Wire Line
	9350 4000 9550 4000
Wire Wire Line
	10250 4000 10050 4000
Wire Wire Line
	10250 3900 10050 3900
Wire Wire Line
	9350 3900 9550 3900
Wire Wire Line
	10250 3800 10050 3800
Wire Wire Line
	9550 3800 9350 3800
Wire Wire Line
	10250 3700 10050 3700
Wire Wire Line
	9550 3700 9250 3700
Wire Wire Line
	9350 3600 9550 3600
Wire Wire Line
	10250 3600 10050 3600
Wire Wire Line
	10250 3500 10050 3500
Wire Wire Line
	9350 3500 9550 3500
Wire Wire Line
	10250 3400 10050 3400
Wire Wire Line
	9350 3400 9550 3400
Wire Wire Line
	10250 3300 10050 3300
Wire Wire Line
	9350 3300 9550 3300
Wire Wire Line
	10250 3200 10050 3200
Wire Wire Line
	9550 3200 9350 3200
Wire Wire Line
	9300 3100 9550 3100
Wire Wire Line
	10250 3100 10050 3100
Wire Wire Line
	9350 3000 9550 3000
Wire Wire Line
	10050 3000 10250 3000
Wire Wire Line
	15950 7550 15950 7200
Wire Wire Line
	15850 7550 15850 7200
Wire Wire Line
	15750 7550 15750 7200
Wire Wire Line
	15650 7550 15650 7200
Wire Wire Line
	15550 7550 15550 7200
Wire Wire Line
	15450 7550 15450 7200
Wire Wire Line
	15350 7550 15350 7200
Wire Wire Line
	15250 7550 15250 7200
Wire Wire Line
	15050 7550 15050 7200
Wire Wire Line
	14950 7550 14950 7200
Wire Wire Line
	14850 7550 14850 7200
Wire Wire Line
	14250 7550 14250 7200
Wire Wire Line
	16150 7400 16150 7200
$Comp
L Connector_Generic:Conn_01x20 J7
U 1 1 560E713A
P 15150 7000
F 0 "J7" H 15150 8050 50  0000 C CNN
F 1 "BONUS_ROW" V 15250 7000 50  0000 C CNN
F 2 "gsg-modules:HEADER-1x20" H 15150 7000 60  0001 C CNN
F 3 "" H 15150 7000 60  0000 C CNN
F 4 "Samtec" H 15150 7000 60  0001 C CNN "Manufacturer"
F 5 "SSQ-120-23-G-S" H 15150 7000 60  0001 C CNN "Part Number"
F 6 "CONN RCPT .100\" 20POS SINGLE-ROW STACKING GOLD" H 15150 7000 60  0001 C CNN "Description"
F 7 "DNP" V 15350 7000 60  0000 C CNN "Note"
	1    15150 7000
	0    -1   -1   0   
$EndComp
Wire Wire Line
	14750 7550 14750 7200
Wire Wire Line
	14650 7550 14650 7200
Wire Wire Line
	14550 7550 14550 7200
Wire Wire Line
	14450 7550 14450 7200
Wire Wire Line
	14350 7550 14350 7200
Text Label 14650 7550 1    40   ~ 0
ADC0_2
Text Label 14550 7550 1    40   ~ 0
ADC0_5
$Comp
L Connector_Generic:Conn_01x01 MH3
U 1 1 5600EED5
P 13650 850
F 0 "MH3" H 13600 950 50  0000 C CNN
F 1 "MOUNTING_HOLE" V 13750 850 50  0000 C CNN
F 2 "gsg-modules:HOLE126MIL-COPPER" H 13650 850 60  0001 C CNN
F 3 "" H 13650 850 60  0000 C CNN
F 4 "DNP" H 13650 850 60  0001 C CNN "Note"
	1    13650 850 
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR077
U 1 1 5600F9D3
P 13650 1150
F 0 "#PWR077" H 13650 900 50  0001 C CNN
F 1 "GND" H 13650 1000 50  0000 C CNN
F 2 "" H 13650 1150 60  0000 C CNN
F 3 "" H 13650 1150 60  0000 C CNN
	1    13650 1150
	1    0    0    -1  
$EndComp
Wire Wire Line
	13650 1050 13650 1150
$Comp
L Connector_Generic:Conn_01x01 MH4
U 1 1 560100F3
P 14150 1000
F 0 "MH4" H 14100 1100 50  0000 C CNN
F 1 "MOUNTING_HOLE" V 14250 1000 50  0000 C CNN
F 2 "gsg-modules:HOLE126MIL-COPPER" H 14150 1000 60  0001 C CNN
F 3 "" H 14150 1000 60  0000 C CNN
F 4 "DNP" H 14150 1000 60  0001 C CNN "Note"
	1    14150 1000
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR078
U 1 1 560100F9
P 14150 1300
F 0 "#PWR078" H 14150 1050 50  0001 C CNN
F 1 "GND" H 14150 1150 50  0000 C CNN
F 2 "" H 14150 1300 60  0000 C CNN
F 3 "" H 14150 1300 60  0000 C CNN
	1    14150 1300
	1    0    0    -1  
$EndComp
Wire Wire Line
	14150 1200 14150 1300
$Comp
L Connector_Generic:Conn_01x01 MH1
U 1 1 56010ADB
P 12650 850
F 0 "MH1" H 12600 950 50  0000 C CNN
F 1 "MOUNTING_HOLE" V 12750 850 50  0000 C CNN
F 2 "gsg-modules:HOLE126MIL-COPPER" H 12650 850 60  0001 C CNN
F 3 "" H 12650 850 60  0000 C CNN
F 4 "DNP" H 12650 850 60  0001 C CNN "Note"
	1    12650 850 
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR079
U 1 1 56010AE1
P 12650 1150
F 0 "#PWR079" H 12650 900 50  0001 C CNN
F 1 "GND" H 12650 1000 50  0000 C CNN
F 2 "" H 12650 1150 60  0000 C CNN
F 3 "" H 12650 1150 60  0000 C CNN
	1    12650 1150
	1    0    0    -1  
$EndComp
Wire Wire Line
	12650 1050 12650 1150
$Comp
L Connector_Generic:Conn_01x01 MH2
U 1 1 56010AE9
P 13150 1000
F 0 "MH2" H 13100 1100 50  0000 C CNN
F 1 "MOUNTING_HOLE" V 13250 1000 50  0000 C CNN
F 2 "gsg-modules:HOLE126MIL-COPPER" H 13150 1000 60  0001 C CNN
F 3 "" H 13150 1000 60  0000 C CNN
F 4 "DNP" H 13150 1000 60  0001 C CNN "Note"
	1    13150 1000
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR080
U 1 1 56010AEF
P 13150 1300
F 0 "#PWR080" H 13150 1050 50  0001 C CNN
F 1 "GND" H 13150 1150 50  0000 C CNN
F 2 "" H 13150 1300 60  0000 C CNN
F 3 "" H 13150 1300 60  0000 C CNN
	1    13150 1300
	1    0    0    -1  
$EndComp
Wire Wire Line
	13150 1200 13150 1300
Text Label 15350 7550 1    40   ~ 0
VBAT
Text Label 15250 7550 1    40   ~ 0
RESET
Text Label 15050 7550 1    40   ~ 0
RTC_ALARM
Wire Wire Line
	16050 7550 16050 7200
$Comp
L power:GND #PWR081
U 1 1 56035FE9
P 16050 7550
F 0 "#PWR081" H 16050 7300 50  0001 C CNN
F 1 "GND" H 16050 7400 50  0000 C CNN
F 2 "" H 16050 7550 60  0000 C CNN
F 3 "" H 16050 7550 60  0000 C CNN
	1    16050 7550
	1    0    0    -1  
$EndComp
Wire Wire Line
	15150 7550 15150 7200
$Comp
L power:GND #PWR082
U 1 1 56036BE7
P 15150 7550
F 0 "#PWR082" H 15150 7300 50  0001 C CNN
F 1 "GND" H 15150 7400 50  0000 C CNN
F 2 "" H 15150 7550 60  0000 C CNN
F 3 "" H 15150 7550 60  0000 C CNN
	1    15150 7550
	1    0    0    -1  
$EndComp
$Comp
L Interface:AM7969 U1
U 1 1 5CCFE902
P 5450 5050
F 0 "U1" H 5000 6200 50  0000 C CNN
F 1 "AM7969" H 5100 6100 50  0000 C CNN
F 2 "Package_LCC:PLCC-28" H 5450 5450 50  0001 C CNN
F 3 "" H 5450 5450 50  0001 C CNN
	1    5450 5050
	1    0    0    -1  
$EndComp
Text Label 7350 4250 0    50   ~ 0
SGPIO0
Text Label 7350 4350 0    50   ~ 0
SGPIO1
Text Label 7350 4450 0    50   ~ 0
SGPIO2
Text Label 7350 4550 0    50   ~ 0
SGPIO3
Text Label 7350 4650 0    50   ~ 0
SGPIO4
Text Label 7350 4750 0    50   ~ 0
SGPIO5
Text Label 7350 4850 0    50   ~ 0
SGPIO6
Text Label 7350 4950 0    50   ~ 0
SGPIO7
NoConn ~ 4850 5550
$Comp
L power:+5V #PWR0101
U 1 1 5CD14E15
P 5500 3750
F 0 "#PWR0101" H 5500 3600 50  0001 C CNN
F 1 "+5V" H 5515 3923 50  0000 C CNN
F 2 "" H 5500 3750 50  0001 C CNN
F 3 "" H 5500 3750 50  0001 C CNN
	1    5500 3750
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 5CD21578
P 5500 6350
F 0 "#PWR0102" H 5500 6100 50  0001 C CNN
F 1 "GND" H 5505 6177 50  0000 C CNN
F 2 "" H 5500 6350 50  0001 C CNN
F 3 "" H 5500 6350 50  0001 C CNN
	1    5500 6350
	1    0    0    -1  
$EndComp
Wire Wire Line
	5450 6150 5450 6250
Wire Wire Line
	5450 6250 5500 6250
Wire Wire Line
	5550 6250 5550 6150
Wire Wire Line
	5500 6250 5500 6350
Connection ~ 5500 6250
Wire Wire Line
	5500 6250 5550 6250
Wire Wire Line
	5450 3950 5450 3850
Wire Wire Line
	5450 3850 5500 3850
Wire Wire Line
	5550 3850 5550 3950
Wire Wire Line
	5500 3850 5500 3750
Connection ~ 5500 3850
Wire Wire Line
	5500 3850 5550 3850
NoConn ~ 6050 5850
Text Label 7350 5550 0    50   ~ 0
SGPIO8
Text Label 7350 5650 0    50   ~ 0
SGPIO9
Text Label 7350 5750 0    50   ~ 0
SGPIO10
Text Label 7350 5450 0    50   ~ 0
SGPIO11
Text Label 7350 5350 0    50   ~ 0
SGPIO12
Text Label 7350 5250 0    50   ~ 0
SGPIO13
Text Label 7350 5150 0    50   ~ 0
SGPIO14
Text Label 7350 5050 0    50   ~ 0
SGPIO15
$Comp
L Connector_Generic:Conn_01x02 J3
U 1 1 5CD3D07A
P 2600 4850
F 0 "J3" H 2520 4525 50  0000 C CNN
F 1 "Conn_01x02" H 2520 4616 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 2600 4850 50  0001 C CNN
F 3 "~" H 2600 4850 50  0001 C CNN
	1    2600 4850
	-1   0    0    1   
$EndComp
Text Notes 11250 4200 0    200  ~ 0
TODO:\nPick XTAL & add\nAdd RS232 stuff
Text Label 4850 4750 2    50   ~ 0
SERIN+
Text Label 4850 4850 2    50   ~ 0
SERIN-
$Comp
L Device:R R1
U 1 1 5CD51D8E
P 3200 4550
F 0 "R1" H 3270 4596 50  0000 L CNN
F 1 "120R" H 3270 4505 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 3130 4550 50  0001 C CNN
F 3 "~" H 3200 4550 50  0001 C CNN
	1    3200 4550
	1    0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 5CD51DD4
P 3200 5050
F 0 "R2" H 3270 5096 50  0000 L CNN
F 1 "330R" H 3270 5005 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 3130 5050 50  0001 C CNN
F 3 "~" H 3200 5050 50  0001 C CNN
	1    3200 5050
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0103
U 1 1 5CD51E12
P 3200 4400
F 0 "#PWR0103" H 3200 4250 50  0001 C CNN
F 1 "+5V" H 3215 4573 50  0000 C CNN
F 2 "" H 3200 4400 50  0001 C CNN
F 3 "" H 3200 4400 50  0001 C CNN
	1    3200 4400
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0104
U 1 1 5CD51E33
P 3200 5200
F 0 "#PWR0104" H 3200 4950 50  0001 C CNN
F 1 "GND" H 3205 5027 50  0000 C CNN
F 2 "" H 3200 5200 50  0001 C CNN
F 3 "" H 3200 5200 50  0001 C CNN
	1    3200 5200
	1    0    0    -1  
$EndComp
$Comp
L Device:R R3
U 1 1 5CD51F2F
P 3600 4550
F 0 "R3" H 3670 4596 50  0000 L CNN
F 1 "120R" H 3670 4505 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 3530 4550 50  0001 C CNN
F 3 "~" H 3600 4550 50  0001 C CNN
	1    3600 4550
	1    0    0    -1  
$EndComp
$Comp
L Device:R R4
U 1 1 5CD51F35
P 3600 5050
F 0 "R4" H 3670 5096 50  0000 L CNN
F 1 "330R" H 3670 5005 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 3530 5050 50  0001 C CNN
F 3 "~" H 3600 5050 50  0001 C CNN
	1    3600 5050
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0105
U 1 1 5CD51F3B
P 3600 4400
F 0 "#PWR0105" H 3600 4250 50  0001 C CNN
F 1 "+5V" H 3615 4573 50  0000 C CNN
F 2 "" H 3600 4400 50  0001 C CNN
F 3 "" H 3600 4400 50  0001 C CNN
	1    3600 4400
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0106
U 1 1 5CD51F41
P 3600 5200
F 0 "#PWR0106" H 3600 4950 50  0001 C CNN
F 1 "GND" H 3605 5027 50  0000 C CNN
F 2 "" H 3600 5200 50  0001 C CNN
F 3 "" H 3600 5200 50  0001 C CNN
	1    3600 5200
	1    0    0    -1  
$EndComp
Wire Wire Line
	2800 4750 3200 4750
Wire Wire Line
	3200 4750 3200 4700
Wire Wire Line
	2800 4850 3600 4850
Wire Wire Line
	3200 4750 3200 4900
Connection ~ 3200 4750
Wire Wire Line
	3600 4850 3600 4700
Connection ~ 3600 4850
Wire Wire Line
	3600 4900 3600 4850
Text Label 2800 4750 0    50   ~ 0
SERIN+
Text Label 2800 4850 0    50   ~ 0
SERIN-
$Comp
L Interface:74ALVC164245 U2
U 1 1 5CD8BD41
P 6950 4950
F 0 "U2" H 6950 6215 50  0000 C CNN
F 1 "74ALVC164245" H 6950 6124 50  0000 C CNN
F 2 "Package_SO:TSSOP-48_6.1x12.5mm_P0.5mm" H 6950 4950 50  0001 C CNN
F 3 "" H 6950 4950 50  0001 C CNN
	1    6950 4950
	1    0    0    -1  
$EndComp
Wire Wire Line
	6050 4250 6550 4250
Wire Wire Line
	6550 4350 6050 4350
Wire Wire Line
	6050 4450 6550 4450
Wire Wire Line
	6550 4550 6050 4550
Wire Wire Line
	6050 4650 6550 4650
Wire Wire Line
	6550 4750 6050 4750
Wire Wire Line
	6050 4850 6550 4850
Wire Wire Line
	6550 4950 6050 4950
Wire Wire Line
	6050 5050 6550 5050
Wire Wire Line
	6550 5150 6050 5150
Wire Wire Line
	6050 5250 6550 5250
Wire Wire Line
	6550 5350 6050 5350
Wire Wire Line
	6050 5550 6100 5550
Wire Wire Line
	6100 5550 6100 5450
Wire Wire Line
	6100 5450 6550 5450
Wire Wire Line
	6050 5750 6200 5750
Wire Wire Line
	6050 5950 6250 5950
Wire Wire Line
	6250 5950 6250 5750
Wire Wire Line
	6250 5750 6550 5750
Text Label 4850 5350 2    50   ~ 0
CLK
$Comp
L power:GND #PWR0107
U 1 1 5CE07E1C
P 4600 5650
F 0 "#PWR0107" H 4600 5400 50  0001 C CNN
F 1 "GND" H 4605 5477 50  0000 C CNN
F 2 "" H 4600 5650 50  0001 C CNN
F 3 "" H 4600 5650 50  0001 C CNN
	1    4600 5650
	1    0    0    -1  
$EndComp
Wire Wire Line
	4850 5450 4600 5450
Wire Wire Line
	4600 5450 4600 5650
Text Label 10050 2900 0    40   ~ 0
VBUS
$Comp
L power:+5V #PWR0108
U 1 1 5CE31150
P 10250 2900
F 0 "#PWR0108" H 10250 2750 50  0001 C CNN
F 1 "+5V" V 10265 3028 50  0000 L CNN
F 2 "" H 10250 2900 50  0001 C CNN
F 3 "" H 10250 2900 50  0001 C CNN
	1    10250 2900
	0    1    1    0   
$EndComp
Wire Wire Line
	10250 2900 10050 2900
$Comp
L power:+5V #PWR0109
U 1 1 5CE394DC
P 6200 3850
F 0 "#PWR0109" H 6200 3700 50  0001 C CNN
F 1 "+5V" H 6215 4023 50  0000 C CNN
F 2 "" H 6200 3850 50  0001 C CNN
F 3 "" H 6200 3850 50  0001 C CNN
	1    6200 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	6200 3850 6200 3950
Wire Wire Line
	6200 3950 6550 3950
$Comp
L power:VCC #PWR0110
U 1 1 5CE41ABC
P 7400 3850
F 0 "#PWR0110" H 7400 3700 50  0001 C CNN
F 1 "VCC" H 7417 4023 50  0000 C CNN
F 2 "" H 7400 3850 50  0001 C CNN
F 3 "" H 7400 3850 50  0001 C CNN
	1    7400 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	7400 3850 7400 3950
Wire Wire Line
	7400 3950 7350 3950
$Comp
L power:GND #PWR0111
U 1 1 5CE52F19
P 6750 6150
F 0 "#PWR0111" H 6750 5900 50  0001 C CNN
F 1 "GND" H 6755 5977 50  0000 C CNN
F 2 "" H 6750 6150 50  0001 C CNN
F 3 "" H 6750 6150 50  0001 C CNN
	1    6750 6150
	1    0    0    -1  
$EndComp
Wire Wire Line
	6950 6050 6750 6150
$Comp
L power:PWR_FLAG #FLG0101
U 1 1 5CE5BDA6
P 9450 2900
F 0 "#FLG0101" H 9450 2975 50  0001 C CNN
F 1 "PWR_FLAG" H 9450 3074 50  0000 C CNN
F 2 "" H 9450 2900 50  0001 C CNN
F 3 "~" H 9450 2900 50  0001 C CNN
	1    9450 2900
	1    0    0    -1  
$EndComp
Connection ~ 9450 2900
Wire Wire Line
	9450 2900 9550 2900
Text Label 6050 4250 0    50   ~ 0
DO0
Text Label 6050 4350 0    50   ~ 0
DO1
Text Label 6050 4450 0    50   ~ 0
DO2
Text Label 6050 4550 0    50   ~ 0
DO3
Text Label 6050 4650 0    50   ~ 0
DO4
Text Label 6050 4750 0    50   ~ 0
DO5
Text Label 6050 4850 0    50   ~ 0
DO6
Text Label 6050 4950 0    50   ~ 0
DO7
Text Label 6050 5050 0    50   ~ 0
CO3
Text Label 6050 5150 0    50   ~ 0
CO2
Text Label 6050 5250 0    50   ~ 0
CO1
Text Label 6050 5350 0    50   ~ 0
CO0
Text Label 6100 5450 0    50   ~ 0
VLTN
Text Label 6250 5650 0    50   ~ 0
DSTRB
Text Label 6200 5550 0    50   ~ 0
CSTRB
Text Label 6250 5750 0    50   ~ 0
CLK
Wire Wire Line
	6050 5650 6550 5650
Wire Wire Line
	6200 5750 6200 5550
Wire Wire Line
	6200 5550 6550 5550
$EndSCHEMATC
