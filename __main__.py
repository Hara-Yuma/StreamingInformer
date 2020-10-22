#!/usr/bin/env python3
from argparse import ArgumentParser
from CUI import CUI
from GUI import GUI

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-m', '--mode', action='store', default='gui', type=str, choices=['cui', 'gui'], dest='mode')
    args = parser.parse_args()

    if args.mode == 'cui':
        ui = CUI()
    elif args.mode == 'gui':
        ui = GUI()

    ui.run()
