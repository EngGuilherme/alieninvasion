
class Settings():
    """ Uma classe para armazenar todas as configurações da Invasão Alienígena."""

    def __init__(self):
        """Inicializa as configurações estáticas do jogo."""
        #Configurações da tela:
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (75,160,255)

        #Configurações da espaçonave
        self.ship_limit = 3

        #Configuração dos projéteis
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255,0,0
        self.bullets_allowed = 30

        #Configurações dos aliens        
        self.fleet_drop_speed = 5

        #A taxa com que a velocidade do jogo aumenta
        self.speedup_scale = 1.1

        #A taxa com que os pontos para cada alien aumentam
        self.score_scale = 10

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inicializa as configurações que mudam no decorrer do jogo."""
        self.ship_speed_factor = 1
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 1
        #fleet_direction igual a 1 representa a direita, -1 esquerda
        self.fleet_direction = 1
        #Pontuacao
        self.aliens_points = 10

    def increase_speed(self):
        """Aumenta as configurações de velocidade"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.aliens_points += self.score_scale




    