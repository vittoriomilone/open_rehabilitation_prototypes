# -*- coding: utf-8 -*-
"""
Created on Sun Sep 14 00:31:42 2014

@author: Administrator
"""
#import comunicazione_arduino  
import wx,os,time
from pygame import mixer
import threading,serial 
import random
#import wx,os,speech #speech only supported on windows machines 
#import wx.lib.inspection
from PIL import Image, ImageDraw
from espeak import espeak
espeak.set_voice('it')

try:
    package_directory = os.path.dirname(os.path.abspath(__file__))
    cartella_esercizi = os.path.join(package_directory, 'ESERCIZI')
except:
    pass

SERIALRX = wx.NewEventType()
# bind to serial data receive events
EVT_SERIALRX = wx.PyEventBinder(SERIALRX, 0)

class SerialRxEvent(wx.PyCommandEvent):
    eventType = SERIALRX
    def __init__(self, windowID, data):
        wx.PyCommandEvent.__init__(self, self.eventType, windowID)
        self.data = data

    def Clone(self):
        self.__class__(self.GetId(), self.data)


class InteractiveFrame(wx.Frame):

    title = "Interactive Mode ON"
    attivato =0
    
    def __init__(self):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title=self.title, size= (1280,800))  
        
        panel=wx.Panel(self)
        self.panel=panel
        self.panel.SetBackgroundColour('cyan')  
        
#elementi liste metafonologia_bisillabiche
        indice_lst_mtf_bsb=0
        indice_2_lst_mtf_bsb=0
        

        lst_mtf_bsb=[['cane200_200.jpg','cane', 'ca','caa','off'],
        ['casa200_200.jpg','casa', 'ca','caa','off'],
        ['dado200_200.jpg','dado','da','daa','off'],
        ['lana200_200.jpg','lana','la','laa','off'],
        ['luna200_200.jpg','luna','lu','luu','off'],
        ['mano200_200.jpg','mano','ma','maa','off'],
        ['mucca200_200.jpg','mucca', 'mu','muu','off'],
        ['pera_bianca200*200.jpg','pera','pe','pee','off'],
        ['pane_bianco200*200.jpg','pane','pa','paa','off'],
        ['sole200_200.jpg','sole','so','soo','off']]
        self.indice_lst_mtf_bsb=indice_lst_mtf_bsb
        self.indice_2_lst_mtf_bsb=indice_2_lst_mtf_bsb
        self.lst_mtf_bsb=lst_mtf_bsb
        self.ListShuffle()
        
        
#        indice_lst_mtf_bsb_scansione=0
#        indice_2_lst_mtf_bsb_scansione=0
#        lst_mtf_bsb_scansione=[['cane200_200_scansione.jpg','cane_scansione', 'ca'],
#        ['casa200_200_scansione.jpg','casa_scansione', 'ca'],
#        ['dado200_200_scansione.jpg','dado_scansione','da'],
#        ['lana200_200_scansione.jpg','lana_scansione','la'],
#        ['luna200_200_scansione.jpg','luna_scansione','lu'],
#        ['mano200_200_scansione.jpg','mano_scansione','ma'],
#        ['mucca200_200_scansione.jpg','mucca_scansione', 'mu'],
#        ['pane_bianco200*200_scansione.jpg','pane_scansione','pa'],
#        ['pera_bianca200*200_scansione.jpg','pera_scansione','pe'],
#        ['sole200_200_scansione.jpg','sole_scansione','so']]
#        self.indice_lst_mtf_bsb_scansione=indice_lst_mtf_bsb_scansione
#        self.indice_2_lst_mtf_bsb_scansione=indice_2_lst_mtf_bsb_scansione
#        self.lst_mtf_bsb_scansione=lst_mtf_bsb_scansione
        

#prima riga
        stellina_grande_bitmap=wx.Bitmap("stellina_grande250*250_cyan.jpg")
        stellina_grande_bitmap=self.scale_bitmap(stellina_grande_bitmap, 200, 200)  
        
#        stellina_grande = wx.StaticBitmap(panel, -1, stellina_grande_bitmap, (stellina_grande_bitmap.GetWidth(), stellina_grande_bitmap.GetHeight()))
        stellina_grande = wx.StaticBitmap(panel, -1,stellina_grande_bitmap, (stellina_grande_bitmap.GetWidth(),stellina_grande_bitmap.GetHeight()))
        static_box_domanda= wx.StaticText(panel,-1,label="CHI COMINCIA CON ", style=wx.ALIGN_CENTER)
        static_box_domanda.SetFont(wx.Font(20, wx.DECORATIVE,wx.NORMAL, wx.BOLD))        
        button_domanda=wx.Button(panel, id=wx.ID_ANY, label=self.lst_mtf_bsb[self.indice_lst_mtf_bsb][2],size=(100,56))
        button_domanda.SetFont(wx.Font(20, wx.DECORATIVE,wx.NORMAL, wx.BOLD))
        punto_interrogativo= wx.StaticText(panel,-1,label=" ?", style=wx.ALIGN_CENTER)
        punto_interrogativo.SetFont(wx.Font(20, wx.DECORATIVE,wx.NORMAL, wx.BOLD))        
 
#seconda riga 

        button_solution=wx.Button(panel, id=wx.ID_ANY, label=self.lst_mtf_bsb[self.indice_lst_mtf_bsb][2],size=(100,56))
        button_solution.SetFont(wx.Font(20, wx.DECORATIVE,wx.NORMAL, wx.BOLD))
#        button = wx.ToggleButton(panel, id=wx.ID_ANY, label="PA",pos=(60,100))
#        button2 = wx.ToggleButton(panel, id=wx.ID_ANY, label="PO",pos=(160,100))


#terza riga

### Tentativo di automatizzare la creazione del bordo intorno alle immagini per la scansione


#        bitmap = wx.Bitmap("pane_bianco200*200.jpg")
#        bitmap2 = wx.Bitmap("pera_bianca200*200.jpg")
#        sBitMap = wx.StaticBitmap(panel, -1, bitmap, (bitmap.GetWidth(), bitmap.GetHeight()))
#        sBitMap2 = wx.StaticBitmap(panel, -1, bitmap2, (bitmap2.GetWidth(), bitmap2.GetHeight()))
#        self.button_solution=button_solution
#        self.bitmap=bitmap
#        self.bitmap2=bitmap2
#        self.sBitMap=sBitMap
#        self.sBitMap2=sBitMap2

        self.bitmap = wx.Bitmap(self.lst_mtf_bsb[self.indice_lst_mtf_bsb][self.indice_2_lst_mtf_bsb])
        self.bitmap2 = wx.Bitmap(self.lst_mtf_bsb[self.indice_lst_mtf_bsb+1][self.indice_2_lst_mtf_bsb])
        self.sBitMap = wx.StaticBitmap(panel, -1, self.bitmap, (self.bitmap.GetWidth(), self.bitmap.GetHeight()))
        self.sBitMap2 = wx.StaticBitmap(panel, -1, self.bitmap2, (self.bitmap2.GetWidth(), self.bitmap2.GetHeight()))
        self.button_solution=button_solution
        self.button_domanda=button_domanda
        self.static_box_domanda=static_box_domanda
        self.punto_interrogativo=punto_interrogativo
#        self.bitmap=bitmap
#        self.bitmap2=bitmap2
#        self.sBitMap=sBitMap
#        self.sBitMap2=sBitMap2

#quarta riga
        stellina_piccola_bianca_bitmap = wx.Bitmap("stellina_bianca_200*200.jpg")
        stellina_piccola_bianca_bitmap =self.scale_bitmap(stellina_piccola_bianca_bitmap, 80, 80)
        
        stellina_piccola_mezza_bianca_bitmap = wx.Bitmap("stellina_mezza_bianca_200*200.jpg")
        stellina_piccola_mezza_bianca_bitmap =self.scale_bitmap(stellina_piccola_mezza_bianca_bitmap, 80, 80)
        
        stellina_piccola_gialla_bitmap=wx.Bitmap("stellina_grande200*200_cyan.jpg")
        stellina_piccola_gialla_bitmap =self.scale_bitmap(stellina_piccola_gialla_bitmap, 80, 80)
        self.stellina_piccola_gialla_bitmap =stellina_piccola_gialla_bitmap 

#controllo dinamico
        stellina_count=0
        self.stellina_count=stellina_count
        indice_stellina=0
        self.indice_stellina=indice_stellina
        scelta_stellina_piccola=[stellina_piccola_bianca_bitmap,stellina_piccola_mezza_bianca_bitmap,stellina_piccola_gialla_bitmap]        
        self.scelta_stellina_piccola=scelta_stellina_piccola        
        stellina_piccola_1 = wx.StaticBitmap(panel, -1, scelta_stellina_piccola[indice_stellina],(scelta_stellina_piccola[indice_stellina].GetWidth(),scelta_stellina_piccola[indice_stellina].GetHeight()))
        stellina_piccola_2 = wx.StaticBitmap(panel, -1, scelta_stellina_piccola[indice_stellina],(scelta_stellina_piccola[indice_stellina].GetWidth(),scelta_stellina_piccola[indice_stellina].GetHeight()))        
        stellina_piccola_3 = wx.StaticBitmap(panel, -1, scelta_stellina_piccola[indice_stellina],(scelta_stellina_piccola[indice_stellina].GetWidth(),scelta_stellina_piccola[indice_stellina].GetHeight()))
        stellina_piccola_4 = wx.StaticBitmap(panel, -1, scelta_stellina_piccola[indice_stellina],(scelta_stellina_piccola[indice_stellina].GetWidth(),scelta_stellina_piccola[indice_stellina].GetHeight()))
        stellina_piccola_5 = wx.StaticBitmap(panel, -1, scelta_stellina_piccola[indice_stellina],(scelta_stellina_piccola[indice_stellina].GetWidth(),scelta_stellina_piccola[indice_stellina].GetHeight()))
        self.stellina_piccola_1=stellina_piccola_1
        self.stellina_piccola_2=stellina_piccola_2
        self.stellina_piccola_3=stellina_piccola_3
        self.stellina_piccola_4=stellina_piccola_4
        self.stellina_piccola_5=stellina_piccola_5
#        stellina_piccola_bianca = wx.StaticBitmap(panel, -1, stellina_grande_bitmap, (80,80))        

#help sonoro e scritto
        book_icon_bitmap = wx.Bitmap("book_icon80x80.png")
        speaker_icon_bitmap = wx.Bitmap("Speaker_Icon80*80.png")
        book_icon = wx.StaticBitmap(panel, -1, book_icon_bitmap, (book_icon_bitmap.GetWidth(), book_icon_bitmap.GetHeight()))
        speaker_icon = wx.StaticBitmap(panel, -1, speaker_icon_bitmap, (speaker_icon_bitmap.GetWidth(), speaker_icon_bitmap.GetHeight()))
        
#layout (box sizer)
        
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer=vsizer
        hbox_new1= wx.BoxSizer(wx.HORIZONTAL)
        hbox_new1_1= wx.BoxSizer(wx.HORIZONTAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
                   
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox1=hbox1
        self.hbox0=hbox0


# prima riga orizzontale        
        
        hbox_new1.AddStretchSpacer(1) 
        hbox_new1_1.Add(stellina_grande,0,wx.ALIGN_CENTER)
        hbox_new1_1.AddSpacer(30)
        hbox_new1_1.Add(static_box_domanda,0,wx.ALIGN_CENTER)
        hbox_new1_1.AddSpacer(10)        
        hbox_new1_1.Add(button_domanda,0,wx.ALIGN_CENTER)
        hbox_new1_1.AddSpacer(5)
        hbox_new1_1.Add(punto_interrogativo,0,wx.ALIGN_CENTER)
        hbox_new1.Add(hbox_new1_1,0,wx.ALIGN_CENTER)                 
        hbox_new1.AddStretchSpacer(1)        
        
# box sizer - seconda riga orizzontale        
        hbox1.AddStretchSpacer(1)
        hbox0.Add(button_solution,0,wx.ALIGN_CENTER)
        
        hbox1.Add(hbox0,0,wx.ALIGN_CENTER)        
        hbox1.AddStretchSpacer(1)
        """CHIAMARE EXPAND su questo sizer per renderlo dinamicamente
        ridimensionabile"""

#box sizer -terza riga orizzontale

        hbox2= wx.BoxSizer(wx.HORIZONTAL)
        hbox3= wx.BoxSizer(wx.HORIZONTAL)
        hbox5= wx.BoxSizer(wx.HORIZONTAL)
        self.hbox3=hbox3
        self.hbox2=hbox2
        self.hbox5=hbox5
        
        hbox2.AddStretchSpacer(1)
        
        hbox3.Add(self.sBitMap,0,wx.ALIGN_CENTER)
 
          
        hbox3.AddSpacer(100)        
#        self.hbox5=hbox5
#        hbox2.Add(hbox5,3,wx.ALIGN_CENTER)
        hbox3.Add(self.sBitMap2,0,wx.ALIGN_CENTER)
##       
        hbox2.Add(hbox3,0,wx.ALIGN_CENTER)        
        hbox2.AddStretchSpacer(1)        
        
#box sizer -quarta riga orizzontale
        
      
        hbox_new4= wx.BoxSizer(wx.HORIZONTAL)
        hbox_new4_1= wx.BoxSizer(wx.HORIZONTAL)

        hbox_new4.AddStretchSpacer(1) 
        hbox_new4_1.Add(stellina_piccola_1,0,wx.ALIGN_CENTER)
        hbox_new4_1.AddSpacer(5)
        hbox_new4_1.Add(stellina_piccola_2,0,wx.ALIGN_CENTER)
        hbox_new4_1.AddSpacer(5)
        hbox_new4_1.Add(stellina_piccola_3,0,wx.ALIGN_CENTER)
        hbox_new4_1.AddSpacer(5)
        hbox_new4_1.Add(stellina_piccola_4,0,wx.ALIGN_CENTER)
        hbox_new4_1.AddSpacer(5)
        hbox_new4_1.Add(stellina_piccola_5,0,wx.ALIGN_CENTER)
        hbox_new4_1.AddSpacer(100)
        hbox_new4_1.Add(speaker_icon,0,wx.ALIGN_CENTER)
        hbox_new4_1.AddSpacer(5)
        hbox_new4_1.Add(book_icon,0,wx.ALIGN_CENTER)
        hbox_new4_1.AddSpacer(5)
        hbox_new4.Add(hbox_new4_1,0,wx.ALIGN_CENTER)                 
        hbox_new4.AddStretchSpacer(1)   

#box sizer - aggiunta sizer orizzontali a quello verticale

        vsizer.AddStretchSpacer(1)
        vsizer.Add(hbox_new1,0,wx.EXPAND|wx.ALIGN_CENTER)
        vsizer.AddSpacer(50)        
        vsizer.Add(hbox1,0,wx.EXPAND|wx.ALIGN_CENTER) 
        vsizer.AddSpacer(50)           
        vsizer.Add(hbox2,0,wx.EXPAND|wx.ALIGN_CENTER)
        vsizer.AddSpacer(50)
        vsizer.Add(hbox_new4,0,wx.EXPAND|wx.ALIGN_CENTER)
        
        vsizer.AddStretchSpacer(1)
        panel.SetSizer(vsizer)        
        
        
        self.sBitMap.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown1)
        self.sBitMap2.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown2)
        
#        dati_arduino = threading.Thread(target=self.SerialCommunication, args = ())
##        t.daemon = True
#        dati_arduino.start()
#        espeak.synth("Quale comincia con"+str(self.button_solution.GetLabel())+"?")
#        espeak.synth("Quale comincia con"+str(self.lst_mtf_bsb[self.indice_lst_mtf_bsb][3])+"?")
#        espeak.synth("Quale comincia con..."+str(self.button_solution.GetLabel())+str(self.button_solution.GetLabel())[-1]+"?")    
        espeak.synth("Quale comincia con..."+str(self.button_solution.GetLabel())+"?")    

        self.Scansione_Immagini()


        self.Bind(wx.EVT_CLOSE, self.OnQuit)

#.............new_serial.....................

        self.serial = serial.Serial('/dev/ttyACM0',115200, timeout=0.5)
        self.thread = None
        self.alive = threading.Event() 
        self.StartThread()  
        self.attach_events()          #register events

        if not self.alive.isSet():
            print "porta chiusa"
            self.Close()

       #----------------------------------------------------------------------
    def ListShuffle(self):
        random.shuffle(self.lst_mtf_bsb)
        index=0
        while index<len(self.lst_mtf_bsb)-1:
            if self.lst_mtf_bsb[index][2] == self.lst_mtf_bsb[index+1][2] and index % 2 == 0:
               random.shuffle(self.lst_mtf_bsb)
               index=index+1
        #       print lst_mtf_bsb
            else:
               index=index+1
        print self.lst_mtf_bsb
        print index
        
    def attach_events(self):           
            self.Bind(EVT_SERIALRX, self.OnSerialRead)   
            
    def StartThread(self):
            """Start the receiver thread"""        
            self.thread = threading.Thread(target=self.ComPortThread)
            self.thread.setDaemon(1)
            self.alive.set()
            self.thread.start()
#            self.StopThread()
#            self.serial.close()
    
    def StopThread(self):
        """Stop the receiver thread, wait util it's finished."""
        if self.thread is not None:
            self.alive.clear()          #clear alive event for thread
            self.thread.join()          #wait until thread has finished
            self.thread = None     

    def OnSerialRead(self, event):
        """Handle input from the serial port."""
        print "arrivato event handler"
        text = event.data
        print str(text)
        self.Test_Answer(text)
        
    def ComPortThread(self):
        """Thread that handles the incomming traffic. Does the basic input
           transformation (newlines) and generates an SerialRxEvent"""
        while self.alive.isSet():               #loop while alive event is true
            text = self.serial.read(1)          #read one, with timout
            if text:                            #check if not timeout
                                    
                n = self.serial.inWaiting()     #look if there is more to read
                print "testo in attesa:"+ str(n)                
                if n:
                    text = text + self.serial.read(n) #get it
                print "testo ricevuto: "+ str(text)
                event = SerialRxEvent(self.GetId(), text)
                self.GetEventHandler().AddPendingEvent(event) 

 #.............end of new_serial.....................   
         
    def OnQuit(self, evt):
        self.Destroy()
        ChoiceFrame().Show()
    
    def scale_bitmap(self,bitmap, width, height):
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result    

    def Scansione_Immagini(self):
#        if self.indice_lst_mtf_bsb<=len(self.lst_mtf_bsb)-1:
            
            fname1 = self.lst_mtf_bsb[self.indice_lst_mtf_bsb][self.indice_2_lst_mtf_bsb]
            im = Image.open(fname1)        
            draw = ImageDraw.Draw(im)
            draw.rectangle((1, 1, im.size[0]-2, im.size[1]-2), outline="red")
            draw.rectangle((0, 0,im.size[0]-1, im.size[1]-1), outline="red")
#                     
            fname4= self.lst_mtf_bsb[self.indice_lst_mtf_bsb][self.indice_2_lst_mtf_bsb][:-4]+"_scansione"+self.lst_mtf_bsb[self.indice_lst_mtf_bsb][self.indice_2_lst_mtf_bsb][-4:]            
            print "sc imm 1 immagine sinistra: "+ str(fname4)            
            im.save(fname4)
            fname4_scansione_bitmap = wx.Bitmap(fname4)

            self.sBitMap.SetBitmap(fname4_scansione_bitmap)
            self.sBitMap.SetLabel(self.lst_mtf_bsb[self.indice_lst_mtf_bsb][self.indice_2_lst_mtf_bsb][:-4]+"_scansione")
            image_des = wx.Image(name= self.lst_mtf_bsb[self.indice_lst_mtf_bsb+1][0], 
                            type =wx.BITMAP_TYPE_ANY)            
            new_bitmap_des=wx.BitmapFromImage(image_des)
#                self.foto.SetBitmap(bitmap=self.fototest)
            self.sBitMap2.SetBitmap(bitmap=new_bitmap_des)
#            self.sBitMap2.SetBitmap(self.bitmap2)
            self.sBitMap2.SetLabel(self.lst_mtf_bsb[self.indice_lst_mtf_bsb+1][1])            
            self.panel.SetSizer(self.vsizer)
            self.panel.Layout()
                        
            wx.CallLater(1500,self.Scansione_Immagini2)   
                
                
         
    def Scansione_Immagini2(self):
         
        fname3 = self.lst_mtf_bsb[self.indice_lst_mtf_bsb+1][self.indice_2_lst_mtf_bsb]
        im2 = Image.open(fname3)
        draw = ImageDraw.Draw(im2)
        draw.rectangle((1, 1, im2.size[0]-2, im2.size[1]-2), outline="red")
        draw.rectangle((0, 0,im2.size[0]-1, im2.size[1]-1), outline="red")
        fname4 = self.lst_mtf_bsb[self.indice_lst_mtf_bsb+1][self.indice_2_lst_mtf_bsb][:-4]+"_scansione"+self.lst_mtf_bsb[self.indice_lst_mtf_bsb+1][self.indice_2_lst_mtf_bsb][-4:]            
        im2.save(fname4)
        print "sc imm 2 immagine destra: "+ str(fname4) 
        fname4_scansione_bitmap = wx.Bitmap(fname4)
        self.sBitMap2.SetBitmap(fname4_scansione_bitmap)
#        self.sBitMap2.SetLabel(self.lst_mtf_bsb[self.indice_lst_mtf_bsb_scansione][1])
        self.sBitMap2.SetLabel(self.lst_mtf_bsb[self.indice_lst_mtf_bsb+1][self.indice_2_lst_mtf_bsb][:-4]+"_scansione")
        image_sin = wx.Image(name= self.lst_mtf_bsb[self.indice_lst_mtf_bsb][0], 
                            type =wx.BITMAP_TYPE_ANY)            
        new_bitmap_sin=wx.BitmapFromImage(image_sin)
#                self.foto.SetBitmap(bitmap=self.fototest)
        self.sBitMap.SetBitmap(bitmap=new_bitmap_sin)
#        self.sBitMap.SetBitmap(self.bitmap)
        self.sBitMap.SetLabel(self.lst_mtf_bsb[self.indice_lst_mtf_bsb][1])
#        self.indice_lst_mtf_bsb=self.indice_lst_mtf_bsb+2
#        self.sBitMap2 = wx.StaticBitmap(self.panel, -1, self.bitmap2, (self.bitmap2.GetWidth(), self.bitmap2.GetHeight()))
        self.panel.SetSizer(self.vsizer)
        self.panel.Layout()
#        
        wx.CallLater(1500,self.Scansione_Immagini)
        
    def Test_Answer(self, text):
        
        print text
        print "button_solution_label= "+str(self.button_solution.GetLabel())
        print "label soluzione= "+str(self.lst_mtf_bsb[self.indice_lst_mtf_bsb][2])
        if self.sBitMap.GetLabelText()== self.lst_mtf_bsb[self.indice_lst_mtf_bsb][self.indice_2_lst_mtf_bsb][:-4]+"_scansione" and str(text)[1:] > 130 and str(self.lst_mtf_bsb[self.indice_lst_mtf_bsb][2])== str(self.button_solution.GetLabel()): #and InteractiveFrame.attivato == 0:           
            print "abbiamo vinto a sinistra"
            
            self.update()
            
#            self.OnForward_left()
        if self.sBitMap2.GetLabelText()== self.lst_mtf_bsb[self.indice_lst_mtf_bsb+1][self.indice_2_lst_mtf_bsb][:-4]+"_scansione" and str(text)[1:] > 130 and str(self.lst_mtf_bsb[self.indice_lst_mtf_bsb+1][2]) == str(self.button_solution.GetLabel()): #and InteractiveFrame.attivato == 0:           
            print "abbiamo vinto a destra"
            
            self.update()
#            self.OnForward_right()    
            
#          
           
    def update(self):
           
                    
#            self.img = wx.Image(name= self.immagine[self.lista_immagini], 
#                            type =wx.BITMAP_TYPE_ANY)
##        
#            self.fototest=wx.BitmapFromImage(self.img)
#            self.foto.SetBitmap(bitmap=self.fototest)
            while self.stellina_count <=5:
                self.stellina_count=self.stellina_count+1
                if self.stellina_count ==1:
                    self.stellina_piccola_1.SetBitmap(bitmap=self.scelta_stellina_piccola[2])
                    mixer.init()
                    self.s = mixer.Sound('finish_norm.wav')
                    self.s.play()
                    break
                if self.stellina_count ==2:
                    self.stellina_piccola_2.SetBitmap(bitmap=self.scelta_stellina_piccola[2])
                    mixer.init()
                    self.s = mixer.Sound('finish_norm.wav')
                    self.s.play()                    
                    break
                if self.stellina_count ==3:
                    self.stellina_piccola_3.SetBitmap(bitmap=self.scelta_stellina_piccola[2])
                    mixer.init()
                    self.s = mixer.Sound('finish_norm.wav')
                    self.s.play()                    
                    break
                if self.stellina_count ==4:
                    self.stellina_piccola_4.SetBitmap(bitmap=self.scelta_stellina_piccola[2])
                    mixer.init()
                    self.s = mixer.Sound('finish_norm.wav')
                    self.s.play()                    
                    break
                if self.stellina_count ==5:
                    self.stellina_piccola_5.SetBitmap(bitmap=self.scelta_stellina_piccola[2])
                    mixer.init()
                    self.s = mixer.Sound('finish_norm.wav')
                    self.s.play()
                    self.sBitMap.Hide()
                    self.sBitMap2.Hide()
                    self.button_solution.Hide()
                    self.button_domanda.Hide()
#        self.button_solution.Hide()
                    self.static_box_domanda.Hide()
                    self.punto_interrogativo.Hide()
                    print "stellina count over 5: "+str(self.stellina_count)
                    wx.CallLater(1500,self.onFinish)                    
                    
                          
#                self.Destroy()
#                ChoiceFrame().Show()
#            mixer.init()
#            self.s = mixer.Sound('finish_norm.wav')
#            self.s.play()
            if self.indice_lst_mtf_bsb <7:
                print "label ed immagine aggiornati!"
                print "indice_lista: "+ str(self.indice_lst_mtf_bsb)
                self.indice_lst_mtf_bsb=self.indice_lst_mtf_bsb+2
                image_sin = wx.Image(name= self.lst_mtf_bsb[self.indice_lst_mtf_bsb][0], 
                            type =wx.BITMAP_TYPE_ANY)
                image_des = wx.Image(name= self.lst_mtf_bsb[self.indice_lst_mtf_bsb+1][0], 
                            type =wx.BITMAP_TYPE_ANY)            
                new_bitmap_sin=wx.BitmapFromImage(image_sin)
                new_bitmap_des=wx.BitmapFromImage(image_des)
#                self.foto.SetBitmap(bitmap=self.fototest)
                self.sBitMap.SetBitmap(bitmap=new_bitmap_sin)
                self.sBitMap2.SetBitmap(bitmap=new_bitmap_des)
                #cercare di  randomizzare con random.choice la scelta della soluzione?
#                label=random.choice(str(self.lst_mtf_bsb[self.indice_lst_mtf_bsb][2]),str(self.lst_mtf_bsb[self.indice_lst_mtf_bsb+1][2]))
#                label=random.choice(str(self.lst_mtf_bsb[self.indice_lst_mtf_bsb][2]),str(self.lst_mtf_bsb[self.indice_lst_mtf_bsb+1][2]))                
                mylabel=random.sample(set([self.lst_mtf_bsb[self.indice_lst_mtf_bsb][2],self.lst_mtf_bsb[self.indice_lst_mtf_bsb+1][2]]), 1)                
                print type(mylabel)                
                print "la soluzione ora è: "+str(mylabel)               
#                str_label=str(mylabel)
                self.button_solution.SetLabel(label=mylabel[0])
                self.button_domanda.SetLabel(label=mylabel[0])
                espeak.synth("Quale comincia con..."+str(self.button_solution.GetLabel())+"?")
                print "button_solution_label aggiornato= "+str(self.lst_mtf_bsb[self.indice_lst_mtf_bsb][2])
                print "label soluzione aggiornato= "+str(self.lst_mtf_bsb[self.indice_lst_mtf_bsb][2])
                print "indice_lista aggiornato: "+ str(self.indice_lst_mtf_bsb)
                
                self.panel.SetSizer(self.vsizer)
                self.panel.Layout()
                print "stellina count: "+str(self.stellina_count)
#            if self.stellina_count >5:
#                print "stellina count over 5: "+str(self.stellina_count)
#                self.onFinish()
                
                # aggiungi istruzioni debug per printing
    def onFinish(self):
        mixer.init()
        self.finish = mixer.Sound('tada_amplified.wav')
        self.finish.play()
#        self.sBitMap.Hide()
#        self.sBitMap2.Hide()
#        self.button_domanda.Hide()
##        self.button_solution.Hide()
#        self.static_box_domanda.Hide()
#        self.punto_interrogativo.Hide()
        self.completed=wx.StaticText(self.panel,-1,label="ESERCIZIO COMPLETATO, COMPLIMENTI!!!", pos=(330,420) , style=wx.ALIGN_CENTER) 
        self.completed.SetFont(wx.Font(20, wx.DECORATIVE,wx.NORMAL, wx.BOLD))
        self.panel.Layout()
        wx.CallLater(3000,self.onDestroy)
    
    def onDestroy(self):
        self.Destroy()
        ChoiceFrame().Show()
    
        
    def onButton(self):
        """
        This method is fired when its corresponding button is pressed
        """
        
        self.button.SetValue(True)
        self.button2.SetValue(False)
#        wx.CallLater(50,self.SensorResults)
#        if self.parent.button.GetValue() ==True and yes_sensor >80:
#                self.player = wx.Sound('tada.wav') 
#                self.player.Play()
#                return "risolto!!!"
#        if exited == 1:
#            return       
#        else:
        wx.CallLater(1500,self.onButton2)
        
        
#        print "Button pressed!"
    def onButton2(self):
        """
        This method is fired when its corresponding button is pressed
        """
#        self.button2.SetLabel("PA")
#        if exited ==1:
#            return
        self.button.SetValue(False)
        self.button2.SetValue(True)
#        wx.CallLater(50,self.SensorResults)
        wx.CallLater(1500,self.onButton)   
#    def initialdelay(self):
#        wx.CallLater(500,self.voicesolution)
#    
#    def voicesolution(self):
#        speech.say("PAH!")   
    
    def OnLeftDown1(self, evt):
        print "OnLeftDown"
        self.sBitMap.SetFocus()
            
            
#           print comunicazione_arduino.SerialData.yes_sensor
    def OnLeftDown2(self, evt):
        print "OnLeft2Down"
#        print comunicazione_arduino.yes_sensor
        self.sBitMap2.SetFocus()
#   
class ImgPanel(wx.Panel):
    def __init__(self, parent, image):
        wx.Panel.__init__(self, parent)

        img = wx.Image(image, wx.BITMAP_TYPE_ANY)
        self.sBmp = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img))

        sizer = wx.BoxSizer()
        sizer.Add(item=self.sBmp, proportion=0, flag=wx.ALL, border=10)
        self.SetBackgroundColour('green')
        self.SetSizerAndFit(sizer)

class ChoiceFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Imposta Sessione',
        size=(800, 600))
        panel = wx.Panel(self, -1)
        sampleList = ['Metafonologia', 'Analisi visiva', 'Seq sillabica', 'Seq grafemica']
        wx.StaticText(panel, -1, "Seleziona esercizio:", (85, 30))
        self.scelta_esercizio = wx.Choice(panel, -1, (85, 60), choices=sampleList)
#         self.scelta_esercizio= scelta_esercizio
        sampleList2 = ['Facile       ', 'Medio       ', 'Difficile        ']
        wx.StaticText(panel, -1, "Seleziona livello test:", (305, 30))
        self.scelta_livello = wx.Choice(panel, -1, (305, 60), choices=sampleList2)
#        self.scelta_livello= scelta_livello
        sampleList3 = ['1 Pallina', '2 Palline', 'Pulsantiera 1 Area', 
                       'Pulsantiera 2 Aree', 'Pulsantiera 3 Aree','Pulsantiera 4 Aree']
        wx.StaticText(panel, -1, "Seleziona sensore:", (525, 30))
        self.scelta_sensore = wx.Choice(panel, -1, (525, 60), choices=sampleList3)
        self.buttonvalidate = wx.Button(panel, -1, "    CONFERMA    ",(305,150), (125,40), style=wx.BU_EXACTFIT)
#        self.scelta_sensore = scelta_sensore  
        self.Bind(wx.EVT_CHOICE, self.OnChoice1, self.scelta_esercizio)
        self.Bind(wx.EVT_CHOICE, self.OnChoice2, self.scelta_livello)
        self.Bind(wx.EVT_CHOICE, self.OnChoice3, self.scelta_sensore)
        self.Bind(wx.EVT_BUTTON, self.OnParsingChoices, self.buttonvalidate)
        
    def OnChoice1(self, event):
            selection = self.scelta_esercizio.GetStringSelection()
            index = self.scelta_esercizio.GetSelection()
            print "Selected Item1: %d '%s'" % (index, selection)
#            self.OnParsingChoices()
    def OnChoice2(self, event):
            selection = self.scelta_livello.GetStringSelection()
            index = self.scelta_livello.GetSelection()
            print "Selected Item2: %d '%s'" % (index, selection)
#            self.OnParsingChoices()
    def OnChoice3(self, event):
            selection = self.scelta_sensore.GetStringSelection()
            index = self.scelta_sensore.GetSelection()
            print "Selected Item3: %d '%s'" % (index, selection)
#            self.OnParsingChoices()
    def OnParsingChoices(self, event):
        if self.scelta_esercizio.GetSelection() == 0 and self.scelta_livello.GetSelection() == 0 and  self.scelta_sensore.GetSelection() == 0:
            self.Hide()
#            InteractiveFrame().ListShuffle()
            InteractiveFrame().Show()
            print "inizia esercizio1!"
        else:
            print "gli altri esercizi non sono ancora pronti!"
            
if __name__ == '__main__':
    app = wx.PySimpleApp()
    ChoiceFrame().Show()
#    wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
# 
# def OnCaricaEsercizi(self,evt):
#        
#                
#        try:
#            dlg = wx.FileDialog(self.panel, "Scegli Esercizio...",
#             cartella_esercizi, style=wx.OPEN, wildcard="*.*")
#        except:
#            dlg = wx.FileDialog(self.panel, "Scegli Esercizio...",
#            defaultDir=".", style=wx.OPEN, wildcard="*.*")      
#        if dlg.ShowModal() == wx.ID_OK:
#            self.filename = dlg.GetPath()
#            self.ReadFile()
#            #self.SetTitle(self.title + ' -- ' + self.filename)
#        dlg.Destroy()   
#    def ReadFile(self):
#        self.lista_figure = 0
#        self.indice_righe=0       
#        self.foreground_colors=0
#        f = open(self.filename, 'r+')
#        self.righe = eval (f.read())           
#        f.close()
#        self.update()
   
# def OnForward(self, evt):

#        print "fwd button pressed"
#        if self.indice_lines<len(self.lines)-1:      
#            self.indice_lines+=1
#    
#        if self.lista_immagini <len(self.immagine)-1: 
#            self.lista_immagini+=1
#        self.answer.Clear()
#        #wx.CallLater(self.speed, self.update) 
#        self.update()  

#    def OnForward_left(self, evt):
#
#        print "fwd button pressed_left"
#        if self.indice_lst_mtf_bsb<len(self.lst_mtf_bsb)-1:      
#            self.indice_lst_mtf_bsb+=1
#            
##        if self.lista_immagini <len(self.immagine)-1: 
##            self.lista_immagini+=1
##        self.answer.Clear()
#        #wx.CallLater(self.speed, self.update) 
#            fname1 = self.lst_mtf_bsb[self.indice_lst_mtf_bsb][self.indice_2_lst_mtf_bsb]
#            im = Image.open(fname1)        
#            draw = ImageDraw.Draw(im)
#            draw.rectangle((1, 1, im.size[0]-2, im.size[1]-2), outline="red")
#            draw.rectangle((0, 0,im.size[0]-1, im.size[1]-1), outline="red")
#            fname2 = self.lst_mtf_bsb_scansione[self.indice_lst_mtf_bsb_scansione][self.indice_2_lst_mtf_bsb_scansione]            
#            im.save(fname2)
#            fname2_scansione_bitmap = wx.Bitmap(fname2)
#            self.sBitMap.SetBitmap(fname2_scansione_bitmap)
#            self.sBitMap.SetLabel(self.lst_mtf_bsb_scansione[self.indice_lst_mtf_bsb_scansione][1])
#            
#            self.sBitMap2.SetBitmap(self.bitmap2)
#            self.sBitMap2.SetLabel(self.lst_mtf_bsb[self.indice_lst_mtf_bsb][1])
#            self.panel.SetSizer(self.vsizer)
#            self.panel.Layout()
#    #            wx.CallLater(1500,self.Scansione_Immagini2)
#            
#            
##    self.lst_mtf_bsb
#        def OnForward_right(self):
#            print "fwd button pressed_right"
#            if self.indice_lst_mtf_bsb<len(self.lst_mtf_bsb)-1:      
#                self.indice_lst_mtf_bsb+=1
#            fname3 = self.lst_mtf_bsb[self.indice_lst_mtf_bsb][self.indice_2_lst_mtf_bsb]
#            im2 = Image.open(fname3)
#            draw = ImageDraw.Draw(im2)
#            draw.rectangle((1, 1, im2.size[0]-2, im2.size[1]-2), outline="red")
#            draw.rectangle((0, 0,im2.size[0]-1, im2.size[1]-1), outline="red")
#            fname4 = self.lst_mtf_bsb_scansione[self.indice_lst_mtf_bsb_scansione][self.indice_2_lst_mtf_bsb_scansione]            
#            im2.save(fname4)
#            fname4_scansione_bitmap = wx.Bitmap(fname4)
#            self.sBitMap2.SetBitmap(fname4_scansione_bitmap)
#            self.sBitMap2.SetLabel(self.lst_mtf_bsb_scansione[self.indice_lst_mtf_bsb_scansione][1])
#            self.sBitMap.SetBitmap(self.bitmap)
#            self.sBitMap.SetLabel(self.lst_mtf_bsb[self.indice_lst_mtf_bsb][1])
#    #        self.sBitMap2 = wx.StaticBitmap(self.panel, -1, self.bitmap2, (self.bitmap2.GetWidth(), self.bitmap2.GetHeight()))
#            self.panel.SetSizer(self.vsizer)
#            self.panel.Layout()
#         