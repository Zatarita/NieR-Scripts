import zlib
import sys

if len(sys.argv) < 3:
    print("python z.py <filename> <outpath>")

data = open(sys.argv[1], "rb").read()
try:
    open(sys.argv[2], "wb").write(zlib.decompress(data))
    print(sys.argv[1])
except:
    print(sys.argv[1])