from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

#Rename Images
def renameFiles(ID):
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith(".JPG"):
                os.rename(filename, (shot_time + ID + ".JPG"))
                print("Renamed the JPG")

# Captures Image
# Sleeps for a bit to allow SD card to save
# Downloads file to image folder
# Clears file from camera
def captureImages():
    gp(triggerCommand)
    sleep(3)
    gp(downloadCommand)
    gp(clearCommand)

#Creates a folder for each unique image
def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print("Failed to create new directory")
    os.chdir(save_location)


# Kill gphoto process that
# starts whenever we connect
# the camera

def killgphoto2Process():
    p = subprocess.Popen(['ps', '-A'], stdout = subprocess.PIPE)
    out, err = p.communicate()
    
    #Search line that has process to kill
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            #Kill
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)

shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
picID = "PiShots"

#Clear File on Camera
clearCommand = ["--folder", "/store_00010001/DCIM/100D5100" , "-R", "--delete-all-files"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

folder_name = shot_date + picID
save_location = "/home/pi/Desktop/ThemeSong/images/" + folder_name

killgphoto2Process()
gp(clearCommand)
while True:
    createSaveFolder()
    captureImages()
    renameFiles(picID)
    sleep(5)