import sys
import pygame

class AlienInvasion:
    """Gerencia o loop principal do jogo e delega os comportamentos usando DIP."""

    def __init__(self, screen, settings, ship, bullet_manager, fleet_manager, event_handler, renderer):
        """
        As dependências agora são injetadas (DIP). 
        A classe não sabe COMO elas foram criadas, apenas sabe COMO usá-las.
        """
        pygame.init()
        self.screen = screen
        self.settings = settings
        self.ship = ship
        
        # Gerenciadores injetados externamente
        self.bullet_manager = bullet_manager
        self.fleet_manager = fleet_manager
        self.event_handler = event_handler
        self.renderer = renderer

    def _update_game_state(self) -> None:
        """Atualiza o estado do jogo delegando para os gerenciadores abstratos."""
        self.ship.update()
        # LSP garantido: fleet_manager.aliens pode conter qualquer tipo de Alien
        self.bullet_manager._update_bullets(self.fleet_manager.aliens)
        self.fleet_manager._update_aliens()

    def run_game(self) -> None:
        """Executa o loop principal do jogo."""
        self.fleet_manager.create_fleet() 

        while True:
            self.event_handler._check_events()
            self._update_game_state()
            self.renderer._render_screen()


# O Bloco Principal assume a responsabilidade de "orquestrar" a criação (Composição Root)
if __name__ == "__main__":
    from settings import Settings
    from ship import Ship
    from bullet_manager import BulletManager
    from fleet_manager import FleetManager
    from game_events import GameEventHandler
    from game_renderer import GameRenderer
    from fast_alien import FastAlien  # Ou Alien normal

    # 1. Configurações básicas de tela e recursos
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # 2. Inicialização dos componentes do jogo
    ship = Ship(screen, settings)
    
    # 3. Criação dos gerenciadores independentes
    bullet_manager = BulletManager(screen, settings, ship)
    
    # ISP/LSP: FleetManager recebe a classe de Alien que desejar rodar (Aberto para extensão)
    fleet_manager = FleetManager(screen, settings, ship, FastAlien)
    
    event_handler = GameEventHandler(ship, bullet_manager)
    
    # ISP: Passamos diretamente o grupo de sprites que o renderizador precisa desenhar
    renderer = GameRenderer(
        screen,
        settings.bg_color,
        ship,
        bullet_manager.bullets,
        fleet_manager.aliens,
    )

    # 4. Injeção das dependências na classe principal
    alien_invasion = AlienInvasion(
        screen=screen,
        settings=settings,
        ship=ship,
        bullet_manager=bullet_manager,
        fleet_manager=fleet_manager,
        event_handler=event_handler,
        renderer=renderer
    )
    
    alien_invasion.run_game()