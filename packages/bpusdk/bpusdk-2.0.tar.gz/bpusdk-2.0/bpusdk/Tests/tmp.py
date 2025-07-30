
import math

def get_blocksize_n(var1,var2):
    nNumMax = (1280+128)*1024/4
    var3 = (nNumMax-var1*var2)/(var1+var2)
    var3 = 8*math.floor(var3/8)
    return var3

var3 = get_blocksize_n(8,8)
print(var3)