import warnings
import brainpy.math as bm
import jax
import numpy as np
import os 
import sys

current_path = os.getcwd()
sys.path.insert(0, current_path)
from bpusdk.Models.EImodel import EINet
from bpusdk.BrainpyLib.lb1_SNN import lb1_SNN
from bpusdk.BrainpyLib.lb1_deploy import lb1_deploy
from bpusdk.BrainpyLib.lb1_checkRes import lb1_checkRes
import random

warnings.filterwarnings("ignore")
random.seed(1)
bm.random.seed(42)
bm.set_dt(1.0)

def gen_net(scope):
    nNeuron = scope*1024
    nExc = int(nNeuron/2)
    nInh = int(nNeuron/2)
    nNeuron = nExc+nInh

    # conn = ["customized",data] 
    #conn = ['FixedPostNum', 1] 
    # conn = ['FixedPreNum', 5] 
    # conn = ['FixedTotalNum', 5] 
    conn = ['FixedProb', 5/nNeuron] 

    net = EINet(nExc, nInh, conn=conn, method = "euler", allow_multi_conn=False)
    return net                                                    

if __name__ == "__main__":
    download_dir = "../data6/40nm96k_bin_comp"
    upload_dir = "../data6"
    scope = 96
    nStep = 10

    #Gendata
    # net = gen_net(scope)
    # inpE = 100.                                      
    # inpS = np.zeros((nStep, scope*1024))
    # inpS = inpS.astype(bool)
    # bpuset = lb1_SNN(net, inpS, inpE)
    # net.dump(download_dir,inpS,inpE,nStep)           
    # bpuset.gen_bin_data(download_dir)
    
    # # Deploy
    xdma_id = 8
    # deploy = lb1_deploy(download_dir,upload_dir)
    # deploy.run_Xdao(step=nStep,xdma_id=xdma_id)

    # convert bin to npy
    
    for xdma_id in range(10):
        server_id = 2007
        upload_dir1 = f"{upload_dir}/ei_data_{scope}k_0.5/bpu-{server_id}_{xdma_id:02d}"
        check = lb1_checkRes(download_dir, upload_dir1, nStep)
        check.bin2npy(sw_compare=True)

