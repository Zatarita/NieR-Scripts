from struct import unpack, pack

class Serializable:
    # abstract method. I just don't want ABC
    def getFormat(): 
        return ("", 0)

    @classmethod
    def fromStream(cls, stream):
        fmt, size = cls.getFormat()
        return cls( *unpack( fmt, stream.read(size) ) )
        
    def toStream(self, stream):
        fmt, _ = self.getFormat()
        return stream.write(pack(fmt, *self.__dict__.values()))

        

@staticmethod
def readNtString(stream):
    ret = ""

    while((buffer := stream.read(1).decode("ascii")) != "\00"):
        ret += buffer

    return ret