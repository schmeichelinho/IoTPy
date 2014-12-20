from IoTPy.core.pwm import PWM

class AtmelPWM(PWM):
	def __init__(self, name, freq, polarity):
		self.name = name
		self.period = int(round(1e9/freq))
		self.polarity = polarity

	def __enter__(self):
		with open("/sys/class/pwm/pwmchip0/export", 'w') as export:
		    export.write("%s" % self.name)
		    export.flush()
		
		self._enable = open("/sys/class/pwm/pwmchip0/pwm%s/enable" % self.name, 'w+')
		self._enable.write('0')
		self._enable.flush()
		    
		with open("/sys/class/pwm/pwmchip0/pwm%s/polarity" % self.name, 'w') as polarity:
		    polarity.write('normal' if self.polarity else 'inversed')
		    polarity.flush()

		self._period = open("/sys/class/pwm/pwmchip0/pwm%s/period" % self.name, 'w')
		self._duty_cycle = open("/sys/class/pwm/pwmchip0/pwm%s/duty_cycle" % self.name, 'w')
		self.set_period(self.period/1000)
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self._enable.write('0')
		self._enable.flush()
		self._period.close()
		self._duty_cycle.close()
		self._enable.close()
		with open("/sys/class/pwm/pwmchip0/unexport", 'w') as unexport:
		    unexport.write("%s" % self.name)
		    unexport.flush()       

	def set_frequency(self, freq):
		self.set_period(int(round(1e6/freq)))

	def set_period(self, period_us):
		self.period = period_us * 1000
		self._enable.write('0')
		self._enable.flush()
		self._period.write("%s" % str(self.period))
		self._period.flush()
		self._enable.write('1')
		self._enable.flush()

	def set_duty_cycle(self, duty_cycle):
		if duty_cycle > 100:
			raise ValueError("Duty cycle value should be between 0 and 100.")
		self._duty_cycle.write("%s" % str(int(round(self.period * float(duty_cycle/100.0)))))
		self._duty_cycle.flush()

	def set_pulse_time(self, pulse_us):
		pulse_ns = pulse_us * 1000
		if pulse_ns > self.period:
				raise ValueError("Pulse cannot be longer than the period.")
		if self.polarity:
			self._duty_cycle.write("%s" % str(pulse_ns))
		else:
			self._duty_cycle.write("%s" % str(self.period - pulse_ns))
		self._duty_cycle.flush()

