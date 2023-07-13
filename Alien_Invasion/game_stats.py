import json


class GameStats():
    """Armazena dados estatisticos da Invasão Alienígena"""

    def __init__(self, ai_settings):
        """Inicia os dados estatisticos."""
        self.ai_settings = ai_settings
        self.reset_stats()
        #A pontuação máxima jamais deverá ser reiniciada
        filename = 'Alien_Invasion/record.json'
        with open(filename) as f_obj:
            self.high_score = json.load(f_obj)
            
        #Inicia a Invasão Alienígena em um estado ativo
        self.game_active = False

    def reset_stats(self):
        """Inicializa os dados estatísticos que podem mudar durante o jogo"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
