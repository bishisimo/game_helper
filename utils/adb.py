"""
@author '彼时思默'
@time 2019/12/7 13:16
@describe:
  通过adb.exe操纵Android
"""
import subprocess
from root import root
from loguru import logger


class AdbNio:
    def __init__(self):
        cmd = 'adb devices'
        statue = self._exe(cmd)
        if 'cannot connect to' in statue:
            cmd = f'adb connect 127.0.0.1:7555'
            self._exe(cmd)

    def _exe(self, cmd):
        logger.debug(cmd)
        connect = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                                   shell=True)
        if 'screencap' in cmd:
            return connect.stdout.read()
        stdout = connect.stdout.read().decode('utf8')
        # if stdout != '':
        # logger.debug(stdout)
        return stdout

    def run_app(self, name='com.cig.themonsterchef'):
        # com.cig.themonsterchef
        cmd = f'adb shell am start -n {name}'
        self._exe(cmd)

    def shot_screen(self):
        cmd = f'adb shell screencap -p'
        out_origin = self._exe(cmd)
        out = out_origin.replace(b'\r\n', b'\n')
        with open(f'{root}/temp/sc_t.png', 'wb')as file:
            file.write(out)
        return out

    def tap(self, x, y):
        cmd = f'adb shell input tap {x} {y}'
        self._exe(cmd)

    def swipe(self, start_x, start_y, end_x, end_y, delay=500):
        cmd = f'adb shell input swipe {start_x} {start_y} {end_x} {end_y} {delay}'
        self._exe(cmd)

    def tap_long(self, start_x, start_y, delay=500):
        cmd = f'adb shell input swipe {start_x} {start_y} {start_x} {start_y} {delay}'
        self._exe(cmd)


adb = AdbNio()

if __name__ == '__main__':
    # pic = adb.shot_screen()
    # with open('../temp/sc.png', 'wb')as file:
    #     file.write(pic)
    # adb.tap(450, 313)
    adb.tap_long(740, 180, 2000)
