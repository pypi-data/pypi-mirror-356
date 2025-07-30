import time
import warnings
import random
import brainpy.math as bm
import jax
import numpy as np
from loguru import logger
import os 
import sys

current_path = os.getcwd()
sys.path.insert(0, current_path)
from bpusdk.Models.Emodel_lb1_int8  import ENet_V3, createConn
from bpusdk.BrainpyLib.lb1_SNN import ASIC_SNN, ModelRun
from bpusdk.BrainpyLib.Common import gen_v2

warnings.filterwarnings("ignore")

# @click.command()
# @click.argument('download_dir')
def test(gen_net = False):
    t0 = time.time()
    label_list = []
    time_list = []

    random.seed(42)
    np.random.seed(42)
    bm.random.seed(42)
    scope = 96 * 8
    groupN = scope * 1024
    group_num = groupN
    download_dir = "./tmp"
    fanOut = 2
    groupSize = 8
    spk_ranges = 1.6
    key = jax.random.PRNGKey(1)

    # scope = 2**scope
    neuronScale, T = 1, 100

    download_dir = rf'../../data/ei_data_{scope}k_{neuronScale}'
    upload_dir = rf'../../upload/xdma0/ei_{scope}k_asic'
    bm.set_dt(1.)

    if gen_net is True:
        pre_list, post_list = createConn(groupN, fanOut, groupSize)
        # pre_list = np.load(r".\pre_list.npy")
        # post_list = np.load(r".\post_list.npy")


        net = ENet_V3(groupN, pre_list=pre_list,
                    post_list=post_list, method='exp_auto')
        x = bm.where(jax.random.normal(key, shape=(
            min(16384, group_num),)) >= spk_ranges, 1, 0)
        I = np.zeros((1, group_num))
        I[0][:min(16384, group_num)] = x

        # mode 0,1,2 = no file saved, save spike, save all
        t1 = time.time()
        logger.info('Initial Brainpy Network. Elapsed: %.2f s\n' % (t1 - t0))  # 输出
        label_list.append("Init Brainpy")
        time_list.append(t1 - t0)

        config_dir = './HardwareConfig/Config_40nmASIC_INT8.yaml'
        bpuset = ASIC_SNN(net, I, 0, config_file=config_dir)
        bpuset.gen_bin_data(download_dir)
    download_dir, upload_dir = gen_v2(base=scope, scale=neuronScale, para_max=6, cp_max=24)
    # bpuset.run_test_int(tile_num=6*1, row=6, col=1, step_num=T, mode=1, download_dir=download_dir, upload_dir=upload_dir, reset=True)
    m = ModelRun(tile_num=6*24, row=6, col=24, step_num=T, loadPath=download_dir, uploadPath=upload_dir)
    m.deploy()
    m.simu()



if __name__ == "__main__":
    test()
