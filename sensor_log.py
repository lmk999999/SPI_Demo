import spidev           #宣告並引用 spidev 函式
import time             #宣告並引用時間函式

spi = spidev.SpiDev()
#將 spi 指到 spidev 的方法，以方便後續操作

spi.open(0,0)
#將 spi 開啟
spi.max_speed_hz = 1000000
#設定 spi 讀取最大頻率，沒有設置的話數值永遠是 0

def readadc(input_ch = 7):
        ch = 7
        if ch > 7 or ch < 0:    #設定頻道讀取的上下限
                return -1
        rst = spi.xfer2([1, (8 + ch) << 4, 0])
        adcout = ((rst[1] & 0x03) << 8) + rst[2]
        return adcout   #回傳 adcout 也就是實際值

while True:             #建立迴圈重複讀取
        for i in range(0,7):    #瀏覽頻道，此處設定是瀏覽 0、1 兩個頻道
                print("Ch " + str(i) + " = " + str(readadc(i)))
                #透過剛剛建立的 readadc() 方法去列印各頻道的結果
        time.sleep(1)
        #延遲一秒在讀取減輕電腦負擔
