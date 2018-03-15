# system_monitor
import psutil, time
for i in range(2000):
	print "second %4.1f" % (0.5*i),
	print "cpu_percent:",psutil.cpu_percent(interval=None, percpu=False)
	memory_vector = psutil.virtual_memory()
	print "memory_usage: available(MB): %4.4f" % (memory_vector.available/1e6), \
		"free(MB): %4.4f" % (memory_vector.free/1e6), \
		"used_percent:", memory_vector.percent # 1e6: Bytes -> MegaBytes
	time.sleep(0.5)

