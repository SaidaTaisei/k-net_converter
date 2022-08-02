# k-net_converter
k-net, kik-net to csv

# Download
Windows: [download converter.zip](https://github.com/SaidaTaisei/k-net_converter/raw/master/converter.zip)

# How to use
1. Download converter.zip from the link above.
2. Unzip the zip file.
3. Run converter.exe.
4. Drop the file you downloaded from k-net or kik-net (text format, binary is not supported, multiple files are acceptable) in the drag area.
5. Click the Run button.
6. The csv file will be output in the same directory as converter.exe.

# Output format
Output format is csv.  
Hz will be the same as the original data.  
All acceleration units are in gal (cm/sec^2).  
Specifically, data is stored as follows.  
```
,桐生_EW 100.0(Hz) unit:(gal)
0,0.002748846997483234
1,0.006564605911560939
2,0.006564605911560939
3,-0.003928731102152305
4,-0.015376007844383643
5,-0.0058366105591902695
6,0.016104003196754313
7,0.01991976211083113
8,-0.003928731102152305
9,-0.023961465401058035
.
.
.
```
