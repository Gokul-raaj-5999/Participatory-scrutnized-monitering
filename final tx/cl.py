import time
import sqlite3
from SX127x.LoRa import *
#from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD

BOARD.setup()
BOARD.reset()
#parser = LoRaArgumentParser("Lora tester")

class mylora(LoRa):
    def __init__(self, verbose=False):
        super(mylora, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def on_rx_done(self):
        i=1
        while True:
            try:
                conn = sqlite3.connect('tx.sqlite')
                cur = conn.cursor()
                cur.execute('''SELECT detected FROM obj WHERE ind=?''',(i,))
                row=cur.fetchone()
                lst = []
                lst.append(255)
                lst.append(255)
                lst.append(0)
                lst.append(0)
                for j in row:
                    for k in j:
                        lst.append(ord(k))

                lst.append(0)
                count = 0
                tic = 65
                en = []
                en.append(255)
                en.append(255)
                en.append(0)
                en.append(0)
                for l in lst[4:-1]:
                    if(count==3):
                        en.append(tic)
                        tic+=1
                        count=0
                    en.append(l+3)
                    count+=1
                en.append(0)
                i+=1
                cur.close()
                print ("Send detected messages:",en)
                self.write_payload(en) # Send DATA RASPBERRY PI
                self.set_mode(MODE.TX)
                time.sleep(2)
                self.reset_ptr_rx()
                self.set_mode(MODE.RXCONT)
            except:
                j=0

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
    lora.on_rx_done()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("Exit")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("Exit")
    lora.set_mode(MODE.SLEEP)
BOARD.teardown()
