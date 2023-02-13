import sys
import os

# if 'sPDC' in sys.modules:  
#     del sys.modules["sPDC"]

# pdcpath = os.path.abspath('../../PDC')
# sys.path.append(pdcpath)
from sPDC  import MyPDC


if __name__=="__main__":
    try:
        pmuInfo = {"id": 7, "ip" :"10.0.2.4","port": 4712}
        pdc1 = MyPDC(pmuInfo)
        pdc1.connect()
        pdc1.get_data()
        MyPDC.start_pdc()
    except KeyboardInterrupt:
        print("interrupted")