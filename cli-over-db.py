#!/usr/bin/python
""" cli-over-db.py
Author: Kevin Dick
Date: 2018-02-08
---
Need to access a device that 
This solution comprises three elements:
1. This script: set it to run on the remote
   device inside of the Dropbox folder.
   It will read from the commands.txt file
   execute the last command if it has changed
   (i.e. been saved and synced from another location)
   and then update the screenshot.
2. commands.txt: the file which contains the commands
   you wish to run when remotely interactingwith the 
   device over Dropbox. When updated and saved, the
   Dropbox daemon will sync the new commands.txt file
   which will trigger this script to execute the new
   command.
3. results.txt: With every execution, this script will
   capture the stdout of the remote device as a 
   confirmation of the run.
"""
import os, sys
from datetime import datetime
import subprocess
from time import sleep

cmd_file = 'commands.txt'
out_file = 'output.txt'
btwn_cmd = 1
VERBOSE  = True

# Set the standard output to 
print 'Starting to read commands...'

last_cmd = ''
while True: # Run forever
    try: cmds = [line.strip() for line in open(cmd_file, 'r').readlines()]
    except: continue

    # May have overwritten the commands file
    if len(cmds) == 0: continue

    if VERBOSE: print cmds
    if not cmds[-1] == last_cmd:
        last_cmd = cmds[-1]
        
        if VERBOSE: print datetime.now().strftime("%Y/%m/%d-%H:%M:%S") + '/nRunning ' + last_cmd
	with open(out_file, 'a') as f: f.write(datetime.now().strftime("%Y/%m/%d-%H:%M:%S") + 
					      '\nRunning: ' + last_cmd)
        # Run the process 
        p = subprocess.Popen(last_cmd, stdout=subprocess.PIPE, shell=True)
        (out, err) = p.communicate()
        p_status = p.wait()

        with open(out_file, 'a') as f: f.write('\n' + '-' * 42 + 
					      '\nOUPUT:\n' + str(out) + 
				              '\nERROR:\n' + str(err) + 
					      '\nSTATUS: ' + str(p_status) + '\n')
	print 'Waiting for next cmd...'
    sleep(btwn_cmd)



