
import time
from SX127x.LoRa import *
#from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
import sqlite3
from datetime import datetime

import RPi.GPIO as GPIO
import time
#------------------------------------------------
# Define GPIO to LCD mapping
LCD_RS = 21
LCD_E  = 20
LCD_D4 = 16
LCD_D5 = 26
LCD_D6 = 19
LCD_D7 = 13
LED_ON = 15

# Define some device constants
LCD_WIDTH = 20    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005


def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
  GPIO.output(LCD_RS, mode) # RS
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
  # Toggle 'Enable' pin
  lcd_toggle_enable()
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
  # Toggle 'Enable' pin
  lcd_toggle_enable()

def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

def lcd_string(message,line,style):
  # Send string to display
  # style=1 Left justified
  # style=2 Centred
  # style=3 Right justified
  if style==1:
    message = message.ljust(LCD_WIDTH," ")
  elif style==2:
    message = message.center(LCD_WIDTH," ")
  elif style==3:
    message = message.rjust(LCD_WIDTH," ")
  lcd_byte(line, LCD_CMD)
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def lcd_backlight(flag):
  # Toggle backlight on-off-on
  GPIO.output(LED_ON, flag)
#----------------------------------------------------------------------------

def number_plate(nplate):
    GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
    GPIO.setup(LCD_E, GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT) # RS
    GPIO.setup(LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7
    GPIO.setup(LED_ON, GPIO.OUT) # Backlight enable
    # Initialise display
    lcd_init()
    # Toggle backlight on-off-on
    lcd_backlight(True)
    time.sleep(0.5)
    lcd_backlight(False)
    time.sleep(0.5)
    lcd_backlight(True)
    time.sleep(0.5)
    # Send some centred test
    #lcd_byte(0x01, LCD_CMD)

    statecode=nplate[:2]
    distno=nplate[2:4]
    rando=nplate[4:6]
    plateno=nplate[6:10]
    conn = sqlite3.connect('rx.sqlite')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS registered_vehicles(state TEXT,dist INT,ran TEXT,plateno TEXT) ''')
    row = cur.fetchone()
    a="NO"
    cur.execute('SELECT * FROM registered_vehicles WHERE state=(?) AND dist=(?) AND ran=(?) AND plateno=(?)',(statecode,distno,rando,plateno))
    for i in cur:
        a=i
    b="nplate: "+nplate
    lcd_string(b,LCD_LINE_3,2)
    if(a=="NO"):
        print("Vehicle Number Not Registered")
        lcd_string("code red",LCD_LINE_1,2)
        lcd_string("Vehicle Not Registered",LCD_LINE_4,2)
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
    GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
    GPIO.setup(LCD_E, GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT) # RS
    GPIO.setup(LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7
    GPIO.setup(LED_ON, GPIO.OUT) # Backlight enable
    # Initialise display
    lcd_init()
    # Toggle backlight on-off-on
    lcd_backlight(True)
    time.sleep(0.5)
    lcd_backlight(False)
    time.sleep(0.5)
    lcd_backlight(True)
    time.sleep(0.5)
    # Send some centred test
    #lcd_byte(0x01, LCD_CMD)
    conn = sqlite3.connect('rx.sqlite')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS object_detect(time TEXT,Object TEXT,Accuracy INT) ''')
    row = cur.fetchone()
    print(objec,'  ',acc,'  ',datetime.now())
    a=str(objec)+' '+str(acc)
    if objec in ["gun","sword","knife","pistol"]:
        lcd_string("code red",LCD_LINE_1,2)
        lcd_string(a,LCD_LINE_2,2)
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
