import os

def run_command(command):
    return os.popen(command).read()

def get_daemon_status():
    return run_command('libinput-gestures-setup status').split('\n')

def get_daemon_autostart():
    status=get_daemon_status()
    autostart_s=status[1].split()
    return not 'not' in autostart_s

def get_daemon_running():
    status=get_daemon_status()
    running_s=status[2].split()
    return not 'not' in running_s

def set_daemon_autostart(value):
    if value:
        run_command('libinput-gestures-setup autostart')
    else:
        run_command('libinput-gestures-setup autostop')

def start_daemon():
    run_command('nohup libinput-gestures-setup start >> /dev/null')

def stop_daemon():
    run_command('libinput-gestures-setup stop')

def restart_daemon():
    run_command('nohup libinput-gestures-setup restart >> /dev/null')
