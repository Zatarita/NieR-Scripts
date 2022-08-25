from fileinput import filename
from struct import pack, unpack, calcsize
from dataclasses import dataclass
import os
import sys
from colorama import init, Fore
from shared import Serializable

@dataclass
class DATHeader(Serializable):
    Signature       : str = ""
    Count           : int = 0
    pOffsetTable    : int = 0
    pExtensionTable : int = 0
    pFileNameTable  : int = 0
    pFileSizeTable  : int = 0
    pUnknown        : int = 0

    @staticmethod
    def getFormat():
        return ("<4s6I", 28)

class DATFile:
    def __init__(self) -> None:
        self.Header     = None
        self.Offsets    = None
        self.Extensions = None
        self.Filenames  = None
        self.Filesizes  = None

        self.Data       = None

    def extractAll(self, path, overwrite = False):
        if os.path.exists(path):
            if os.path.isfile(path): 
                raise OSError(f"Path supplied is a file: {path}")
        else:
            os.makedirs(path)

        if self.Header.Count == 0:
            print(Fore.YELLOW + "\t[IGNORING EMPTY DAT FILE]")
            return

        for name in self.Filenames:
            try:
                if self.extract(name, path, overwrite):
                    print("\t" + Fore.GREEN + name)
                else:
                    print("\t" + Fore.YELLOW + name + "  \t[ALREADY EXISTS - IGNORING]")
            except(...):
                print("\t" + Fore.RED + name)

    def extract(self, name : str, path : str, overwrite = False):
        if os.path.exists(path):
            if os.path.isfile(path): 
                raise OSError(f"Path supplied is a file: {path}")

        if self.Filenames is not None:
            if name not in self.Filenames:
                raise OSError("Unable to extract: Requested filename doesn't exist: " + name)
        else:
            raise AttributeError("Filenames haven't been initialized.")

        if os.path.exists(f"{path}\{name}"):
            if not overwrite:
                return False

        with open(f"{path}\{name}", "wb") as file:
            file.write(self.Data[name])

        return True

    @classmethod
    def fromFile(cls, path: str):
        if not os.path.exists(path): raise OSError(f"File not found: {path}")
        if not os.path.isfile(path): raise OSError(f"Path supplied is not a file: {path}")

        ret = cls()

        with open(path, "rb") as file:
            ret.Header     = DATHeader.fromStream(file)

            file.seek(ret.Header.pOffsetTable)
            ret.Offsets    = list( unpack( "<" + ("I" * ret.Header.Count), file.read( 4 * ret.Header.Count ) ) )
            
            file.seek(ret.Header.pExtensionTable)
            ret.Extensions = list( unpack( "<" + ("4s" * ret.Header.Count), file.read( 4 * ret.Header.Count ) ) )
            
            file.seek(ret.Header.pFileNameTable)
            fileNameSize   = int.from_bytes(file.read(4), "little")
            ret.Filenames  = [file.read(fileNameSize).decode("ascii").rstrip("\x00") for x in range(ret.Header.Count)]
            
            file.seek(ret.Header.pFileSizeTable)
            ret.Filesizes  = list( unpack( "<" + ("I" * ret.Header.Count), file.read( 4 * ret.Header.Count ) ) )

            ret.Data = {}
            for i in range(ret.Header.Count):
                file.seek(ret.Offsets[i])
                ret.Data.update({ret.Filenames[i]: file.read(ret.Filesizes[i])})

        return ret

init()


if len(sys.argv) <= 1:
    print(Fore.CYAN + "python dat.py <filename>")
else:
    if os.path.getsize(sys.argv[1]) == 0:
        print(Fore.YELLOW + "Ignoring empty file")
        exit()
    test = DATFile.fromFile(sys.argv[1])
    print(Fore.CYAN + f"Writing {sys.argv[1]}... ")
    test.extractAll(sys.argv[1][:-3])
    print("")

