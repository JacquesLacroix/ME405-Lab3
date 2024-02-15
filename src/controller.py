import encoder_reader
import motor_driver
import utime

class Controller:

    def __init__(self, encoder, motor, setpoint, kp):
        self.encoder = encoder
        self.motor = motor
        self.set_setpoint(setpoint)
        self.set_kp(kp)
        self.times = []
        self.positions = []
        
    def run(self):
        PWM = self.kp*(self.setpoint - self.encoder.read())
        self.motor.set_duty_cycle(PWM)
        self.positions.append(self.encoder.read()) 
        self.times.append(utime.ticks_ms())
        return PWM
    
    def set_setpoint(self, setpoint):
        self.setpoint = setpoint
        
    def set_kp(self, kp):
        self.kp = kp
        
    def print_list(self, start):
        for i in range(len(self.times)):
            print(f"{(self.times[i] - start):d}, {self.positions[i]:d}")
        self.times = []
        self.positions = []
    
if __name__ == "__main__":
    
    pinC1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
    pinA0 = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP) 
    pinA1 = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
    
    pinC6 = pyb.Pin(pyb.Pin.board.PC6, pyb.Pin.OUT_PP) 
    pinC7 = pyb.Pin(pyb.Pin.board.PC7, pyb.Pin.OUT_PP)
    
    tim5 = pyb.Timer(5, freq=20000)   #Motor Controller Timer 
    tim8 = pyb.Timer(8, prescaler=1, period=65535)
    
    motor = motor_driver.MotorDriver(pinC1, pinA0, pinA1, tim5)
    encoder = encoder_reader.Encoder(pinC6, pinC7, tim8)
    
    setpoint = 1600
    
    controller = Controller(encoder, motor, setpoint, 1/16)
    
    while True:
        
        kp = input("ENTER KP VALUE: ")
        try:
            kp = float(kp)
        except:
            print("KP MUST BE NUMBER, DUMB DUMB")
            continue
        
        controller.set_kp(kp)
        encoder.zero()
        
        startticks = utime.ticks_ms()
        
        while not abs(controller.run()) < 10:        
            utime.sleep_ms(10)
        
        controller.print_list(startticks)