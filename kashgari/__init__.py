# encoding: utf-8
"""
@author: BrikerMan
@contact: eliyar917@gmail.com
@blog: https://eliyar.biz

@version: 1.0
@license: Apache Licence
@file: __init__.py.py
@time: 2019-01-19 13:42

"""
import kashgari.macros as k
from kashgari import embedding
from kashgari import tasks
from kashgari.utils.logger import init_logger
from . import corpus
from .macros import *
from .tokenizer import Tokenizer

init_logger()

if __name__ == "__main__":
    print("Hello world")