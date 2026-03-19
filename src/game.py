import sys
import pygame

from inputHandler import InputHandler
from PhysicsSystem import PhysicsSystem
from CollisionSystem import CollisionSystem
from renderSystem import RenderSystem

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class Game:
    def __init__(self):
        """Construtor da classe que inicializa o jogo e cria os recursos básicos"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        # Criando uma instância da classe Ship para representar a nave espacial
        self.ship = Ship(self.screen, self.settings)

        # Mudando a cor do plano de fundo em RGB
        self.bg_color = self.settings.bg_color

        self.bullets = (
            pygame.sprite.Group()
        )  # Cria um grupo para armazenar os projéteis disparados pela nave

        self.aliens = (
            pygame.sprite.Group()
        )  # Cria um grupo para armazenar os alienígenas presentes no jogo

        # Sistemas
        self.input_handler = InputHandler(self)
        self.physics = PhysicsSystem(self)
        self.collision = CollisionSystem(self)
        self.renderer = RenderSystem(self)

    def run(self) -> None:
        """Loop principal do jogo."""

        self.create_fleet()

        while True:
            self.input_handler.handle()
            self.physics.update()
            self.collision.check()
            self.renderer.render()

    def create_fleet(self) -> None:
        """Cria a frota inicial de alienígenas."""

        alien = Alien(self.screen, self.settings)
        alien_width = alien.rect.width
        alien_height = alien.rect.height

        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        available_space_y = (
            self.settings.screen_height
            - (3 * alien_height)
            - self.ship.rect.height
        )
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number: int, row_number: int) -> None:
        """Cria um único alienígena e posiciona na frota."""

        alien = Alien(self.screen, self.settings)

        alien_width = alien.rect.width
        alien_height = alien.rect.height

        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x

        alien.rect.y = alien_height + 2 * alien_height * row_number

        self.aliens.add(alien)


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()