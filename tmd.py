from ast import arg
import os
import struct
import sys
from turtle import color
import colorama

class TMDFile:
    def __init__(self) -> None:
        self.Count = None
        self.Strings = None

    def toTxt(self, path):
        with open(path, "w") as file:
            for name, value in self.Strings.items():
                file.write(f"{name}: {value}\n")


    @classmethod
    def fromFile(cls, path : str):
        if not os.path.exists(path): raise OSError(f"Unable to find requested file: {path}")
        if not os.path.isfile(path): raise OSError(f"Unable to open requested path; it's a directory: {path}")

        ret = cls()
        with open(path,"rb") as file:
            ret.Count = int.from_bytes(file.read(4), "little")
            if (strings := cls._readStrings(file, ret.Count)) is not None:
                ret.Strings = strings
        return ret

    @staticmethod
    def _readStrings(file, count):
        ret = {}
        
        for i in range(count):
            try:
                Entry = {
                    file.read(2 * int.from_bytes(file.read(4), "little")).decode("utf-16").rstrip("\x00") : 
                    file.read(2 * int.from_bytes(file.read(4), "little")).decode("utf-16").rstrip("\x00")
                }
                ret.update(Entry)
            except:
                return None
        
        return ret

colorama.init()

if len(sys.argv) <= 1:
    print(colorama.Fore.CYAN + "python tmd.py <filename>")
else:
    test = TMDFile.fromFile(sys.argv[1])
    outpath = sys.argv[1][:-3] + "txt"

    print(colorama.Fore.CYAN + f"Writing {len(test.Strings)} entries to {outpath}... ", end=' ')
    if test is not None:
        test.toTxt(outpath)
    print(colorama.Fore.GREEN + f"Done!")