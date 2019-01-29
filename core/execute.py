import sys, os
import subprocess
# from core import utils
import queue

from . import messages
from . import utils


class ProcessQueue():
    """docstring for ProcessQueue"""
    def __init__(self, options):
        self.options = options
        self.q = queue.Queue()

    #put process to queue
    def put_cmd_to_queue(self, process_item):
        cmd = process_item['cmd']
        process = utils.run_as_background(cmd)

        process_item['process'] = process
        self.q.put(process_item)

    #if the task was done create a status message
    def pop_to_check(self):

        process_item = self.q.get()

        if self.alive(process_item):
            self.done(process_item)
        self.q.task_done()



    #checking if process is still running or not
    def alive(self, process_item):
        process = process_item['process']

        if process.poll() is None:
            # print("put it back")
            self.q.put(process_item)
            return False
        else:
            return True

    #create report message or status message
    def done(self, process_item):
        utils.print_good('Done some command')

        if process_item['out'] != '':
            #send attach message
            sm = messages.Messages(self.options)
            mess = {
                'author_name' : 'Command Done with Output',
                'title' : process_item['cmd'],
                'content' : process_item['out'],
            }
            sm.send_info(mess)


            #send snippet message
            sm = messages.Messages(self.options)
            mess = {
                'filename' : process_item['out'],
                # 'filename' : process_item['out'],
                'title' : process_item['out']
            }
            sm.send_file(mess)

        else:
            #send attach message
            output = process_item['process'].stdout.read().decode("utf-8")
            sm = messages.Messages(self.options)
            mess = {
                'channel' : 'CFSTHB3K9',
                'author_name' : 'Command Done',
                'title' : process_item['cmd'],
                'content' : output
            }
            sm.send_info(mess)
            

        #create message


















