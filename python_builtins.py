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
import win32file
import win32api

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

def line():
  while True:
    try:
      code=input('line>>>')
      if code=='lines':return
      exec(code)
    except Exception as e:print(e)

while True:
  try:lines()
  except Exception as e:print(e)
  #else:print('no error then')
  #finally:input()
