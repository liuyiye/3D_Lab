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
  import msvcrt
  import PIL
  import numpy
  import pydicom
  import pynetdicom

import sys
import codecs
import chardet
if len(sys.argv)==2:
  file=sys.argv[1]
  with open(file, 'rb') as f:
    enc = chardet.detect(f.read(10000))['encoding']
  with codecs.open(file, encoding=enc) as f:
    exec(f.read())
else:print('usage: python3d xxx.py')
