import machine
import pcd8544
import time

# 1. Softwarová emulace SPI – fiktivní miso pin zůstává na GP20 (nezapojuje se)
spi = machine.SoftSPI(baudrate=2000000, polarity=0, phase=0, sck=machine.Pin(18), mosi=machine.Pin(19), miso=machine.Pin(20))

# 2. Ovládací piny srovnané s tvým přímým zapojením
dc = machine.Pin(12)    # DC -> Máš fyzicky na GP12
cs = machine.Pin(17)    # CE -> GP17
rst = machine.Pin(11)   # RST -> GP11

# 3. Inicializace displeje
lcd = pcd8544.PCD8544(spi, dc, cs, rst)

# 4. Hrubý test paměti: Horní polovina černá, spodní čistá
for i in range(252):
    lcd.buffer[i] = 0xFF

for i in range(252, 504):
    lcd.buffer[i] = 0x00

lcd.show()