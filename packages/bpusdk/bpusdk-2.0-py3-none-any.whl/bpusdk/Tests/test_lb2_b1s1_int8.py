import time
import warnings
import brainpy.math as bm
import numpy as np
import random
import os 
import sys

current_path = os.getcwd()
sys.path.insert(0, current_path)
from bpusdk.Models.EImodel_lb2_int8 import EINet
from bpusdk.BrainpyLib.lb2_SNN import lb2_SNN
from bpusdk.BrainpyLib.lb2_checkRes import lb2_checkRes
from bpusdk.BrainpyLib.lb2_deploy import lb2_deploy

warnings.filterwarnings("ignore")
random.seed(1)
bm.random.seed(42)
bm.set_dt(2.0)

def createConn(nNeuron,fanOut,groupSize):
    iNeuron_list = list(np.arange(nNeuron))
    nGroup = int(np.ceil(nNeuron/groupSize)) #last group may have a different size
    group_pre_list = list(np.arange(nGroup))
    group_pre_list = [item for item in group_pre_list for _ in range(fanOut)]
    if fanOut < groupSize:
        # with no replacement -> act as pre once/never
        # risk for self connection
        group_post_list = random.sample(iNeuron_list, k=len(group_pre_list))
    else:
        group_post_list = random.choice(iNeuron_list, k=len(group_pre_list))
        #TODO: check multiple connection here
    pre_list = []
    post_list = []
    for pre,post in zip(group_pre_list,group_post_list):
        if pre == nGroup:
            tmp_pre = np.arange(pre*groupSize,nNeuron)
            tmp_post = [post]*len(tmp_pre)
        else:
            tmp_pre = np.arange(pre*groupSize,pre*groupSize+groupSize)
            tmp_post = [post]*groupSize
        pre_list.extend(tmp_pre)
        post_list.extend(tmp_post)
    return pre_list,post_list

def gen_net(nExc,nInh):
    nNeuron = nExc+nInh
    t0 = time.time()

    data = np.array(createConn(nNeuron,fanOut=2,groupSize=4))  
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
    download_dir = "../data7/Lb2_int8_576k"
    upload_dir = "../upload7/ResLb2_int8_576k"
    nExc = 288*1024
    nInh = 288*1024
    nStep = 18
    
    #Gendata
    net = gen_net(nExc,nInh)
    inpE = 2.                                       
    inpS = np.zeros((nStep, nExc+nInh))
    inpS = inpS.astype(bool)    
    bpuset = lb2_SNN(net, inpS, inpE, config={"Dtype":"int8"})
    net.dump(download_dir,inpS,inpE,nStep,save=True,jit=True)     
    bpuset.gen_bin_data(download_dir)     
    #bpuset.gen_hex_data(download_dir)     

    # Deploy
    deploy = lb2_deploy(download_dir,upload_dir)
    sender_path = "/home/test1/work/LBII_matrix/build/LBII"
    deploy.run_from_host(step=nStep,sender_path=sender_path,device_id=15)
    # deploy.run_from_driver(step=nStep,device_id=7,dmos=False)
    
    # Compare results or convert bin to npy
    check = lb2_checkRes(download_dir, upload_dir, nStep)
    check.bin2npy()
    check.npyVSnpy() 