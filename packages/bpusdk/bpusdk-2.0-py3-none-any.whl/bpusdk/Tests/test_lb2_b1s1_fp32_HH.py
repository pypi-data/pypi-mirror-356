import time
import warnings
import brainpy.math as bm
import numpy as np
import random
import os 
import sys

current_path = os.getcwd()
sys.path.insert(0, current_path)
from bpusdk.Models.EImodel_HH import EINet
from bpusdk.BrainpyLib.lb2_SNN import lb2_SNN
from bpusdk.BrainpyLib.lb2_checkRes import lb2_checkRes
from bpusdk.BrainpyLib.lb2_deploy import lb2_deploy

warnings.filterwarnings("ignore")
random.seed(1)
bm.random.seed(42)
bm.set_dt(1.0)

def gen_net(nExc,nInh):
    nNeuron = nExc+nInh

    t0 = time.time()
    arr = np.arange(nExc+nInh)
    shuffled_arr = np.random.permutation(arr)   
    data = np.vstack((arr,shuffled_arr))

    conn = ["customized",data] 
    #conn = ['FixedPostNum', 1] 
    # conn = ['FixedPreNum', 5] 
    # conn = ['FixedTotalNum', 5] 
    # conn = ['FixedProb', 5/nNeuron] 
    # conn = ["prob", 5/nNeuron] 

    net = EINet(nExc, nInh, conn=conn, method = "euler")
    t1 = time.time()
    print(f"{nNeuron//1024}k network generated in {t1-t0:.2f} seconds")
    return net

if __name__ == "__main__":
    download_dir = "../data6/Lb2_64k_HH"
    upload_dir = "../upload6/ResLb2_64k_HH"
    nExc = 8*1024
    nInh = 8*1024
    nStep = 20

    # # Gendata
    net = gen_net(nExc,nInh)
    inpE = 100.                                       
    inpS = np.zeros((nStep, nExc+nInh))
    inpS = inpS.astype(bool)    
    bpuset = lb2_SNN(net, inpS, inpE)
    net.dump(download_dir,inpS,inpE,nStep,save=False,jit=True)     
    bpuset.gen_bin_data(download_dir)
    #bpuset.gen_hex_data(download_dir)

    # # Deploy
    # sender_path = "/home/gdiist/work/git/LBII_timetest/build/LBII"
    # deploy = lb2_deploy(download_dir,upload_dir)
    # deploy.run(step=nStep,sender_path=sender_path,device_id=0)

    # # # Compare results or convert bin to npy
    # check = lb2_checkRes(download_dir, upload_dir, nStep)
    # check.bin2npy(sw_compare=True)