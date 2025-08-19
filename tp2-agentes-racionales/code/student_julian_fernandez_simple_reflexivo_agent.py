#para que sea reflexivo simple no puedo usar memoria ni usar conocimientos del entorno
#entonces voy a crear un agente random pero que limpie solo si la casilla esta sucia

import sys  
import os  
import random  
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  
from base_agent import BaseAgent  
  
class JulianFernandezRandomAgent(BaseAgent):  
    def __init__(self, server_url="http://localhost:5000", **kwargs):  
        super().__init__(server_url, "JulianFernandezRandomAgent", **kwargs)  
      
    def get_strategy_description(self):  
        return "Random movement and cleaning strategy"  
      
    def think(self):  
        if not self.is_connected():  
            return False  
          
        perception = self.get_perception()  
        if not perception or perception.get('is_finished', True):  
            return False  
          
        # Lista de todas las acciones posibles  
        actions = [self.up, self.down, self.left, self.right, self.idle]  
          
        # Seleccionar una acción aleatoria  
        if perception.get('is_dirty',False):
            action = self.suck
            return action()
        else:
            random_action = random.choice(actions)  
            return random_action()