@echo off

echo Extracting DDT Files...
:: Run this twice as some dats hold other dtts
for /r %%f in (*.dtt) do python dat.py "%%f"
for /r %%f in (*.dtt) do python dat.py "%%f"

echo Extracting DAT Files
:: Run this twice as some dats hold other dats
for /r %%f in (*.dat) do python dat.py "%%f"
for /r %%f in (*.dat) do python dat.py "%%f"

echo Extracting EFF Files...
for /r %%f in (*.eff) do python dat.py "%%f"

echo Extracting EVN Files...
:: Run this twice as some evns have other evns
for /r %%f in (*.evn) do python dat.py "%%f"
for /r %%f in (*.evn) do python dat.py "%%f"

echo Decompressing Z Files...
for /r %%f in (*.z) do python z.py "%%f" "%%~dpnf.txt"

echo Extracting TMD Files...
for /r %%f in (*.tmd) do python tmd.py "%%f"

echo Extracting WTP Files...
for /r %%f in (*.wtp) do ppython wtp.py "%%f" "%%~dpnf-wtp"

echo Extracting WTB Files...
for /r %%f in (*.wtb) do ppython wtb.py "%%f" "%%~dpnf-wtb"