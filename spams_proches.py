from ctypes import *
import sys

lib = CDLL("ressemblances.so")
lib.fichier_proximite("fichier_proximite.txt","Messages","gzip","gunzip","gz")
