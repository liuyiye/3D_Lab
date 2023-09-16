from win32file import CreateFile, GetFileTime, SetFileTime, CloseHandle
from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from pywintypes import Time
from datetime import datetime

file=r'c:\0\1.txt'
fh = CreateFile(file, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)

#cam=GetFileTime(fh)
#print(cam)

c=Time(datetime(2023,9,16,9,16,8).timestamp())
a=Time(datetime(2023,9,16,9,16,16).timestamp())
m=Time(datetime(2023,9,16,9,16,32).timestamp())

SetFileTime(fh, c,a,m)
CloseHandle(fh)
