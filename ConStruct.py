import struct
import socket
import json
import sys

class Connection:

    def __init__(self, ip, port):
        self.__createSocket()

        self.__ip = ip
        self.__port = port
        

    def __createSocket(self):
        self.__socket = socket.socket(socket.AF_INET, \
            socket.SOCK_DGRAM)

    def sendSocket(self, struct_data):
        self.__socket.connect((self.__ip, self.__port))

        self.__socket.sendall(struct_data)


    def __del__(self):
        self.__socket.close()


class PackStruct:

    def __init__(self, pack_str, values):
        self.__struct = struct.Struct(pack_str)
        self.__data = self.__struct.pack(*values)
        self.__values = values

    def getPacked(self):
        return self.__data

    def getUnPacked(self):
        return self.__struct.unpack(self.__data)

    def getValues(self):
        return self.__values

    def sizeOfPacked(self):
        return self.__struct.size

    def fmtString(self):
        return self.__struct.format


class DataTypes:
 

    def __init__(self):

        self.__data_types = {

            "char": "c",
            "signed char": "b",
            "unsigned char": "B",
            "bool": "?",
            "short": "h",
            "unsigned short": "H",
            "int": "i",
            "unsigned int": "I",
            "long": "l",
            "unsigned long": "L",
            "long long": "q",
            "unsigned long long": "Q",
            "float": "f",
            "double": "d",
            "char array": "s"
        }

    def Lookup(self, s):
        if s in self.__data_types.keys():
            return self.__data_types[s]
        else:
            raise ValueError("invalid struct field", s)

def main():

    global no_unicode
    with open(sys.argv[1]) as data_file:
        data = json.load(data_file)
 
    con = Connection(data["ip"], data["port"])
    types = DataTypes()

    parse_str =''
    vals = []
    for key in data["struct"]:
        field = key.keys()[0].encode('ascii','ignore')
        parse_str += types.Lookup(field)

        if field in ('char', 'char array'):
            vals.append(key[field].encode("utf-8"))
        else:
            vals.append(key[field])

    packed = PackStruct("!"+parse_str, vals)

    con.sendSocket(packed.getPacked())



if __name__ == "__main__":
    main()

