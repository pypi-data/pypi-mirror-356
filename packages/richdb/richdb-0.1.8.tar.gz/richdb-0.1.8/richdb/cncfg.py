# -*- encoding=utf8 -*-

'''
open .cn config file
.cn file is a kind of file for config or complex text content storage with time record.
this will help you to record the config file's every change time and what be changed,
this is very usefull for administrator.
you can store only one json or dict which start with { and end with }.
If a .cn file is empty,it means {}

{
    "a":1,
    "c":[1,2],
    "b":{
        "a":3,
        "e":{
            "b":4
        }
    }
}


in .cn file it will be like this:

+@:a:1,2022-07-01 12:13:11.10001
+@:c:1,2022-07-01 12:13:11.10040
+@:c:2,2022-07-01 12:13:11.20000
+@:b:a:3, 2022-07-01 12:13:11.20000
+@:b:e:b:4, 2022-07-01 12:13:11.20000

if you want to delete the "e" branch you can add this reccord to the .cn file
-@:b:e:b:4, 2022-07-01 12:13:11.30000

[1,2,3,4]

+(0,0)@:1, 2022-07-01 12:13:11.30000
+(0,1)@:2, 2022-07-01 12:13:11.30000
+(0,2)@:3, 2022-07-01 12:13:11.30000
+(0,3)@:4, 2022-07-01 12:13:11.30000

{
    a:[1,2,3,4]
}

+(0,0)(0,0)@:a:1,2022-07-01 12:13:11.30000
+(0,0)(0,1)@:a:2,2022-07-01 12:13:11.30000
+(0,0)(0,2)@:a:3,2022-07-01 12:13:11.30000
+(0,0)(0,3)@:a:4,2022-07-01 12:13:11.30000

This is the graph database's log and config design.It is very elegant and awesome.

you can also use the most simple mode as default


a:b:c
a:1
b:1
c:1

{
    "a":{
        "b":{
            "c":[2,4,5, [1,2,3]]
        }
    }
}

a:b:c:[0]:2
a:b:c:[1]:4
a:b:c:[2]:5
a:b:c:[3]:[0]:1
a:b:c:[3]:[1]:2
a:b:c:[3]:[2]:3

{
    "a":{
        "b":"[a]b:c"
        "c":1
    }
}

a:b:\[a\]b\:c
a:c:1

in simple mode you also can add datetime as modify datetime

a:c:2,2022-10-28 20：29

when you want to use the complex mode you should add in the head of the file:
#>complex

default is :
#>simple

dustmasker -in genome.fasta -infmt fasta -parse_seqids -outfmt maskinfo_asn1_bin -out dust.asnb

'''

class cncfg():
    def __init__(self):
        self.__dict = {}

    def __repr__():
        return self.__dict

    def __str__():
        return 
