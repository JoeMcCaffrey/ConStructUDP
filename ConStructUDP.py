import struct
import socket
import json
import sys

# this class will handle the udp socket
class Connection:

    def __init__(self, ip, port):
        self.__createSocket()

        self.__ip = ip
        self.__port = port
        
    def __createSocket(self):

        # declare an IP and UDP socket
        self.__socket = socket.socket(socket.AF_INET, \
            socket.SOCK_DGRAM)

    def sendSocket(self, struct_data):
        print "Sending to: ", self.__ip,":",self.__port
        self.__socket.connect((self.__ip, self.__port))

        self.__socket.sendall(struct_data)

    # Deconstructor
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
    #hash table of input data types translated to struct string

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
            "char array": "{}s"
        }

    def Lookup(self, s, l=0):
        if s in self.__data_types.keys():

            # if we get a length then its a char array so format with length
            if l :
                # return formatted map
                return self.__data_types[s].format(l)
            #otherwise return lookup
            return self.__data_types[s]
        else:
            # there was something invalid in the struct json file
            raise ValueError("invalid struct field", s)

def main():

    global no_unicode

    #open json file will be unicode
    with open(sys.argv[1]) as data_file:
        data = json.load(data_file)

    #create connection
    con = Connection(data["ip"], data["port"])
    types = DataTypes()

    parse_str =''
    vals = []
    for key in data["struct"]:

        #encode from unicode, struct doesnt take unicode
        field = key.keys()[0].encode('ascii','ignore')

        # if we have a char then convert and call lookup data type
        if field in ('char'):
            vals.append(key[field].encode("utf-8"))
            parse_str += types.Lookup(field)

        # char array here, convert and send length to lookup for fomatting
        elif field in ('char array'):
            s = key[field].encode("utf-8")
            vals.append(s)
            parse_str += types.Lookup(field, len(s))

        # other call by value datatype call directly
        else:
            vals.append(key[field])
            parse_str += types.Lookup(field)

    # pack the binary data with ! network order
    packed = PackStruct("!"+parse_str, vals)

    print "Size of Packed Data: ", packed.sizeOfPacked()
    print "Packed Data: ", packed.getUnPacked()
    # Send over that socket
    con.sendSocket(packed.getPacked())



if __name__ == "__main__":
    main()

