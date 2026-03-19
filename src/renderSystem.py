

import pygame


class RenderSystem:
    """Sistema responsável por renderizar todos os elementos na tela."""

    def __init__(self, game) -> None:
        """Inicializa o sistema de renderização com acesso ao estado do jogo."""
        self.game = game

    def render(self) -> None:
        """Desenha todos os elementos do jogo na tela."""
        screen = self.game.screen

        # Preenche o fundo
        screen.fill(self.game.settings.bg_color)

        # Desenha a nave
        self.game.ship.blitme()

        # Desenha os alienígenas
        self.game.aliens.draw(screen)

        # Desenha os projéteis
        for bullet in self.game.bullets.sprites():
            bullet.draw_bullet()

        # Atualiza a tela
        pygame.display.flip()