import time
import warnings
import brainpy.math as bm
import numpy as np
import random
import os 
import sys

current_path = os.getcwd()
sys.path.insert(0, current_path)
from bpusdk.Models.EImodel import EINet
from bpusdk.BrainpyLib.lb2_SNN import lb2_SNN
from bpusdk.BrainpyLib.lb2_checkRes import lb2_checkRes
from bpusdk.BrainpyLib.lb2_deploy import lb2_deploy

def gen_net(nExc,nInh):
    nNeuron = nExc+nInh

    t0 = time.time()
    arr = np.arange(nExc+nInh)
    shuffled_arr = np.random.permutation(arr)
    #conn = ["customized",np.vstack((arr,np.roll(arr,-1)))] 
    conn = ["customized",np.vstack((arr,shuffled_arr))] 
    #conn = ['FixedPostNum', 1] 
    # conn = ['FixedPreNum', 5] 
    # conn = ['FixedTotalNum', 5] 
    # conn = ['FixedProb', 5/nNeuron] 

    net = EINet(nExc, nInh, conn=conn, method = "euler")
    t1 = time.time()
    print(f"{nNeuron//1024}k network generated in {t1-t0:.2f} seconds")
    return net

warnings.filterwarnings("ignore")
random.seed(1)
bm.random.seed(1864)
bm.set_dt(1.0)

if __name__ == "__main__":
    download_dir = "../data7/Lb2_mode2_32k"
    upload_dir = "../upload7/ResLb2_mode2_32k" 
    nExc = 16*1024
    nInh = 16*1024
    nStep = 20

    # Gendata
    net = gen_net(nExc,nInh)
    inpE = 100.                                       
    inpS = np.zeros((nStep, nExc+nInh))
    inpS = inpS.astype(bool)    
    bpuset = lb2_SNN(net, inpS, inpE, mode=2)
    net.dump(download_dir,inpS,inpE,nStep,save=True,jit=True)     
    bpuset.gen_bin_data(download_dir)
    #bpuset.gen_hex_data(download_dir)

    # Deploy
    deploy = lb2_deploy(download_dir,upload_dir)
    sender_path = "/home/test1/work/LBII_matrix/build/LBII"
    deploy.run_from_host(step=nStep,sender_path=sender_path,device_id=15)
    # deploy.run_from_driver(step=nStep,device_id=7,dmos=False)

    # # Compare results or convert bin to npy
    check = lb2_checkRes(download_dir, upload_dir, nStep)
    check.bin2npy()
    check.npyVSnpy() 