#!/usr/bin/env python

import argparse, os, treat_nfo

def clean_uninteresting_file(path_file_mjr, path_file_nfo):
    os.system("rm -f " + path_file_mjr)
    if (os.path.exists(path_file_nfo)):
        os.system("rm -f " + path_file_nfo)

def clean_nfo(path_file_nfo, FileName):
    nfo = treat_nfo.TreatNfo(path_file_nfo, FileName, "clean")
    nfo.CreateCleanedNfo()
    nfo.DeleteNfo()

def clean_up(folder):
    for file in os.listdir(folder):
        if file.endswith(".mjr"):
            name_file = file.split(".")
            path_file_nfo = folder + file.split("-")[1] + ".nfo"
            path_file_mjr = folder + "/" + file

            if os.path.getsize(path_file_mjr) <= 8:
                clean_uninteresting_file(path_file_mjr, path_file_nfo)
            else:
                clean_nfo(path_file_nfo, file.split("-")[1])

def pars_argument():
    parser = argparse.ArgumentParser()

    parser.add_argument("folder", help = "set the folder to be cleaned (required absolute path)", type = str)
    parser.add_argument("--dny_run", help = "display the execution of the program")

    args = parser.parse_args()

    if args.dny_run:
        print """execution :
        -Delete .mjr file with size less than 8 bytes and .nfo associated
        -Refactor .nfo badly formatted
        -Create a .nfo.clean
        -Remove .nfo"""
    return args.folder

if __name__ == "__main__":
    folder = pars_argument()

    clean_up(folder)
