from IoTPy.core.gpio import GPIOProducer
from IoTPy.core.i2c import I2CProducer
from IoTPy.core.spi import SPI, SPIProducer
from IoTPy.core.adc import ADCProducer
from IoTPy.core.pwm import PWM_Producer
from IoTPy.atmel.gpio import AtmelGPIO
from IoTPy.atmel.spi import AtmelSPI
from IoTPy.atmel.adc import AtmelADC
from IoTPy.atmel.pwm import AtmelPWM
from IoTPy.linux.i2c import LinuxI2C

class AtmelBoard(GPIOProducer, SPIProducer, I2CProducer, ADCProducer, PWM_Producer):

	gpio_names = [1, 11, 12, 15, 16, 17, 18, 19, 20, 21, 22, 23]
	spi_cs_names = [0, 1]
	adc_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	pwm_names = ['1', '2', '3', '4']
	SPIDEV_NUM = 32765

	def __init__(self):
		pass

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		pass

	def GPIO(self, name, *args, **kwargs):
		if name not in self.gpio_names:
			raise ValueError("Invalid GPIO name %s. Must be one of %s." % (name, ", ".join(self.gpio_names)))

		return AtmelGPIO(name)

	def SPI(self, name, clock=1000000, mode=SPI.MODE_0, *args, **kwargs):
		if name not in self.spi_cs_names:
			raise ValueError("Invalid SPI CS number %s. Must be one of %s." % (name, ", ".join(self.spi_cs_names)))

		return AtmelSPI(self.SPIDEV_NUM, clock, mode, cs=name)

	def I2C(self, name=0, *args, **kwargs):
		if isinstance(name, int):
			name = "/dev/i2c-%d" % name

		return LinuxI2C(name)
		
	def ADC(self, name, *args, **kwargs):
		if name not in self.adc_names:
			raise ValueError("Invalid ADC number %s. Must be one of %s." % (name, ", ".join(self.adc_names)))

		return AtmelADC(name)
	
	def PWM(self, name, freq=1000, polarity=1, *args, **kwargs):
		if name not in self.pwm_names:
			raise ValueError("Invalid PWM number %s. Must be one of %s." % (name, ", ".join(self.pwm_names)))

		return AtmelPWM(name, freq, polarity)


