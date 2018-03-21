import numpy as np
from nbodykit.lab import *
from nbodykit import setup_logging, style
import matplotlib.pyplot as plt
import dask.array as da
import sys
from multiprocessing import Pool

inpath = "/home/users/chto/code/pair_sim/pair_simulation/HaloCatalogs/Halo_z0.0_{0:04d}/catalog_z0.0_{0:04d}.txt"
outpath = "/home/users/chto/code/pair_sim/pair_simulation/pk_nbodykit_out/"
def calculatePk(number):
    print("working on {0}" .format(number))
    sys.stdout.flush()
    cat = CSVCatalog(path=inpath.format(number), names=["x","y","z","vx","vy","vz","M"])
    cat['position']=da.stack([cat['x'],cat['y'],cat['z']]).T
    mesh = cat.to_mesh(window='cic', Nmesh=1024, compensated=True,BoxSize=1500,position='position')
    print("start making power")
    sys.stdout.flush()
# compute the power, specifying desired linear k-binning
    r = FFTPower(mesh, mode='1d', dk=0.05, kmin=0.01)
    Pk = r.power
    k=Pk['k']
    power = Pk['power'].real - Pk.attrs['shotnoise']
    
    print("start writing power")
    sys.stdout.flush()
    f = open(outpath+"Pk_{0}.pk".format(number),"w")
    f.write("k(h/Mpc) Pk(h/Mpc)^3\n")
    for i in range(len(Pk['k'])):
        f.write("{0} {1}\n".format(k[i],power[i]))
    f.close()
if __name__=="__main__":
    for i in range(1,101):
        calculatePk(i)
    
    
    
#p.map(calculatePk, range(1,101))
