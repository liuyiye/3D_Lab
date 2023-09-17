def packages():
  import profile
  import smtplib
  import sqlite3
  import time
  import timeit
  import trace
  import argparse
  import asyncio
  import codecs
  import collections
  import configparser
  import copy
  import csv
  import datetime
  import difflib
  import getpass
  import gettext
  import io
  import itertools
  import json
  import locale
  import logging
  import math
  import mmap
  import multiprocessing
  import os
  import pickle
  import pydoc
  import random
  import re
  import shutil
  import signal
  import socket
  import sys
  import tempfile
  import threading
  import unittest
  import webbrowser
  import zlib
  
def line():
  while True:
    try:
      code=input('line>>>')
      if code=='lines':return
      exec(code)
    except Exception as e:print(e)

def lines():
  print('lines:')
  mem_file=io.StringIO()
  while True:
    i=input()
    if i=='line':line()
    if i=='':break
    mem_file.write(i+'\n')
  code=mem_file.getvalue()
  exec(code)

def t():
  from win32file import CreateFile, GetFileTime, SetFileTime, CloseHandle
  from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
  from pywintypes import Time
  from datetime import datetime
  import win32timezone
  
  file=input(r'filename c:\0\1.txt: ') or 'c:\\0\\1.txt'
  ct=input('createTime datetime(2023,9,17,9,17,9): ') or 'datetime(2023,9,17,9,17,9)'
  at=input('accessTime datetime(2023,9,17,9,17,7): ') or 'datetime(2023,9,17,9,17,7)'
  mt=input('modifyTime datetime(2023,9,17,9,17,1): ') or 'datetime(2023,9,17,9,17,1)'

  c=Time(eval(ct).timestamp())
  a=Time(eval(at).timestamp())
  m=Time(eval(mt).timestamp())
  
  fh = CreateFile(file, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
  #cam=GetFileTime(fh)
  #print(cam)
  SetFileTime(fh, c,a,m)
  CloseHandle(fh)

import io
while True:
  try:lines()
  except Exception as e:print(e)
  #else:
  #finally:
