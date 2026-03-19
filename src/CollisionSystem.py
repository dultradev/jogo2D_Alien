import sys

import pygame


class CollisionSystem:
    """Sistema responsável por detectar e tratar colisões no jogo."""

    def __init__(self, game) -> None:
        """Inicializa o sistema de colisão com acesso ao estado do jogo."""
        self.game = game

    def check(self) -> None:
        """Executa todas as verificações de colisão do jogo."""
        self._bullet_alien_collision()
        self._ship_alien_collision()

    def _bullet_alien_collision(self) -> None:
        """Verifica colisões entre projéteis e alienígenas."""
        pygame.sprite.groupcollide(
            self.game.bullets,
            self.game.aliens,
            True,
            True,
        )

    def _ship_alien_collision(self) -> None:
        """Verifica colisões entre a nave e alienígenas."""
        if pygame.sprite.spritecollideany(
            self.game.ship,
            self.game.aliens,
        ):
            print("A nave foi atingida!")
            sys.exit()
