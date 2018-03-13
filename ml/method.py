from scapy.all import *

from headers import Seer
from anomaly_model import AnomalyModel
from utils import *

ETH_BROADCAST = 'ff:ff:ff:ff:ff:ff'

# TODO: update with actual ethernet address of ECU
ETH_SRC = ETH_BROADCAST

class Method():
    def __init__(self, send_fn=sendp):
        self.model = AnomalyModel()
        self.load_model()
        self.send_fn = send_fn

    def load_model(self):
        try:
            self.model.load('model.pkl')
        except:
            reader = read_tcpdump_file('data/outside.tcpdump')
            packets = [f for f in featurize_packets(reader)]
            self.model.fit(packets)
            model.save('model.pkl')

    def handle_pkt(self, pkt):
        featurized_pkt = featurize_scapy_pkt(pkt)
        prediction = self.model.predict(featurized_pkt)
        ether = Ether(dst=ETH_BROADCAST, src=ETH_SRC)
        seer = Seer(malicious=prediction, data=pkt)
        self.send_fn(ether / seer)

    def run(self):
        sniff(prn=self.handle_pkt, count=0)