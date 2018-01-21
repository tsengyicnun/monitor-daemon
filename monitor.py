import sys
import time
import commands
import os
import json

from daemon import Daemon

log_path = "/var/log/hcc2/"
all_mem_log = "memall.log"
proc_mem_log = "memproc.log"
swap_log = "swap.log"
io_log = "iostat.log"

class monitorMemory(object):
    def run(self):
        if os.path.exists(log_path) is False:
            os.makedirs(log_path)
        memlog_fs = open(log_path+all_mem_log,'a',0)
        swaplog_fs = open(log_path+swap_log,'a',0)
        iolog_fs = open(log_path+io_log,'a',0)
        if os.stat(log_path+all_mem_log).st_size == 0:
            memstatus=commands.getoutput("free -m | grep total")
            memlog_fs.write(memstatus+"\n")
        if os.stat(log_path+swap_log).st_size == 0:
            swapstatus=commands.getoutput("free -m | grep total")
            swaplog_fs.write(swapstatus+"\n")
        if os.stat(log_path+io_log).st_size == 0:
            iostatus=commands.getoutput("iostat /dev/sda | grep Device:")
            iolog_fs.write(iostatus+"\n")
        while True:
            out=commands.getoutput("date +\"%Y %m-%d, %H:%M:%S\">> " +log_path+proc_mem_log)
            out=commands.getoutput("ps aux | awk 'NR>1 {$5=int($5/1024/8)\"M\";}{ print $4,$3,$11}'  | sort -k1rn | head -n 10 >>" +log_path+proc_mem_log)
            curtime = commands.getoutput("date +\"%Y %m-%d, %H:%M:%S\"")
            memstatus=commands.getoutput("free -m | grep Mem")+"         "+curtime+"\n"
            swapstatus=commands.getoutput("free -m | grep Swap")+"         "+curtime+"\n"
            iostatus=commands.getoutput("iostat /dev/sda | grep sda")+"      "+curtime+"\n"
            iolog_fs.write(iostatus)
            memlog_fs.write(memstatus)
            swaplog_fs.write(swapstatus)
            time.sleep(5)
        memlog_fs.close()
        swaplog_fs.close()
        iolog_fs.close()

class Monitor(Daemon):
    def run(self):
        print"Monitor Run"
        memory_status = monitorMemory()
        memory_status.run()

if __name__ == "__main__":
    daemon = Monitor('/tmp/monitor-daemon.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print "start daemon"
            daemon.start()
        elif 'stop' == sys.argv[1]:
            print "stop daemon"
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart"
        sys.exit(2)
