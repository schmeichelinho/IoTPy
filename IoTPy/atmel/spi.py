import ctypes
from fcntl import ioctl
import struct
import array
from IoTPy.core.spi import SPI
from IoTPy.linux.ioctl_def import IOW


class AtmelSPI(SPI):
	SPI_IOC_MAGIC = ord('k')
	SPI_IOC_MESSAGE = IOW(SPI_IOC_MAGIC, 0, 32)
	SPI_IOC_WR_MODE = IOW(SPI_IOC_MAGIC, 1, 1)
	SPI_IOC_WR_BITS_PER_WORD = IOW(SPI_IOC_MAGIC, 3, 1)
	SPI_IOC_WR_MAX_SPEED_HZ = IOW(SPI_IOC_MAGIC, 4, 4)

	def __init__(self, spidev, clock, mode, cs):
		self.name = '/dev/spidev%d.%d' % (spidev, cs)
		self.clock = clock
		self.mode = mode

	def __enter__(self):
		try:
			self._file = open(self.name, "w+")
		except IOError:
			warn("Could not open the desired spidev.")
		try:
			ioctl(self._file, SPI_IOC_WR_MODE, self.mode, True)
			ioctl(self._file, SPI_IOC_WR_BITS_PER_WORD, 8, True)
			ioctl(self._file, SPI_IOC_WR_MAX_SPEED_HZ, self.clock, True)
		except:
			raise RuntimeError("Error while setting up the SPI.")
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self._file.close()
        
	def read(self, count, value=0):
		return self._file.read(count)

	def write(self, data):
		self._file.write(data)
		self._file.flush()

	def transaction(self, data_out):
		size = len(data_out)
		buf = ctypes.c_buffer(data_out, size)

		txfer = struct.pack("@QQIIHBBxxxx", ctypes.addressof(buf), ctypes.addressof(buf), size, 0, 0, 8, 0)
		txfer = array.array('b', txfer)

		try:
			ioctl(self._file, SPI_IOC_MESSAGE, txfer, True)
		except:
			raise RuntimeError("Error while performing SPI transaction.")

		return ctypes.string_at(buf, size)
