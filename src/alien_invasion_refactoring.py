import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Gerencia o jogo e seus comportamentos."""


    def create_fleet(self):
        """Cria uma frota de alienígenas."""
        # Cria um alienígena e calcula o número de alienígenas em uma linha
        # O espaçamento entre os alienígenas é igual a um alienígena
        alien = Alien(self.screen, self.settings)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        ship_height = self.ship.rect.height
        available_space_y = (
            self.settings.screen_height - (3 * alien_height) - ship_height
        )
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            # Cria a primeira linha de alienígenas
            for alien_number in range(number_aliens_x):
                # Cria um alienígena e o posiciona na linha
                alien = Alien(self.screen, self.settings)
                alien.x = alien_width + 2 * alien_width * alien_number
                alien.rect.x = alien.x
                alien.y = alien_height + 2 * alien_height * row_number
                alien.rect.y = alien.y
                self.aliens.add(alien)

   

   

    

   

    
    def _update_bullets(self) -> None:
        """Atualiza a posição dos projéteis e remove os que saíram da tela."""

        self.bullets.update()  # Atualiza a posição de cada projétil no grupo de projéteis

        for bullet in self.bullets.copy():  # Verifica se algum projétil saiu da tela
            if bullet.rect.bottom <= 0:  # Se o projétil saiu da tela
                self.bullets.remove(bullet)  # Remove o projétil do grupo de projéteis

        # Verifica as colisões entre projéteis e alienígenas
        pygame.sprite.groupcollide(
            self.bullets,
            self.aliens,
            True,
            True,
        )

    def _update_aliens(self) -> None:
        """Atualiza a posição da frota de alienígenas e verifica colisões."""

        self._check_fleet_edges()
        self.aliens.update()  # Atualiza a posição de cada alienígena no grupo de alienígenas

        # Verifica se a nave colidiu com algum alienígena
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("A nave foi atingida!")  # Imprime mensagem no console
            sys.exit()  # Encerra o jogo

    def _check_fleet_edges(self) -> None:
        """Verifica se algum alienígena atingiu a borda da tela."""

        for alien in self.aliens.sprites():
            if alien.check_edges():
                for alien in self.aliens.sprites():
                    alien.rect.y += self.settings.fleet_drop_speed  # Move cada alienígena para baixo

                self.settings.fleet_direction *= -1  # Inverte a direção da frota
                break

    def _update_screen(self) -> None:
        """Atualiza todos os elementos visuais da tela."""

        # Redesenha a tela a cada passagem pelo laço
        self.screen.fill(self.bg_color)

        # Redesenha a nave em sua posição atual
        self.ship.blitme()

        # Desenha os alienígenas presentes no grupo de alienígenas na tela
        self.aliens.draw(self.screen)

        # Desenha cada projétil na tela
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Torna visível a tela mais recente
        pygame.display.flip()


if __name__ == "__main__":
    alien_invasion = AlienInvasion()
    alien_invasion.run_game()
