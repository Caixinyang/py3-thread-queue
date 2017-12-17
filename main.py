import sys, os, threading, time, random, queue

class RunThread(threading.Thread):
    
	def __init__(self, name, thread_mutex, thread_queue = None):
		threading.Thread.__init__(self)
		self.name = name
		
		self.thread_queue = thread_queue
		if self.thread_queue != None:
			self.thread_queue.put(self)
			print("添加了" + self.name + "线程到列队")
		
		self.thread_mutex = thread_mutex
		
	def run(self):
		
		time.sleep(random.uniform(1, 3))
		
		if self.thread_mutex.acquire(10):
			print(self.name + ' 执行完成!')			
			self.thread_mutex.release()
		
		if self.thread_queue != None:
			#向任务已经完成的队列发送一个信号
			self.thread_queue.task_done()
	
if __name__ == "__main__":	
	
	#运行线程数
	thread_count = 100
	
	thread_mutex = threading.Lock()
	
	thread_queue = queue.Queue()
	for i in range(0, thread_count):
		t = RunThread("thread_" + str(i), thread_mutex, thread_queue)
		t.start()
	
	thread_queue.join()
	print("全部列队执行完成")
	