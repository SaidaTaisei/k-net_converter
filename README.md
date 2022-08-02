# k-net_converter
k-net, kik-net to csv

# Download
Windows: [download converter.zip](https://www.u.tsukuba.ac.jp/~s2120854/converter_build.zip)

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
,MYG004_EW 100.0(Hz) unit:(gal)
0,0.4418442332371164
1,0.44438031703527514
2,0.4653030083701033
3,0.46720507121872146
4,0.45452465222791716
5,0.44628237988389685
6,0.447550421782978
7,0.4634009455214816
8,0.467839092168262
9,0.45389063127838014
.
.
.
```
