'''
Created on 28/05/2012

@author: Fabio Zadrozny
'''

import threading


#===================================================================================================
# OnOutputThread
#===================================================================================================
class OnOutputThread(threading.Thread):

    FINISH_PROCESSING_ITEM = ()

    def __init__(self, output_queue, on_output):
        threading.Thread.__init__(self)
        self.output_queue = output_queue
        self.on_output = on_output
        self.setDaemon(True)


    def run(self):
        while True:
            action = self.output_queue.get(True)
            try:
                if action == self.FINISH_PROCESSING_ITEM:
                    return
                self.on_output(action)
            finally:
                self.output_queue.task_done()


#===================================================================================================
# ExecuteThreadsHandlingOutputQueue
#===================================================================================================
def ExecuteThreadsHandlingOutputQueue(threads, output_queue, on_output):
    queue_printer_thread = OnOutputThread(output_queue, on_output)

    for t in threads:
        t.start()

    queue_printer_thread.start()

    for t in threads:
        t.join()

    output_queue.put(OnOutputThread.FINISH_PROCESSING_ITEM)
    output_queue.join()
