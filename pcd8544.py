import time
from micropython import const
import framebuf

# Registry a příkazy řadiče PCD8544
PCD8544_FUNCTIONSET = const(0x20)
PCD8544_POWERDOWN = const(0x04)
PCD8544_ENTRYMODE = const(0x02)
PCD8544_EXTENDEDINSTRUCTION = const(0x01)
PCD8544_DISPLAYCONTROL = const(0x08)
PCD8544_DISPLAYBLANK = const(0x00)
PCD8544_DISPLAYNORMAL = const(0x04)
PCD8544_DISPLAYALLON = const(0x01)
PCD8544_DISPLAYINVERTED = const(0x05)
PCD8544_SETYADDR = const(0x40)
PCD8544_SETXADDR = const(0x80)

class PCD8544:
    def __init__(self, spi, dc, cs, rst):
        self.spi = spi
        self.dc = dc
        self.cs = cs
        self.rst = rst
        self.width = 84
        self.height = 48
        
        # Buffer pro monochromatický displej (84x48 pixelů = 504 bajtů)
        self.buffer = bytearray((self.height // 8) * self.width)
        
        # Architektonická oprava: Inicializace framebufferu trvale v paměti
        self.fbuf = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        
        # Hardwarová inicializace
        self.init()

    def write_cmd(self, cmd):
        self.dc.value(0) # Režim příkazů
        self.cs.value(0)
        self.spi.write(bytearray([cmd]))
        self.cs.value(1)

    def init(self):
        # 1. Agresivnější hardwarový reset pro čínské klony
        self.rst.value(1)
        time.sleep_ms(20)
        self.rst.value(0)
        time.sleep_ms(100) # Podržení resetu dole pro vybití kondenzátorů
        self.rst.value(1)
        time.sleep_ms(100) # Čas na stabilizaci interního generátoru napětí
        
        # 2. Kompletní inicializační sekvence řadiče (včetně vynucení H=1 stavu)
        self.write_cmd(PCD8544_FUNCTIONSET | PCD8544_EXTENDEDINSTRUCTION) # 0x21
        self.write_cmd(0x90) # Bezpečnější operační napětí (Vop) pro červené moduly
        self.write_cmd(0x04) # Teplotní koeficient
        self.write_cmd(0x14) # Bias systém 1:48
        
        # 3. Návrat do standardního režimu a aktivace displeje
        self.write_cmd(PCD8544_FUNCTIONSET) # 0x20 (Přepnutí H zpět na 0)
        self.write_cmd(PCD8544_DISPLAYCONTROL | PCD8544_DISPLAYNORMAL) # 0x0C
        
        # Vyčištění displeje po startu, aby na něm nezůstal náhodný šum
        self.fill(0)
        self.show()

    def text(self, string, x, y, color=1):
        # Odstraněna paměťová alokace při každém volání, kreslí se rovnou přes stálý fbuf
        self.fbuf.text(string, x, y, color)

    def fill(self, color):
        # Přímé využití optimalizovaného C-kódu z framebuf místo pomalého for-cyklu
        self.fbuf.fill(color)

    def show(self):
        self.write_cmd(PCD8544_SETYADDR) # Reset řádkového čítače na 0
        self.write_cmd(PCD8544_SETXADDR) # Reset sloupcového čítače na 0
        self.dc.value(1) # Režim dat
        self.cs.value(0)
        self.spi.write(self.buffer)
        self.cs.value(1)