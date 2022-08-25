from ast import While
from genericpath import isfile
import os
import sys

def ExtractWTP():
    data    = open(sys.argv[1], "rb").read()
    offsets = GetOffsets(data)
    sizes   = [ offsets[i + 1] - offsets[i] for i in range(len(offsets) - 1) ]

    if os.path.exists(sys.argv[2]):
        if os.path.isfile(sys.argv[2]):
            raise OSError("Unable to use path; path is a file: " + sys.argv[2])
    else:
        os.makedirs(sys.argv[2])

    for i in range(len(sizes)):
        with open(f"{sys.argv[2]}/{i:02d}.dds", "wb") as file:
            file.write(data[offsets[i]:offsets[i] + sizes[i]])

def GetOffsets(rawdata):
    offsets = [0]

    index = 0
    while True:
        index = rawdata.find(b"DDS\x20", index + 1) # No offset table, so I gotta sig scan :c
        if index < 0:
            break
        offsets.append(index)
    offsets.append(os.path.getsize(sys.argv[1]))

    return offsets


if len(sys.argv) < 3:
    print("python z.py <filename> <outpath>")
ExtractWTP()

