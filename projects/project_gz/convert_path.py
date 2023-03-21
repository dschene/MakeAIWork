#!/usr/bin/env python3

import os
import sys

def main():
    osPath = str(sys.argv[1])
    print(os.path.abspath(osPath))

if __name__ == "__main__":
    main()
        