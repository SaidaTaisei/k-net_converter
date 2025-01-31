# k-net_converter
k-net, kik-net to csv

# Download
The link was broken, so I updated the link.  
Windows: [download converter.zip](https://github.com/SaidaTaisei/k-net_converter/blob/master/converter_build/converter.exe)

# How to use
1. Download converter.zip from the link above.
2. Unzip the zip file.
3. Run converter.exe.
4. Drop the file you downloaded from k-net or kik-net (text format only, binary is not supported, multiple files are acceptable) in the drag area.
5. Click the Run button.
6. The csv file will be output in the same directory as converter.exe.


https://user-images.githubusercontent.com/62459697/182280770-abf01fc9-07fa-4069-979b-f89eba16c8f7.mp4


# Input format
The input type is a tar.gz file downloaded from the [NIED web page](https://www.kyoshin.bosai.go.jp/kyoshin/). (When expanded, the file contains .EW, .NS, and .UD.)

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
