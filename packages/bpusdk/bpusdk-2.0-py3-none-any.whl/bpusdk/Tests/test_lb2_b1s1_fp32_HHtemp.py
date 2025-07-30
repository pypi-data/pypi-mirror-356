import time
import warnings
import brainpy.math as bm
import numpy as np
import random
import os 
import sys

current_path = os.getcwd()
sys.path.insert(0, current_path)
from bpusdk.Models.EImodel_HHtemp import EINet
from bpusdk.BrainpyLib.lb2_SNN import lb2_SNN
from bpusdk.BrainpyLib.lb2_checkRes import lb2_checkRes
from bpusdk.BrainpyLib.lb2_deploy import lb2_deploy

warnings.filterwarnings("ignore")
random.seed(1)
bm.random.seed(42)
dt = 1.
bm.set_dt(dt)

def gen_net(nExc,nInh):
    nNeuron = nExc+nInh

    t0 = time.time()
    arr = np.arange(nExc+nInh)
    shuffled_arr = np.random.permutation(arr)   
    data = [np.array([])]

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
    download_dir = "../data7/Lb2_mode3_16k_HHtemp_hex"
    upload_dir = "../upload7/ResLb2_mode3_16k_HHtemp"
    nExc = 8*1024
    nInh = 8*1024
    #nStep = int(6/dt)
    nStep = 10

    # Gendata
    net = gen_net(nExc,nInh)
    inpE = 0.                                       
    inpS = np.zeros((nStep, nExc+nInh))
    inpS = inpS.astype(bool)    
    bpuset = lb2_SNN(net, inpS, inpE, mode=3)
    net.dump(download_dir,inpS,inpE,nStep,save=False,jit=False)     
    #bpuset.gen_bin_data(download_dir)
    bpuset.gen_hex_data(download_dir)

    # # Deploy
    # deploy = lb2_deploy(download_dir,upload_dir)
    # sender_path = "~/work/LBII/build/LBII"
    # deploy.run_from_host(step=nStep,sender_path=sender_path,device_id=15)
    # # #  deploy.run_from_driver(step=nStep,device_id=16,dmos=False)


    # # # # Compare results or convert bin to npy
    # check = lb2_checkRes(download_dir, upload_dir, nStep)
    # # check.bin2npy(sw_compare=True)
    
    # print('\n step0:')
    # check.ref_v(0)
    # print('\n step1:')
    # check.ref_v(1)
    # print('\n step2:')
    # check.ref_v(2)
    # print('\n step3:')
    # check.ref_v(3)
    # print('\n step4:')
    # check.ref_v(4)
    