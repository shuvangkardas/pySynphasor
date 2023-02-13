import os
import sys
from pySynphasor.synphasor import *
import pySynphasor.pdc


class pyPDC:
    workerList = []
    def __init__(self,pmu):
        self.id = pmu["id"]
        self.ip = pmu["ip"]
        self.port = pmu["port"]
        self.pdcObj = pdc.Pdc(pdc_id=self.id, pmu_ip=self.ip,
                             pmu_port=self.port)
        self.worker = None
        self.header = None
        self.cfg = None
    def connect(self):
        self.pdcObj.run()
        # self.header = self.pdcObj.get_header()
        _,rawdata = self.pdcObj.get_config()
        self.cfg = synphasor(rawdata)
        self.cfg.show()
        
        # self.pdcObj.start()
    def data_loop(self):
        self.pdcObj.start()  # Request to start sending measurements
        
        while True:
            dataObj,rawPkt = self.pdcObj.get()
            print("<---------------Synphasor Data--------------->")
            set_cfg_data(self.cfg)
            pkt = synphasor(rawPkt)
            # pkt.show()
            print("ID Code: %d, soc: %d, fracsec: %d " %(pkt["synphasor"].idcode,pkt["synphasor"].soc,pkt["synphasor"].fracsec))
            if synphasor_data in pkt:
                data = pkt['synphasor_data']
                data.show()
                # for phasorPkt in data.pmu_data:
                #     # print(data.pmu_data[0].phasors)
                #     print(phasorPkt.phasors)
            # pkt.show()
            if not dataObj:
                self.pdcObj.quit() #close connection  
    def get_data(self):
        self.worker = threading.Thread(target=self.data_loop,daemon=True)
        # self.worker.start()
        # self.worker.join()
        MyPDC.workerList.append(self.worker)
    
    @classmethod 
    def start_pdc(cls): # class method takes cls as a first parameter
        for w in cls.workerList:
            w.start()
        for w in cls.workerList:
            w.join()