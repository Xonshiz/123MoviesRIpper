#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append("..")
from movies import *

if __name__ == "__main__":
    Movies(sys.argv[1:], os.getcwd())
    sys.exit()
