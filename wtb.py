from dataclasses import dataclass
from genericpath import isfile
from shared import Serializable
import struct
import os
import sys

@dataclass
class WTBHeader(Serializable):
    Signature    : str = ""
    UnknownCount : int = 0
    TextureCount : int = 0
    MetaOffset   : int = 0

    def getFormat():
        return ("<4s3I", 16)

class WTBFile:
    def __init__(self) -> None:
        self.Header   = None
        self.Textures = None

    @classmethod
    def fromFile(cls, path: str):
        if not os.path.exists(path): raise OSError("Path doesn't exist: " + path)
        if not os.path.isfile(path): raise OSError("Unable to open path; It's not a file " + path)

        ret = cls()
        with open(path, "rb") as file:
            ret.Header = WTBHeader.fromStream(file)
            unknownOffsets = list(struct.unpack("<" + ("I" * ret.Header.UnknownCount), file.read(4 * ret.Header.UnknownCount)))
            unknown = int.from_bytes(file.read(4), "little")
            Offsets = list(struct.unpack("<" + ("I" * ret.Header.TextureCount), file.read(4 * ret.Header.TextureCount)))
            Offsets.append(os.path.getsize(path))
            Sizes = [ Offsets[i + 1] - Offsets[i] for i in range(len(Offsets) - 1) ]

            ret.Textures = []
            for i in range(len(Sizes)):
                file.seek(Offsets[i])
                ret.Textures.append(file.read(Sizes[i]))
        return ret

    def extract(self, index: int, path: str):
        if os.path.exists(path):
            if os.path.isfile(path):
                raise OSError("Unable to extract to requested path; path is file: " + path)
        else:
            os.makedirs(path)

        if index > len(self.Textures):
            raise AttributeError("Index exceeds the bounds of the list")

        with open(f"{path}/{index:02d}.dds", "wb") as file:
            file.write(self.Textures[index])

    def extractAll(self, path : str):
        for i in range(len(self.Textures)):
            self.extract(i, path)

test = WTBFile.fromFile(sys.argv[1])
test.extractAll(sys.argv[2])
        
                
            
            
