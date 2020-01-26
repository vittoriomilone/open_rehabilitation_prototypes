# -*- coding: utf-8 -*-

""" Copyright (C) 2013-2014 Vittorio Milone
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>."""

import wx,datetime
import glob, os,random
from pygame import mixer
import numpy as np
import matplotlib.pyplot as plt

pennarelli = ['red','magenta','yellow','green']
cvc = ['ron','ton','son','con']
bisillabiche = ['marco','bagno','toro','topo']
trisillabiche = ['casetta','postino','bambino','chiodino']


try:
    package_directory = os.path.dirname(os.path.abspath(__file__))
    cartella_esercizi = os.path.join(package_directory, 'ESERCIZI')
except:
    pass
try:
    package_directory = os.path.dirname(os.path.abspath(__file__))
    cartella_liste = os.path.join(package_directory, 'LISTE')
except:
    # probably running inside py2exe which doesn't set __file__
    pass
try:
    package_directory = os.path.dirname(os.path.abspath(__file__))
    cartella_utenti = os.path.join(package_directory, 'UTENTI')
except:
    # probably running inside py2exe which doesn't set __file__
    pass
#Afterwards, load your resources based on this package_directory:

class InteractiveFrame(wx.Frame):

    title = "Interactive Mode ON"
    
    
    def __init__(self):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title=self.title, size= (1024,768))  
        
        panel=wx.Panel(self)
        self.panel=panel
        self.panel.SetBackgroundColour('cyan')
        
        menuFile = wx.Menu()
        menuFile.Append(12, "Carica &Esercizi...")
        menuFile.AppendSeparator()
        menuFile.Append(13, "E&xit")
        
        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, "&File")
        self.SetMenuBar(menuBar)

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.SetStatusText\
        ("Versione Sperimentale per utilizzo non terapeutico",1)
        
        #EVENTI MENU /bindings
        
        self.Bind(wx.EVT_MENU, self.OnCaricaEsercizi, id=12)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=13)

    def OnQuit(self, evt):
        self.Close()
    def OnCaricaEsercizi(self,evt):
        
                
        try:
            dlg = wx.FileDialog(self.panel, "Scegli Esercizio...",
             cartella_esercizi, style=wx.OPEN, wildcard="*.*")
        except:
            dlg = wx.FileDialog(self.panel, "Scegli Esercizio...",
            defaultDir=".", style=wx.OPEN, wildcard="*.*")      
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.ReadFile()
            #self.SetTitle(self.title + ' -- ' + self.filename)
        dlg.Destroy()   
    def ReadFile(self):
        self.lista_figure = 0
        self.indice_righe=0       
        self.foreground_colors=0
        f = open(self.filename, 'r+')
        self.righe = eval (f.read())           
        f.close()
        self.update()
    
class MyFrame(wx.Frame):
   
    def __init__(self,parent, id):
        super(MyFrame, self).__init__(None)        

        panel=wx.Panel(self)
        self.panel=panel
        self.panel.SetBackgroundColour('green')

        self.t = wx.StaticText(panel,-1, style= wx.ALIGN_CENTER)
        self.answer=wx.TextCtrl(panel,-1, style=wx.TE_PROCESS_ENTER)

        font = wx.Font(22, wx.DEFAULT,wx.NORMAL,
        wx.BOLD)
        self.t.SetFont(font)
        self.new= wx.StaticText(panel,-1, style=wx.ALIGN_CENTER)

        try:        
            self.placeholder = wx.Image('green.JPG', wx.BITMAP_TYPE_ANY)
            self.foto = wx.StaticBitmap(self.panel,-1, wx.BitmapFromImage(self.placeholder),
                                    style=wx.ALIGN_CENTER)
        except:
            pass                            

        self.buttonnew = wx.Button(panel, -1, "New", style=wx.BU_EXACTFIT)
        self.buttonstats = wx.Button(panel, -1, "Stats", style=wx.BU_EXACTFIT)
        self.buttonback = wx.Button(panel, -1, "Back", style=wx.BU_EXACTFIT)
        self.buttonforward = wx.Button(panel, -1, "Forward", style=wx.BU_EXACTFIT)
        self.buttonreloadtext = wx.Button(panel, -1, "Reload Text!", style=wx.BU_EXACTFIT)
        self.buttonvalidate = wx.Button(panel, -1, "Validate", style=wx.BU_EXACTFIT)
        self.buttonsave = wx.Button(panel, -1, "Save", style=wx.BU_EXACTFIT)
        self.buttonreset = wx.Button(panel, -1, "Reset", style=wx.BU_EXACTFIT)        
        
        self.rispostegiuste= 0
        self.rispostesbagliate= 0
        self.buttonrispostegiuste = wx.Button(panel, -1, label = str(self.rispostegiuste), style=wx.BU_EXACTFIT)
        self.buttonrispostesbagliate = wx.Button(panel, -1, label = str(self.rispostesbagliate), style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnNew, self.buttonnew) 
        self.Bind(wx.EVT_BUTTON, self.OnStats, self.buttonstats)               
        self.Bind(wx.EVT_BUTTON, self.OnBack, self.buttonback)        
        self.Bind(wx.EVT_BUTTON, self.OnForward, self.buttonforward)
        self.Bind(wx.EVT_BUTTON, self.OnReloadText, self.buttonreloadtext)
        self.Bind(wx.EVT_BUTTON, self.OnValidateText, self.buttonvalidate)
        self.Bind(wx.EVT_BUTTON, self.OnSaveData, self.buttonsave)
        self.Bind(wx.EVT_BUTTON, self.OnReset, self.buttonreset)
        
        self.Bind(wx.EVT_TEXT_ENTER, self.OnEnterText,self.answer)
        self.Bind(wx.EVT_TEXT, self.OnEnterText,self.answer)
               
        #self.button.SetDefault()
        self.sc = wx.SpinCtrl(panel, -1, "",style=wx.SP_WRAP)
        self.sc.SetRange(200,800)
        self.sc.SetValue(500)
        
        
        #LAYOUT FRAME; PANEL ; BOX SIZERS        
        
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hbox2= wx.BoxSizer(wx.HORIZONTAL)
        hbox3= wx.BoxSizer(wx.HORIZONTAL)
        self.hbox3=hbox3
        self.hbox2=hbox2
        hbox2.AddStretchSpacer(1)
        hbox2.Add(hbox3,0,wx.ALIGN_CENTER,20)
        self.hbox3.Add(self.foto,0,wx.ALIGN_CENTER) 
        """CHIAMARE EXPAND su questo sizer per renderlo dinamicamente
        ridimensionabile"""

        hbox2.AddStretchSpacer(1)        
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox1=hbox1
        hbox1.AddStretchSpacer(1)
        hbox1.Add(self.t,0,wx.ALIGN_CENTER)
        """CHIAMARE EXPAND su questo sizer per renderlo dinamicamente
        ridimensionabile"""

        hbox1.AddStretchSpacer(1)
        hbox5=wx.BoxSizer(wx.HORIZONTAL)
        hbox5.AddStretchSpacer(1)
        hbox5.Add(wx.StaticText(panel,-1,label="QUAL ERA LA PAROLA?   ", style=wx.ALIGN_CENTER),0,wx.ALIGN_CENTER)
        hbox5.Add(self.answer,0,wx.ALIGN_CENTER)
        hbox5.AddStretchSpacer(1)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox4=hbox4
        hbox4.AddStretchSpacer(1)
        
        hbox4.Add(self.buttonnew,0,wx.ALIGN_CENTER)
        hbox4.AddSpacer(7)
        hbox4.Add(self.buttonstats,0,wx.ALIGN_CENTER)
        hbox4.AddSpacer(7)
        hbox4.Add(self.buttonback,0,wx.ALIGN_CENTER)
        hbox4.AddSpacer(7)
        hbox4.Add(self.buttonforward,0,wx.ALIGN_CENTER)
        hbox4.AddSpacer(7)
        hbox4.Add(wx.StaticText(panel,-1,label="RIGHT: ", style=wx.ALIGN_CENTER),0,wx.ALIGN_CENTER)
        hbox4.Add(self.buttonrispostegiuste,0,wx.ALIGN_CENTER)
        hbox4.AddSpacer(4)
        hbox4.Add(wx.StaticText(panel,-1,label="WRONG: ", style=wx.ALIGN_CENTER),0,wx.ALIGN_CENTER)
        hbox4.Add(self.buttonrispostesbagliate,0,wx.ALIGN_CENTER)
        hbox4.AddSpacer(7)
        hbox4.Add(self.buttonreloadtext,0,wx.ALIGN_CENTER)
        hbox4.AddSpacer(7)
        hbox4.Add(self.buttonvalidate,0,wx.ALIGN_CENTER)
        
        hbox4.AddSpacer(7)
        hbox4.Add(self.buttonsave,0,wx.ALIGN_CENTER)
        hbox4.AddSpacer(7)
        hbox4.Add(self.buttonreset,0,wx.ALIGN_CENTER)
        hbox4.AddSpacer(7)
        hbox4.Add(wx.StaticText(panel,-1,label="SPEED(ms)    ", style=wx.ALIGN_CENTER),0,wx.ALIGN_CENTER)
        hbox4.Add(self.sc,0,wx.ALIGN_CENTER)
        hbox4.AddSpacer(7)
        hbox4.Add(self.new,0,wx.ALIGN_CENTER)
        """CHIAMARE EXPAND su questo sizer per renderlo dinamicamente
        ridimensionabile"""

        hbox4.AddStretchSpacer(1)


        vsizer.AddStretchSpacer(2)
        vsizer.Add(hbox2,0,wx.EXPAND|wx.ALIGN_CENTER) 
                   
        vsizer.Add(hbox1,0,wx.EXPAND|wx.ALIGN_CENTER)
        vsizer.AddStretchSpacer(1)
        vsizer.Add(hbox5,0,wx.EXPAND|wx.ALIGN_CENTER)
        vsizer.AddStretchSpacer(1)
        vsizer.Add(hbox4,0,wx.EXPAND|wx.ALIGN_CENTER)
        vsizer.AddStretchSpacer(2)
        panel.SetSizer(vsizer)
        
       
        #LAYOUT DEL MENU
        
        menuFile = wx.Menu()
        menuFile.Append(1, "&About...")
        menuFile.Append(2, "&Carica Liste...")
        menuFile.Append(4, "Carica Da &File..")
        menuFile.Append(5, "&Interactive Mode..")

        menuFile.AppendSeparator()
        menuFile.Append(3, "E&xit")
        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, "&File")
        self.SetMenuBar(menuBar)

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.SetStatusText\
        ("Versione Sperimentale per utilizzo non terapeutico",1)
        
        #EVENTI MENU /bindings
        
        self.Bind(wx.EVT_MENU, self.OnAbout, id=1)
        self.Bind(wx.EVT_MENU, self.OnCaricaListe,id=2)
        self.Bind(wx.EVT_MENU, self.OnCaricaDaFile,id=4)
        self.Bind(wx.EVT_MENU, self.OnInteractiveMode,id=5)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=3)

        self.Layout()
        
    def OnQuit(self, evt):
        self.Close()
    def OnInteractiveMode(self,evt):
        
                
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
        self.Hide()
        InteractiveFrame().Show()
        
    def OnCaricaDaFile(self,evt):
        try:
            dlg = wx.FileDialog(self.panel, "Scegli Lista...",
             cartella_liste, style=wx.OPEN, wildcard="*.*")
        except:
            dlg = wx.FileDialog(self.panel, "Scegli Lista...",
            defaultDir=".", style=wx.OPEN, wildcard="*.*")      
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.ReadFile()
            #self.SetTitle(self.title + ' -- ' + self.filename)
        dlg.Destroy()

    def ReadFile(self):
        self.lista_immagini = 0
        self.indice_lines=0       
        self.foreground_colors=0
        f = open(self.filename, 'r+')
        self.righe = eval (f.read())           
        f.close()
        self.update()
    def OnReset(self,evt): 
        try:
            "reset!"            
            self.lista_immagini = 0
            self.indice_lines=0       
            self.foreground_colors=0
            self.rispostegiuste= 0
            self.rispostesbagliate= 0
            self.buttonrispostegiuste.SetLabel(label=str(self.rispostegiuste))
            self.buttonrispostegiuste.SetLabel(label=str(self.rispostesbagliate))
            self.update()
        except:
            print "reset con except senza errori!"
            pass    
        

    def update(self):            
        self.immagine=zip(*self.righe) [0]
        self.lines=zip(*self.righe) [1]
        #self.t.SetLabel(self.lines[self.indice_lines])
        #SUPPORTO AD UNICODE CON chiamata di setlabel necessariamente con parametro esplicito (label=)
        self.test=self.lines[self.indice_lines]
        self.t.SetLabel(label=self.test)
        
        try:    
                    
            self.img = wx.Image(name= self.immagine[self.lista_immagini], 
                            type =wx.BITMAP_TYPE_ANY)
#        self.PhotoMaxSize = 500
#        
#        W = self.img.GetWidth()
#        H = self.img.GetHeight()
#        if W > H:
#            NewW = self.PhotoMaxSize
#            NewH = self.PhotoMaxSize * H / W
#        else:
#            NewH = self.PhotoMaxSize
#            NewW = self.PhotoMaxSize * W / H
#        self.img_resized = self.img.Scale(NewW,NewH)
            self.fototest=wx.BitmapFromImage(self.img)
            self.foto.SetBitmap(bitmap=self.fototest)
        except:
            pass
        colors=['brown','yellow','purple','blue','red','black']
        
        self.t.SetForegroundColour((random.choice(colors)))
        print "unhide!"
        self.t.Show()
 
        
        self.t.Layout()
        self.foto.Layout()
        self.hbox3.Layout()
        
        self.panel.Layout()        
        self.speed=self.sc.GetValue()
        wx.CallLater(self.speed, self.hide)
#            wx.CallLater(speed, self.update)
        #call later in if affinchè venga eseguito un numero finito di volte 
        #per evitare bug che non trova ultimo 
        #elemento di lista perchè lo cerca
        #in continuazione mentre si carica nuovo file di lista (si può legare generalizzando a 
        #len(indice liste iterate))
        
        #f.close()
#        SOLUZIONE PER LOOP INFINITO        
#        self.index = 0
#        
#        duration, label = DATA[self.index]
#        self.text.SetLabel(label)
#        self.index = (self.index + 1) % len(DATA)
#        self.Bind(wx.EVT_CHAR_HOOK, self.onKey)
    def hide(self):
        print "hide!"
        self.t.Hide()

    def OnNew(self,evt):
        self.user_name=wx.TextEntryDialog(self,message="Il tuo nome, per favore...", caption="I tuoi dati",
        defaultValue="")
        if self.user_name.ShowModal() == wx.ID_OK:
            self.nomeutente=self.user_name.GetValue()
            self.new.SetLabel(label=self.nomeutente)
            self.OnCaricaDaFile(evt)
    
    def OnEnterText(self, evt):
        print "text entered!"
        testo_risposta= self.answer.GetValue()
        try:        
            self.soluzioni=zip(*self.righe) [2]        
            testo_soluzione=self.soluzioni[self.indice_lines]
            if testo_risposta== testo_soluzione:
                if wx.Platform != '__WXGTK__':               
                   self.player = wx.Sound('tada.wav') 
                   self.player.Play()
                   print "esatto!"
                else:                        
                      mixer.init()
                      self.s = mixer.Sound('tada.wav')
                      self.s.play()
                      print "esatto su linux!"
            else:
                if wx.Platform != '__WXGTK__':               
                    self.player = wx.Sound('Windows_Hardware_Fail.wav') 
                    self.player.Play()        
                    print "errore!"    
                else:
                    mixer.init()
                    self.s = mixer.Sound('Windows_Hardware_Fail.wav')
                    self.s.play()                
                    print "errore su linux!"
        except:
            pass
    def OnForward(self, evt):

        print "fwd button pressed"
        if self.indice_lines<len(self.lines)-1:      
            self.indice_lines+=1
    
        if self.lista_immagini <len(self.immagine)-1: 
            self.lista_immagini+=1
        self.answer.Clear()
        #wx.CallLater(self.speed, self.update) 
        self.update()        
        #else:
#            evt.Skip()
    
    def OnBack(self, evt):
        print "back button pressed"
        if self.indice_lines == 0 and self.foreground_colors == 0 and self.lista_immagini == 0:
            self.OnZero()
        else:    
            if self.indice_lines <=len(self.lines)-1 and self.indice_lines != 0:      
                self.indice_lines-=1
    
            if self.lista_immagini <=len(self.immagine)-1 and self.lista_immagini != 0: 
                self.lista_immagini-=1
            self.answer.Clear()
        #wx.CallLater(self.speed, self.update) 
            self.update()
    def OnZero(self):
        print "back on zero!"        
                
        
    def OnReloadText(self,evt):
        print "reload text pressed"
        wx.CallLater(self.speed, self.hide)
        self.answer.Clear()
        self.update()
    def OnValidateText(self,evt):
        print "reload text pressed"
        testo_risposta= self.answer.GetValue()
        self.soluzioni=zip(*self.righe) [2]
        testo_soluzione=self.soluzioni[self.indice_lines]
        if testo_risposta== testo_soluzione:
            if wx.Platform != '__WXGTK__':               
               self.player = wx.Sound('tada.wav') 
               self.player.Play()
               self.rispostegiuste+=1
               self.buttonrispostegiuste.SetLabel(label=str(self.rispostegiuste))
               print "esatto!"
            else:                        
                  mixer.init()
                  self.s = mixer.Sound('tada.wav')
                  self.s.play()
                  self.rispostegiuste+=1
                  self.buttonrispostegiuste.SetLabel(label=str(self.rispostegiuste))
                  print "esatto su linux!"
        else:
            if wx.Platform != '__WXGTK__':               
                self.player = wx.Sound('Windows_Hardware_Fail.wav') 
                self.player.Play()
                self.rispostesbagliate+=1
                self.buttonrispostesbagliate.SetLabel(label=str(self.rispostesbagliate))
                print "errore!"    
            else:
                mixer.init()
                self.s = mixer.Sound('Windows_Hardware_Fail.wav')
                self.s.play()
                self.rispostesbagliate+=1
                self.buttonrispostesbagliate.SetLabel(label=str(self.rispostesbagliate))              
                print "errore su linux!"
        self.OnForward(evt)
    def OnSaveData(self,evt):
        
        self.basename = self.nomeutente+".txt"
        self.filename = os.path.join(cartella_utenti, self.basename)
        self.datafile= file(self.filename,'a+')
        print self.filename+" salvato!"
        #nome=str(self.user_name.GetValue())
        data=(datetime.date.today().strftime('%d/%m/%Y'))            
        self.listadati= [self.rispostegiuste,data]
#        for item in self.listadati:
#            print>>self.datafile, item        
        
        if os.stat(self.filename)[6]==0: #checks whether file is empty, then do not write the comma
        
            self.datafile.write(str(self.listadati))
            self.datafile.close()
        else:
            self.datafile.write(","+str(self.listadati))
            self.datafile.close()
    
    def OnStats(self,evt):
        
        try:
            self.basename = self.nomeutente+".txt"
            self.filename = os.path.join(cartella_utenti, self.basename)
    #        self.datafile= file(self.filename,'a+')
            f = open(self.filename, 'r+')
            #f = open('paolo.txt', 'r+')
            dati_utente = eval (f.read())
            f.close()
            punteggi=zip(*dati_utente)[0]
            date= zip(*dati_utente)[1]   
            
            N=len(date)
            x = np.arange(N)
            y = list(punteggi)
            width = 0.1
            xticks=list(date)
            plt.xticks(x,xticks)
            
            p1 = plt.bar(x, y,width, color='r')
            plt.ylabel('Punteggi')
            plt.title('Punteggi '+self.nomeutente)
    #               
            plt.show()
        except:
            print "not enough data!"
            if wx.Platform != '__WXGTK__':               
                    self.player = wx.Sound('Windows_Hardware_Fail.wav') 
                    self.player.Play()        
                    print "errore!"    
            else:
                mixer.init()
                self.s = mixer.Sound('Windows_Hardware_Fail.wav')
                self.s.play()                
                print "errore su linux!"
            wx.MessageBox("Not enough data to build stats!","Errore", wx.OK | wx.ICON_INFORMATION, self)
            
    def OnCaricaListe(self, event):
        try:
            il = wx.ImageList(32,32, True)
            for name in glob.glob("icon??.png"):
                bmp = wx.Bitmap(name, wx.BITMAP_TYPE_PNG)
                il_max = il.Add(bmp)
    
            self.list = wx.ListCtrl(self,-1,pos=(50,50),size=(650,350))
    
            # assign the image list to it
            self.list.AssignImageList(il, wx.IMAGE_LIST_NORMAL)
            names = ['pennarelli', 'cvc','bisillabiche', 'trisillabiche']
            names_item = 0
    
            for x in range(4):
                img = x % (il_max+1)
                           
                self.list.InsertImageStringItem(x, 
                        "%02s" % names[names_item], img)
                names_item+=1
            self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated,
            self.list)
        except:
            pass
        
        #event.Skip()
        
    def OnItemActivated(self, evt): 
        try:
            item = evt.GetItem()
            print "Item activated:", item.GetText()
            selected_list=item.GetText()
            
            if selected_list == "bisillabiche":
                selected_list=list (selected_list)
                selected_list = bisillabiche    
            elif selected_list == "trisillabiche":
                selected_list=list (selected_list)
                selected_list = trisillabiche
            elif selected_list == "cvc":
                selected_list=list (selected_list)
                selected_list = cvc
            elif selected_list == "pennarelli":
                selected_list=list (selected_list)
                selected_list = pennarelli
            indice_lista=0    
            self.list.Hide()
            conto = 0        
            #for elemento in selected_list:
                #wx.StaticText(panel,-1,selected_list[indice_lista],pos=(350,250),size=(400,180))
            while True:
                conto <= 80
                indice_lista <3
                t = wx.StaticText(None,-1,selected_list[indice_lista],pos=(350,250),size=(400,180))
                if conto < 80:
                    
                    t.Show()
                    conto +=1                
                else:    
                    t.Hide()
                    indice_lista+=1
                    conto= 0
                    if indice_lista >3:
                        break
        except:
            pass


            
            
              
    def OnAbout(self, event):
        wx.MessageBox("Kronoword 0.16 Alpha\nExperimental software developed by\nBattista A Faticato D Milone V", 
                "About Kronoword", wx.OK | wx.ICON_INFORMATION, self)
"""   what's new:_
   - wxcalllater per gui sempre attiva
   - csv files(vedere esempio correlato per cambiare formato liste per personalizzare
   durata singola voce lista) 
   -'migliorato' box sizer con layout method chiamato sui suoi children e proporzioni 
   per allineamento dinamico e compatibilità win-mac-linux (si spera)
   - inserimento immagini statico rescaled con max size (ed aspect ratio(?))
    
   """ 
              

'''TODO LIST: seguire file progetto con associazione immagini (creare formato 
dizionario e stimolo/rinforzo, 
 creare profilo utente e display log punteggi, http://wiki.wxpython.org/Widget%20Inspection%20Tool                
aggiunta cartella liste come path relativo al path assoluto di lavoro- studiare os.path.join
studiare live o non live photo zoom function
- sul dizionario vedere se creare database o loop di immagini e fare iterare su chiavi/valori di dizionario e far
iterare probabilmente l'item number come un indice; cominciare a vedere come si rappresenta l'errore nel testo
della parola, ad es. col sottolineato '''
"""AGGIORNAMENTO A FEBBRAIO 2013: se il formato deve essere la lista di liste, controllare anche il modulo csv
come descritto qui per avere un formato di input più usabile, ed inoltre resta sempre il problema di segnalare l'errore
: http://mail.python.org/pipermail/tutor/2009-October/072482.html parole chiave: strip, split,eval, repr, csv; vedere 
l'interoperabilità con il richtext editor del demo e vedere come randomizzarlo in maniera intelligente (finto random o random
controllato)
Inserire controllo per evitare bug quando si prova a caricare un nuovo elemento mentre sta ancora iterando
le vecchie liste: tipo se viene invocata una nuova funzione vai automaticamente in pausa (con un tasto o 
gestire la cosa con un'eccezione...eccezione non sembra efficace poichè l'errore sembra venire da fuori python
, forse la sol. è il (multi)threading, o cercare di sveltire il processo di caricamento/elaborazione delle immagini

SLIDER non multipiattaforma: vedere come rimpiazzarlo o mettere al suo posto lo spinner?(slider non funziona su ubuntu)
CODICE BARRA SPAZIO anche esso non multipiattaforma? controllare (avanzamento con spazio non funziona su ubuntu)
FARSI SESSIONE DI DEBUG CON Pdb o altro; vedere come debuggare interattivamente variabili interne a classe

SPINNER: se premo enter esce il popup di "about"?, aggiustare font

NOTE: le immagini devono avere tutte la stessa dimensione, devono restare sullo schermo per tot ms, e poi sparire(hide)
ok, compatibilità raggiunta con ubuntu (solo ridimensionare a 400x400 per netbook)
al posto di segnaposto green.jpg, potrebbe apparire un msg di indicazioni iniziale, tipo come caricare liste
(da valutare se si può fare one-shot, poichè rischierebbe di rimanere evidente in navigazione agli estremi lista)
vedere di portare su piattaforme mobili, anche symbian- vedi sito offline
PULSANTE RELOAD TEXT (RELOAD IMAGE) per mostrare di nuovo testo
X- cancella testo textctrl quando si va avanti e nel reload text?  
- settare controllo volume con peak meter (si può utilizzare pygame)
- animazione visuale che dice bravo con personaggino random etc + contatore
- grafico con colonne giusto e sbagliato (matplotlib), contatore su monitor di arduino(;-))
- sessione utente con memorizzazione risultati 
x cambiare soluzione ultimo quesito così non dà "giusto!"
- vedere perchè si sposta un poco grafica dopo il primo "forward!" in win
- aggiustare fonts e grafica in generale, inserire materiali faticato
PERCHE' per ora ho scelto di usare pygame:
wx.sound /wx.soundfromdata non sono multipiattaforma: silenzio su ubuntu, soundfromdata non funziona e dà 
errori su mac os x 10.4.11
- in win dà rumore di sbagliato anche quando si preme solo "reload text", senza inserire niente (vedere eventi 
chiamati)
- piccole freccine tipo spinner nel wx textctrl all'inizio su win
- vedere altre soluzioni sia per plotting che per user session, per plotting o c'è pyplot in wx o matplotlib
http://stackoverflow.com/questions/10737459/embedding-a-matplotlib-figure-inside-a-wxpython-panel
x magari si potrebbe dare al file il nome utente e semplificare struttura dati salvando solo dati utente nel file
senza nome, più facile anche da plottare
su struttura dati utente:
http://stackoverflow.com/questions/2222189/printing-to-a-file-from-a-list-of-lists-in-python
x mostrare nome utente in static text in gui... 
- disabilitare scrittura in wxtextctrl (inserimento soluzioni) prima di caricare lista:togli read only e (rimettilo 
alla fine?): EDIT: pare che si possa cambiare questo stile dinamicamente solo sotto GTK 
- cercare di utlizzare "plot_date" al posto di plot per fargli fare parsing di date e far
quindi comprendere il significato delle date, che se si modifica data il sw non fa che metterle 
in fila; 
- quando si preme "new", il test va resettato automaticamente(?)
x aggiungere un pulsante "reset" 
- aggiungere messaggio sonoro di errore come in test sul pulsante stats + messaggio di "not enough data!" per 0,1 
risultati memorizzati (no plotting, vedere come si potrebbe fare!)
- testare compatibilità mac linux
- farlo testare ad antonella stefano daniela altre logs 
- studiarsi bene spyder o altre gui per aumentare produttività 
"""


if __name__ == '__main__':

    app = wx.App(None)
    frame = MyFrame(None,-1)
    frame.SetTitle('Kronoword DEMO 0.16 Alpha')
    frame.SetSize((1024,768))    
    frame.Center()
    frame.Layout()    
    frame.Show()
    
#    import wx.lib.inspection
#    wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
  
