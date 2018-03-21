import numpy as np
from nbodykit.lab import *
from nbodykit import setup_logging, style
import matplotlib.pyplot as plt
import dask.array as da
import sys
from multiprocessing import Pool
import gc
import os
inpath = "/home/users/chto/code/pair_sim/pair_simulation/HaloCatalogs/Halo_z0.0_{0:04d}/catalog_z0.0_{0:04d}.txt"
outpath = "/home/users/chto/code/pair_sim/pair_simulation/pk_nbodykit_jack_5/"
def makejack(boxsizes, number_of_jack):
    lengthx = float(boxsizes[0])/number_of_jack
    lengthy = float(boxsizes[1])/number_of_jack
    lengthz = float(boxsizes[2])/number_of_jack
    rangeList=[]
    for idx in range(number_of_jack):
        for idy in range(number_of_jack):
            for idz in range(number_of_jack):
                rangex = [idx*lengthx, (idx+1)*lengthx]
                rangey = [idy*lengthz, (idy+1)*lengthy]
                rangez = [idz*lengthz, (idz+1)*lengthz]
                rangeList.append([rangex,rangey,rangez]) 
    return rangeList 

def calculatejackPk(number_of_jack):
    cat = CSVCatalog(path=inpath.format(1), names=["x","y","z","vx","vy","vz","M"])
    jackknifeList = makejack([1500,1500,1500], number_of_jack)
    cat['position']=da.stack([cat['x'],cat['y'],cat['z']]).T
    for jacknumber, rangeList in enumerate(jackknifeList):
        print("making jack {0}".format(jacknumber))
        sys.stdout.flush()
        outName = outpath+"Pk_jack{0}.pk".format(jacknumber)
        if os.path.isfile(outName):
            print("jack {0} already exists".format(jacknumber))
            sys.stdout.flush()
            continue
        mask = np.logical_not((cat['x']>rangeList[0][0])&(cat['x']<rangeList[0][1])&
                (cat['y']>rangeList[1][0])&(cat['y']<rangeList[1][1])&
                (cat['z']>rangeList[2][0])&(cat['z']<rangeList[2][1]))
        cat_new = cat[mask]
        mesh = cat_new.to_mesh(window='cic', Nmesh=1024, compensated=True,BoxSize=1500,position='position')
        print("start making power")
        sys.stdout.flush()
# compute the power, specifying desired linear k-binning
        r = FFTPower(mesh, mode='1d', dk=0.05, kmin=0.01)
        Pk = r.power
        k=Pk['k']
        power = Pk['power'].real - Pk.attrs['shotnoise']
        print("start writing power")
        sys.stdout.flush()
        f = open(outName,"w")
        f.write("k(h/Mpc) Pk(h/Mpc)^3\n")
        for i in range(len(Pk['k'])):
            f.write("{0} {1}\n".format(k[i],power[i]))
        f.close()
        del mesh
        del cat_new
        gc.collect()

if __name__=="__main__":
   calculatejackPk(5)
    
    
#p.map(calculatePk, range(1,101))
