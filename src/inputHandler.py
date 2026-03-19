import sys
import pygame

from bullet import Bullet


class InputHandler:
    def __init__(self, game):
        self.game = game

    def handle(self) -> None:
        """Processa todos os eventos do jogo."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

            elif event.type == pygame.KEYUP:
                self._handle_keyup(event)

    def _handle_keydown(self, event: pygame.event.Event) -> None:
        """Detecta quando uma tecla é pressionada."""

        if event.key == pygame.K_RIGHT:
            self.game.ship.moving_right = True

        elif event.key == pygame.K_LEFT:
            self.game.ship.moving_left = True

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _handle_keyup(self, event: pygame.event.Event) -> None:
        """Detecta quando uma tecla é liberada."""

        if event.key == pygame.K_RIGHT:
            self.game.ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            self.game.ship.moving_left = False

    def _fire_bullet(self) -> None:
        """Cria um novo projétil se o limite permitido não foi atingido."""

        if len(self.game.bullets) < self.game.settings.bullet_allowed:
            new_bullet = Bullet(
                self.game.screen,
                self.game.settings,
                self.game.ship,
            )
            self.game.bullets.add(new_bullet)
