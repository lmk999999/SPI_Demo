import spidev           #宣告並引用 spidev 函式
import time             #宣告並引用時間函式
import RPi.GPIO as GPIO

spi = spidev.SpiDev()
#將 spi 指到 spidev 的方法，以方便後續操作

spi.open(0,0)
#將 spi 開啟
spi.max_speed_hz = 1000000
#設定 spi 讀取最大頻率，沒有設置的話數值永遠是 0

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

pwm_list = []

for i in range(2,5):
        GPIO.setup(i, GPIO.OUT)
        pwm_list.append(GPIO.PWM(i, 200))
        pwm_list[i-2].start(0)


def readadc(input_ch = 7):
        ch = input_ch
        if ch > 7 or ch < 0:    #設定頻道讀取的上下限
                return -1
        rst = spi.xfer2([1, (8 + ch) << 4, 0])
        adcout = ((rst[1] & 0x03) << 8) + rst[2]
        return adcout   #回傳 adcout 也就是實際值

channel_i = 7
led_level = 0

while True:             #建立迴圈重複讀取
        light_value = readadc(channel_i)
        #light_value = int(float(light_value)/10.0)*10
        #led_level = 3
        led_level = 3-((float(light_value)-20)/200.0)
        if   led_level < 0.0 : led_level = 0.0
        elif led_level > 3.0 : led_level = 3.0

        for i in range(1,4):
                if   led_level <= i-1 : pwm_list[i-1].ChangeDutyCycle(0)
                elif led_level <  i   :
                        setting_level = int(led_level*100)%100
                        if setting_level < 1 : pwm_list[i-1].ChangeDutyCycle(0)
                        else : pwm_list[i-1].ChangeDutyCycle(setting_level)
                elif led_level >= i   : pwm_list[i-1].ChangeDutyCycle(100)

        print("light level = {} , led level = {:.2f}".format(light_value,led_level),end="\r",flush=False)
        #time.sleep(1)
        #延遲一秒在讀取減輕電腦負擔

