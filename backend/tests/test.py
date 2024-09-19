import os
import sys

parent_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(parent_dir)


import unittest
from tests.test_auth_router import *

unittest.main()
