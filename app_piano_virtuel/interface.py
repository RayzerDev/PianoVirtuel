# Modules externes
from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
from osc import OSC
import os

class Fenetre(Tk):
    
    COLOR_BACK = '#2B2F2D'
    COLOR_BLACK = '#000000'
    COLOR_FONT = '#DF4F4F'
    
    def __init__(self, titre, dim = (1280,720)):
        """
        """
        # Initialisation des variables
        self.dim, self.titre, self.frame_active, self.statut_osc = dim, titre, None, False

        # Initialisation de la fenêtre
        Tk.__init__(self)
        self.title(self.titre)
        dimension_fenetre = "%dx%d" % (self.dim[0], self.dim[1])
        self.geometry(dimension_fenetre)
        #self['bg'] = self.COLOR_BACK

        self.l_synths = [':piano', ':saw', '']

        self.w_statut_osc = Label(self, text = "Appuyez sur le bouton 'Connectez-vous' afin de pouvoir utiliser le piano sur SonicPI")
        self.w_statut_osc.place(x = self.dim[0]/3, y = 30)

        self.onglet_piano()
        
    def frame_destroy(self):
        """
        Permets de supprimer la frame actuel et de passer à la frame voulu.
        """
        if self.frame_active:
            self.frame_active.destroy()
            
    def onglet_piano(self):
        """
        """
        self.frame_destroy()
        
        # Mise en place de la frame d'accueil
        self.frame_piano = Frame(self, width = self.dim[0]-10, height = self.dim[1]-100, bg = Fenetre.COLOR_BACK)
        self.frame_active = self.frame_piano
        self.frame_piano.place(x= 5, y= 90)

        self.partie_configuration()

        self.mainloop()

    def partie_touches(self, l_notes = ['C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']):
        """
        """
        self.w_statut_osc['text'] = "Vous êtes connecté en OSC sur la destination : " + str(self.connexion.ip) + ":" + str(self.connexion.port)
        self.w_statut_osc.place(x = self.dim[0]/3 + 50, y = 30)
        
        self.frame_touches = Frame(self.frame_active, borderwidth = 5, width = self.dim[0]-10, height = 440, bg = Fenetre.COLOR_FONT)
        self.frame_touches.place(x= 0, y= 180)

        self.l_touches = []
        self.l_notes = l_notes

        for i in range(len(l_notes)):
            self.l_touches.append(TouchePiano(self, l_notes[i], 80*i+30))
            self.l_touches[i].afficher_touche()

        self.b_connexion_osc.destroy()

    def partie_configuration(self):
        """
        """
        self.frame_configuration = Frame(self.frame_active, borderwidth = 5, width = self.dim[0]-10, height = 180, bg = Fenetre.COLOR_BLACK)
        self.frame_configuration.place(x= 0, y= 0)
        
        self.b_connexion_osc = Button(self.frame_configuration, text = "Connectez-vous à SonicPI", command= self.connexion_osc)
        self.b_connexion_osc.place(x=5, y=20)
        
        self.l_box_synths = ttk.Combobox(self.frame_active, values = self.l_synths)
        self.l_box_synths.current(0)
        self.l_box_synths.place(x=10, y=60)

    def connexion_osc(self):
        """
        """
        self.connexion = OSC()
        self.partie_touches()
        
        process = os.popen('wmic process get description').read()
        if not 'sonic-pi.exe' in process:
            try:
                os.startfile("C:\Program Files\Sonic Pi\app\gui\qt\build\Release\sonic-pi.exe")
                return showinfo("Connexion réussi !", "Vous êtes bien connecté en OCS ! \n Lancement de SonicPI, configurez le piano et jouez !")
            
            except:
                return showerror("Connexion réussi !", "Vous êtes bien connecté en OCS ! \n Le lancement de SonicPI n'a pas réussi. Veuillez le lancer par vous même !")

    def envoi_note(self, note):

        return self.connexion.send_msg_osc('/note/', note)

class TouchePiano():

    def __init__(self, fenetre, note, pos_x):
        """
        """
        self.note = note
        self.pos_x = pos_x
        self.fenetre = fenetre
        self.couleur = '#FFFFFF'

    def afficher_touche(self):
        """
        """
        self.b_touches = Button(self.fenetre.frame_touches, text = self.note, height = 22, width = 10, command = self.jouer_note, bg = self.couleur)
        self.b_touches.place(x = self.pos_x, y = 50)

    def jouer_note(self):

        return self.fenetre.envoi_note(self.note)