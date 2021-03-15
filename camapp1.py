from kivy.app import App
from kivy.uix.widget import Widget
#from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.popup import Popup
import cv2
from picamera import PiCamera
import uuid
import time
from time import sleep
import os
import shutil


total_program = '0'
total_intervalo = '0'
total_pic_intervalo = '0'
j = 0
r = 0
k = 0

framed = None


Window.clearcolor = (1,1,1,1)

class confirm_reboot(Popup):
    pass
class confirm_shutdown(Popup):
    pass
class end_process(Popup):
    pass
class my_popup(Popup):
    pass
class alert_popup(Popup):
    pass
class set_behavior(Widget):
    
    def changeToExit(self):
        cam_app.screen_manager.current = "exitLayout"
    def changeToTransfer(self):
        cam_app.screen_manager.current = "transLayout"
        
    def changeToMain(self):     
        cam_app.screen_manager.current = "mainLayout"
        
    def changeToPrev(self):
        cam_app.screen_manager.current = "prevLayout"
           
    def changeToProgram(self):
        cam_app.screen_manager.current = "programLayout"
        
    def initProgramClock(self):
        global k        
        self.function_program = Clock.schedule_interval(self.takeShot,k)
        self.function_stop = Clock.schedule_once(self.stopProgramClock,j)
    def stopProgramClock(self, *args):
        self.function_program.cancel()
        print('Program Clock was unscheduled')
        
    def checkValues(self):
        global j
        global r
        global k
        
        if j == 0 or k == 0 or r ==0 :
            cam_app.alertPopup.open()            
        else:
            cam_app.myPopup.open()
                
        
    def defValues(self):
        global total_program
        global total_intervalo
        global total_pic_intervalo
        global j
        global r
        global k
        k = int(total_intervalo)*60        
        j = (int(total_program)*60)+30
        r = int(total_pic_intervalo)      
        
    def takeShot(self,*args):
        global r        
        print("Iniciando Setup de Camara")
        camera = PiCamera(resolution=(1200,720),framerate=30)
        camera.iso = 600
        sleep(3)
        camera.shutter_speed = 50000
        #camera.exposure_speed = camera.shutter_speed
        camera.exposure_mode = 'off'
        
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g
        sleep(5)
        i = 0
        for filename in camera.capture_continuous('/home/pi/Pictures/Programa/P-%s.jpg'%(str(uuid.uuid4()))):
            print ('Toma %s guardada'% filename)
            sleep(4)
            i += 1
            if i == r:
                sleep(3)
                camera.close()
                break
            
    def transferAll(self):
        src="/home/pi/Pictures/Programa"
        dst="/media/pi/EBRDGE_CAM/Cam/Programa"
        file_names = os.listdir(src)        
        for filename in file_names:
            shutil.move(src=src+"/"+filename,dst=dst)
        src2="/home/pi/Pictures/Manual"
        dst2="/media/pi/EBRDGE_CAM/Cam/Manual"
        file_names = os.listdir(src2)
        for filename in file_names:
            shutil.move(src=src2+"/"+filename,dst=dst2)
        sleep(2)
        cam_app.endProcess.open()            
                   
    def programToUsb(self):        
        src="/home/pi/Pictures/Programa"
        dst="/media/pi/EBRDGE_CAM/Cam/Programa"
        file_names = os.listdir(src)        
        for filename in file_names:
            shutil.move(src=src+"/"+filename,dst=dst)
        sleep(2)
        cam_app.endProcess.open()            
        
            
    def manualToUsb(self):        
        src="/home/pi/Pictures/Manual"
        dst="/media/pi/EBRDGE_CAM/Cam/Manual"
        file_names = os.listdir(src)
        for filename in file_names:
            shutil.move(src=src+"/"+filename,dst=dst)
        sleep(2)
        cam_app.endProcess.open()
            
    def clearFiles(self):
        src="/home/pi/Pictures/Manual"
        src2="/home/pi/Pictures/Programa"
        list_one = os.listdir(src)
        list_two = os.listdir(src2)
        for file in list_one:
            os.remove(os.path.join(src,file))
        for file in list_two:
            os.remove(os.path.join(src2,file))
        sleep(2)
        cam_app.endProcess.open()
    def rebootDevice(self):
        sleep(1)
        os.system('sudo reboot now -h')
            
    def shutdownDevice(self):
        sleep(1)
        os.system('sudo shutdown now')
        

class program_layout(set_behavior):
    def clear_saved(self):
        global total_program
        global total_intervalo
        global total_pic_intervalo
        self.ids.totalProgram.text = ''
        self.ids.totalInter.text = ''
        self.ids.totalPicInter.text = ''
        self.ids.slider_1.value = 0
        self.ids.slider_2.value = 0
        self.ids.slider_3.value = 0
        total_program = '0'
        total_intervalo = '0'
        total_pic_intervalo = '0'
    def initValues(self):
        super(program_layout,self).defValues()
    
    def changeMain(self):
        super(program_layout,self).changeToMain()
    def save_totalProgram(self):
        global total_program
        self.ids.totalProgram.text = total_program
    def save_totalInter(self):
        global total_intervalo
        self.ids.totalInter.text = total_intervalo
    def save_picInterv(self):
        global total_pic_intervalo
        self.ids.totalPicInter.text = total_pic_intervalo
    def slide_intCaptur(self,*args):
        global total_intervalo
        self.slide_text.text =str(int(args[1]))
        total_intervalo = str(int(args[1]))
    def slide_fotInterv(self, *args):
        global total_pic_intervalo
        self.slide_text2.text = str(int(args[1]))
        total_pic_intervalo = str(int(args[1]))
    def slide_program(self, *args):
        global total_program
        self.slide_text3.text = str(int(args[1]))
        total_program = str(int(args[1]))        
    
class main_layout(set_behavior):    
    def changePrev(self):
        super(main_layout,self).changeToPrev()   
    def startUse(self):
        cam_app.startPrev()        
    def changeProgram(self):
        super(main_layout,self).changeToProgram()
    def testShot(self):
        super(main_layout,self).takeShot()
class trans_layout(set_behavior):
    pass
class prev_layout(set_behavior):
    global framed
    def changeMain(self):
        sleep(0.1)
        super(prev_layout,self).changeToMain()
    def stopUse(self):
        cam_app.stopClock()
        sleep(0.1)
    def saveImgVid(self):
        cv2.imwrite('/home/pi/Pictures/Manual/M-%s.jpg'%(str(uuid.uuid4())),framed)
    
class splash_layout(set_behavior):
    def changeMain(self):
        super(splash_layout,self).changeToMain()
        
class exit_layout(set_behavior):
    pass

class FinalCamApp(App):        
    
    def startPrev(self):
        sleep(0.1)        
        self.capture = cv2.VideoCapture(0)
        self.capture.open(0)
        self.function_img = Clock.schedule_interval(self.update, 1.0/33.0)
        
    def update(self,dt):
        global framed
        rt,framed = self.capture.read()
        buffer_1 = cv2.flip(framed,1)
        buffer_2 = buffer_1.tostring()
        texture_1 = Texture.create(size=(framed.shape[1],framed.shape[0]),colorfmt = 'rgba')
        texture_1.blit_buffer(buffer_2, colorfmt = 'bgr', bufferfmt = 'ubyte')
        self.prevLayout.ids.feedImg.texture = texture_1                
        
    def stopClock(self, *args):
        self.capture.release()
        self.function_img.cancel()        
        
    def build(self):
        self.confirmShutdown = confirm_shutdown()
        self.confirmReboot = confirm_reboot()
        self.myPopup = my_popup()
        self.endProcess = end_process()
        self.setBehavior = set_behavior()
        self.alertPopup = alert_popup()
        
        self.screen_manager = ScreenManager()
        self.prevLayout = prev_layout()
        screen_1 = Screen(name = "prevLayout")
        screen_1.add_widget(self.prevLayout)
        self.screen_manager.add_widget(screen_1)
        
        self.splashLayout = splash_layout()
        screen_2 = Screen(name = "splashLayout")
        screen_2.add_widget(self.splashLayout)
        self.screen_manager.add_widget(screen_2)
        
        self.mainLayout = main_layout()
        screen_3 = Screen(name = "mainLayout")
        screen_3.add_widget(self.mainLayout)
        self.screen_manager.add_widget(screen_3)
        
        self.programLayout = program_layout()
        screen_4 = Screen(name = "programLayout")
        screen_4.add_widget(self.programLayout)
        self.screen_manager.add_widget(screen_4)
        
        self.transLayout = trans_layout()
        screen_5 = Screen(name = "transLayout")
        screen_5.add_widget(self.transLayout)
        self.screen_manager.add_widget(screen_5)
        
        self.exitLayout = exit_layout()
        screen_6 = Screen(name = "exitLayout")
        screen_6.add_widget(self.exitLayout)
        self.screen_manager.add_widget(screen_6)
      
        cam_app.screen_manager.current = "splashLayout"
        return self.screen_manager      
    
       
if __name__ == '__main__':
    cam_app = FinalCamApp()
    cam_app.run()
    cv2.destroyAllWindows()
        