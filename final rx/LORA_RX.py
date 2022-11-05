
import time
from SX127x.LoRa import *
#from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
import sqlite3
from datetime import datetime

def number_plate(nplate):
    statecode=nplate[:2]
    distno=nplate[2:4]
    rando=nplate[4:6]
    plateno=nplate[6:10]
    conn = sqlite3.connect('rx.sqlite')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS registered_vehicles(state TEXT,dist INT,ran TEXT,plateno TEXT) ''')
    row = cur.fetchone()
    a="NO"
    cur.execute('SELECT * FROM registered_vehicles WHERE state,dist,ran,plateno=(?,?,?,?)',(statecode,distno,rando,plateno))
    for i in cur:
        a=i
    if(a=="NO"):
        print("Vehicle Number Not Registered")
    conn = sqlite3.connect('rx.sqlite')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS number_plate(time TEXT,state TEXT,dist INT,ran TEXT,plateno TEXT) ''')
    row = cur.fetchone()
    print(statecode,distno,' ',rando,plateno,'  ',datetime.now())
    print("ENTERING NUMBERPLATE IN DATABASE")
    cur.execute('INSERT INTO number_plate (time,state,dist,ran,plateno) VALUES (?, ?, ?, ?, ?)', (datetime.now(),statecode,distno,rando,plateno))
    conn.commit()
    cur.close()

def object_detection(objec,acc):
    conn = sqlite3.connect('rx.sqlite')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS object_detect(time TEXT,Object TEXT,Accuracy INT) ''')
    row = cur.fetchone()
    print(objec,'  ',acc,'  ',datetime.now())
    print("ENTERING THE OBJECT DETECTED IN DATABASE")
    cur.execute('INSERT INTO object_detect (time,object,accuracy) VALUES (?, ?, ?)', (datetime.now(),objec,acc))
    conn.commit()
    cur.close()

BOARD.setup()
BOARD.reset()
#parser = LoRaArgumentParser("Lora tester")


class mylora(LoRa):
    def __init__(self, verbose=False):
        super(mylora, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.var=0

    def on_rx_done(self):
        BOARD.led_on()
        #print("\nRxDone")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        print ("Receive: ",payload)
        print(bytes(payload).decode("utf-8",'ignore')) # Receive DATA
        BOARD.led_off()
        time.sleep(2) # Wait for the client be ready
        dec = []
        dec.append(255)
        dec.append(255)
        dec.append(0)
        dec.append(0)
        count = 0
        for i in payload[4:-1]:
            if (count!=3):
                dec.append(i-3)
                count+=1
            else:
                count = 0
        dec.append(0)
        print("dec: ",dec)
        mens=bytes(dec).decode("utf-8",'ignore')
        print ("Received decryted message:",mens)
        ls=mens.split()
        prob=0
        #ls=["  nplHR26AT1234"]
        for i in ls:
            i.lstrip()
            i.rstrip()
            print(i[2:5])
            if(i[2:5]=='npl'):
                print("numplate received")
                nplate=i[5:]
                number_plate(nplate)

            if(prob==1):
                print("calling object_detect")
                pro=i[2:4]
                pro=int(pro)
                objec=detect
                acc=int(pro)
                object_detection(objec,acc)
                prob=0
            if(i[2:5]=='obj'):
                print("obj received")
                detect=i[5:-1]
                prob=1
        print("completed")


    def on_tx_done(self):
        print("\nTxDone")
        print(self.get_irq_flags())

    def on_cad_done(self):
        print("\non_CadDone")
        print(self.get_irq_flags())

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())

    def on_valid_header(self):
        print("\non_ValidHeader")
        print(self.get_irq_flags())

    def on_payload_crc_error(self):
        print("\non_PayloadCrcError")
        print(self.get_irq_flags())

    def on_fhss_change_channel(self):
        print("\non_FhssChangeChannel")
        print(self.get_irq_flags())

    def start(self):
        while True:
            while (self.var==0):
                self.reset_ptr_rx()
                self.set_mode(MODE.RXCONT) # Receiver mode

                start_time = time.time()
                while (time.time() - start_time < 10): # wait until receive data or 10s
                    pass;

            self.var=0
            self.reset_ptr_rx()
            self.set_mode(MODE.RXCONT) # Receiver mode
            time.sleep(10)

lora = mylora(verbose=False)
#args = parser.parse_args(lora) # configs in LoRaArgumentParser.py

#     Slow+long range  Bw = 125 kHz, Cr = 4/8, Sf = 4096chips/symbol, CRC on. 13 dBm
lora.set_pa_config(pa_select=1, max_power=21, output_power=15)
lora.set_bw(BW.BW500)
lora.set_coding_rate(CODING_RATE.CR4_8)
lora.set_spreading_factor(12)
lora.set_rx_crc(True)
#lora.set_lna_gain(GAIN.G1)
#lora.set_implicit_header_mode(False)
lora.set_low_data_rate_optim(True)

#  Medium Range  Defaults after init are 434.0MHz, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on 13 dBm
#lora.set_pa_config(pa_select=1)


assert(lora.get_agc_auto_on() == 1)

try:
    print("START")
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("Exit")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("Exit")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
