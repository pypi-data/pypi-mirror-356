import os 
import sys
import numpy as np
import time

current_path = os.getcwd()
sys.path.insert(0, current_path)
from bpusdk.MatrixLib.lb2_matrix import lb2_matrix
from bpusdk.MatrixLib.lb2_checkRes import lb2_checkRes
from bpusdk.MatrixLib.lb2_deploy import lb2_deploy

np.random.seed(42)


def init_value(A_nRow,A_nCol,B_nRow,B_nCol):
    A = np.random.uniform(-2.0, 2.0, size=(A_nRow,A_nCol))
    B = np.random.uniform(-2.0, 2.0, size=(B_nRow,B_nCol))
    A[0,:] = 1
    return (A,B)


A_nRow = 8
A_nCol = 800
B_nRow = A_nRow
B_nCol = A_nCol

download_dir = f"../data6/Lb2_GEMA_{A_nRow}x{A_nCol}"
upload_dir = f"../upload6/ResLb2_GEMA_{A_nRow}x{A_nCol}"

(A,B) = init_value(A_nRow,A_nCol,B_nRow,B_nCol)
iMode = 0     #{GEMA:0, GEMPM:1, GEMM:2}

# # GenData
matrix = lb2_matrix(A,B,iMode)
# riscV_dir = "/home/test2/work/Riscv-gcc-tool"
riscV_dir =  "/home/gdiist/work/Riscv-gcc-tool"
matrix.gen_bin_file(download_dir,riscV_dir)

# # # Deploy
#sender_path = "~/work/LBII/build/LBII"
sender_path = "/home/gdiist/work/git/LBII_matrix/build/LBII"
deploy = lb2_deploy(download_dir,upload_dir)
deploy.run(sender_path=sender_path,device_id=0,saveAB=False,run=True)

# CheckData
t0 = time.time()
check = lb2_checkRes(download_dir, upload_dir)
# check.bin2npy_ABC()
check.bin2npy_GEMA(saveAB=False)
t1 = time.time()
print(f'CheckData finished. Time cost: {t1-t0:.2f} s')

