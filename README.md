# ConStructUDP

ConStructUDP is a unicast binary message injection tool perfect for development, dubugging and error injection.

  - Define packed C/C++ data types and values in a JavaScript Object Notation file
  - Specify IPv4 target IP address and Port
  - Runs on Python 2.7
  - Made in the USA

*Any program is only as good as it is useful. -Linus Torvalds*   
*The best solutions solve problems locally. - Me*  

### Usage

ConStructUDP requires Python 2.7 to run.

```sh
$ python ConStructUDP.py struct.json
```
Example JSON file contents

- Field names must match exactly below, the struct list length and datatypes may be varied

```sh
{   
    "ip": "127.0.0.1",
    "port": 5555,
    "struct" : [

        {"char": "a"},
        {"signed char": 1},
        {"unsigned char": 2},
        {"bool": 1},
        {"short": -1},
        {"short": 3},
        {"unsigned short": 2},
        {"int": 50},
        {"unsigned int": 1},
        {"long": 11},
        {"unsigned long": 3},
        {"long long": 1000},
        {"unsigned long long": 44},
        {"float": 3.14},
        {"double": 3.14},
        {"char array": "hello"}
    ]
}
```

### Notes
- Binary packed struct will be sent in network order (Big-endian)

### Output
```sh
[remy@localhost ConStruct]$ python ConStructUDP.py struct.json 
Size of Packed Data:  59
Packed Data:  ('a', 1, 2, True, -1, 3, 2, 50, 1, 11, 3, 1000, 44, 3.140000104904175, 3.14, 'hello')
Sending to:  127.0.0.1 5555
```
*struct.json as example*
Notice the floating point skew from converting from double to float (3.14 to 3.140000104904175) 

### Test
In the test directory, run the runtests.py as a server and run ConStructUDP on localhost port 5555. 

License
----

MIT
**Free Software, Hell Yeah!**
