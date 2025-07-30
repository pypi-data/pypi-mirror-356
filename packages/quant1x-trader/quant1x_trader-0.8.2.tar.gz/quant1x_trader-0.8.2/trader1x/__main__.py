# -*- coding: UTF-8 -*-
import sys

from q1x import base

base.redirect('trader1x', __file__)

from trader1x.auto import auto_trader


if __name__ == '__main__':
    sys.exit(auto_trader())
