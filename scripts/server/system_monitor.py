# system_monitor
import psutil, time
interval = 0.5 # seconds between 2 tests
for i in range(int(1200/interval)): # monitoring for 20 min
	print "========================================"
	print "second %4.1f" % (interval*i),
	print "cpu_percent:",psutil.cpu_percent(interval=None, percpu=False)
	memory_vector = psutil.virtual_memory()
	print "memory_usage: available(MB): %4.4f" % (memory_vector.available/1e6), \
		"free(MB): %4.4f" % (memory_vector.free/1e6), \
		"used_percent:", memory_vector.percent # 1e6: Bytes -> MegaBytes
	time.sleep(0.5)

