import sys
sys.path.insert(1, './pythonosc')

from pythonosc import udp_client
import time

class OSC():
    
    L_NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    
    def __init__(self, ip = '127.0.0.1', port = 4560):
        """
        """
        self.ip = ip
        self.port = port
        try:
            self.liaison = udp_client.SimpleUDPClient(self.ip , self.port)
            print('Connexion réussie !')
            # self.test_send()
        
        except:
            print('Connexion échouée..')        
    
    def test_send(self):
        """
        """
        try:
            for note in self.L_NOTES:
                time.sleep(0.3)
                self.send_msg_osc('/note/', note)
            return True
        
        except:
            return False
    
    def send_msg_osc(self, directory, msg):
        """
        """
        self.liaison.send_message(directory, msg)