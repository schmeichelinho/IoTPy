from IoTPy.core.adc import ADC

class AtmelADC(ADC):
	def __init__(self, name):
		self.name = name
	
	def __enter__(self):
		self._value = "/sys/bus/iio/devices/iio:device0/in_voltage%s_raw" % self.name
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		pass

	def read(self):
		with open(self._value, 'r') as value:
			val = value.read()
		if(val):	
			return float(float(int(val)/4095.0))

	def read_raw(self):
		with open(self._value, 'r') as value:
			val = value.read()
		if(val):
			return int(val)
