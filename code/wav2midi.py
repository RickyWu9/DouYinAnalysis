import os
import subprocess
import time
dir='..\\wav\\'
filename= os.listdir(dir)
exe='wav2midi.exe'
print(filename)
for file in filename:
    p = subprocess.Popen(exe+' '+dir+file)
    time.sleep(10)
    p.kill()
