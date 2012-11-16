import subprocess

class WiFi(object):
    def __init__(self):
        self.command = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport"
        self.args_info = "-I"
        self.args_scan = "-s"
        self.info = None

    def update(self):
        p = subprocess.Popen([self.command, self.args_info],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        (child_stdout, child_stdin) = (p.stdout, p.stdin)
        self.info = {}
        for line in child_stdout:
            key, value = line.strip().split(':', 1)
            if value.strip():
                self.info[key] = value.strip()

    def get_ssid(self):
        if 'SSID' in self.info:
            return self.info['SSID']
        else:
            return '??'
                        
