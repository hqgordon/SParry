# pip install nvidia-ml-py3
import pycuda.autoinit
import pycuda.driver as drv
from pynvml import *

class Device(object):
	"""
	function: get the GPU device infomation, get the type and attributes.

	parameters: None.

	attributes:
		device: a pyCUDA device class.
		CUDAVersion: the version of CUDA.
		driverVersion: the version of CUDA driver.
		deviceNum: the number of valid GPU device.
		deviceName: the name of the device.
		globalMem: the max number of the global memory.
		sharedMem: the max number of the shared memory.
		processNum: the number of processors.
		freeMem: the bytes of free memory.
		temperature: the temperature of the device.
		powerStstus: the power ststus of the device.

	return Device object.
	"""
	def __init__(self):
		self.device = drv.Device(0) # pycuda 的 device 类

		self.CUDAVersion = None # 编译 pyCUDA CUDA 的版本
		self.driverVersion = None # 运行 CUDA 的驱动的版本
		
		self.deviceName = None # gpu 设备的型号
		self.deviceNum = None # CUDA 设备的数量
		self.globalMem = None # global memory 的容量
		self.sharedMem = None # shared memory 的容量
		self.processNum = None # 处理器的数量

		self.SMNum = None # SM 的数量
		self.gridSize = None # 一个元组 grid 分别表示 grid 两个方向是最大值
		self.blockSize = None # 同上 block 的三个方向的最大值

		self.total = None # GPU 中的显存总容量 单位是 Byte
		self.free = None # GPU 中的目前剩余总量
		self.used = None # 已经使用了的显存
		self.temperature = None # 温度
		self.powerStstus = None # 电源状态

		self.getDeviceInfo()

	def get_device_type(self):
		"""
		get the device name
		"""

		if self.deviceName == None:
			self.deviceName = self.device.name()
		
		return self.deviceName

	def get_number_of_device(self):
		"""
		get the number of CUDA devices found
		"""

		if self.deviceNum == None:
			self.deviceNum = self.device.count()
	
	def get_version(self):
		"""
		Obtain the version of CUDA against which PyCuda was compiled. 
		Returns a 3-tuple of integers as (major, minor, revision).
		"""
		if self.CUDAVersion == None:
			self.CUDAVersion = drv.get_version()
		
		return self.CUDAVersion
	
	def get_driver_version(self):
		"""
		Obtain the version of the CUDA driver on top of which PyCUDA is running. 
		Returns an integer version number.
		"""
		if self.driverVersion == None:
			self.driverVersion = drv.get_driver_version()
		
		return self.driverVersion
	
		"""
		Obtain the version of the CUDA driver on top of which PyCUDA is running. 
		Returns an integer version number.
		"""
		if self.driverVersion == None:
			self.driverVersion = drv.get_driver_version()
		
		return self.driverVersion
	
	def getDeviceInfo(self):
		"""
		获取设备的信息, 并返回 deviceinfo 的类
		"""	

		# 初始化
		nvmlInit()

		# 驱动信息
		nvmlSystemGetDriverVersion()

		#查看设备名字
		self.deviceNum = nvmlDeviceGetCount()
		self.deviceType = []

		for i in range(self.deviceNum):
			handle = nvmlDeviceGetHandleByIndex(i)
			self.deviceType.append(nvmlDeviceGetName(handle))

		#查看显存、温度、风扇、电源
		handle = nvmlDeviceGetHandleByIndex(0)
		info = nvmlDeviceGetMemoryInfo(handle)

		# 单位是 Byte
		self.total = info.total
		self.free = info.free
		self.used = info.used

		self.temperature = nvmlDeviceGetTemperature(handle,0)
		self.powerStstus = nvmlDeviceGetPowerState(handle)

		#最后要关闭管理工具
		nvmlShutdown()
