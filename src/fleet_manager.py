import pygame
import sys

from alien import Alien

class FleetManager:
    """Responsável por criar e gerenciar a frota de alienígenas."""
    def __init__(self, screen, settings, ship, alien_class=Alien) -> None:
        self.screen = screen
        self.settings = settings
        self.ship = ship
        self.aliens = pygame.sprite.Group()

    def _create_alien(self, alien_number: int, row_number: int, alien_width: int, alien_height: int) -> None:
        """Método focado exclusivamente em instanciar, posicionar e adicionar o alienígena."""
        alien = Alien(self.screen, self.settings)
        
        # Calcula a posição X e Y com base nos índices da grade
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.y = alien_height + 2 * alien_height * row_number
        alien.rect.y = alien.y
        
        # Adiciona o novo alienígena ao grupo da frota
        self.aliens.add(alien)

    def create_fleet(self):
        """Cria uma frota de alienígenas."""
        # Cria um alienígena temporário apenas para calcular o espaço e tamanhos
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

        # Monta a grade da frota delegando a criação individual
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number, alien_width, alien_height)

    def _update_aliens(self) -> None:
        """Verifica se a frota de alienígenas está em uma borda, então atualiza as posições."""
        self._check_fleet_edges()
        self.aliens.update()
        self._check_ship_collision()

    def _check_fleet_edges(self) -> None:
        """Responde apropriadamente se algum alienígena tiver alcançado uma borda."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self) -> None:
        """Desce a frota e muda sua direção."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_ship_collision(self) -> None:
        """Verifica se a nave colidiu com algum alienígena."""
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("A nave foi atingida!")
            sys.exit()