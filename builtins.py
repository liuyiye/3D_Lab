def h():
    print('''
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
  import win32timezone
  
  file=input('filename:1.txt: ') or '1.txt'
  c=input('createTime Time((2023,9,16,9,16,8,0,0,0)):  ') or 'Time((2023,9,16,9,16,8,0,0,0))'
  a=input('accessTime Time((2023,9,16,9,16,16,0,0,0)): ') or 'Time((2023,9,16,9,16,16,0,0,0))'
  m=input('modifyTime Time((2023,9,16,9,16,32,0,0,0)): ') or 'Time((2023,9,16,9,16,32,0,0,0))'
  
  fh = CreateFile(file, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
  #cam=GetFileTime(fh)
  #print(cam)
  SetFileTime(fh, eval(c),eval(a),eval(m))
  CloseHandle(fh)

import io
while True:
  try:lines()
  except Exception as e:print(e)
  #else:
  #finally:
''')

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
  import win32timezone
  
  file=input('filename:1.txt: ') or '1.txt'
  c=input('createTime Time((2023,9,16,9,16,8,0,0,0)):  ') or 'Time((2023,9,16,9,16,8,0,0,0))'
  a=input('accessTime Time((2023,9,16,9,16,16,0,0,0)): ') or 'Time((2023,9,16,9,16,16,0,0,0))'
  m=input('modifyTime Time((2023,9,16,9,16,32,0,0,0)): ') or 'Time((2023,9,16,9,16,32,0,0,0))'
  
  fh = CreateFile(file, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
  #cam=GetFileTime(fh)
  #print(cam)
  SetFileTime(fh, eval(c),eval(a),eval(m))
  CloseHandle(fh)

import io
while True:
  try:lines()
  except Exception as e:print(e)
  #else:
  #finally:
