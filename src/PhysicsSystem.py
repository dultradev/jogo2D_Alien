class PhysicsSystem:
    def __init__(self, game):
        self.game = game
     
    def update(self) -> None:
        """Atualiza o estado físico do jogo (movimento e posições)."""

        # Atualiza a posição da nave
        self.game.ship.update()

        # Atualiza projéteis
        self._update_bullets()

        # Atualiza alienígenas
        self._update_aliens()

    def _update_bullets(self) -> None:
        """Atualiza a posição dos projéteis e remove os que saíram da tela."""

        self.game.bullets.update()

        for bullet in self.game.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.game.bullets.remove(bullet)

    def _update_aliens(self) -> None:
        """Atualiza a posição dos alienígenas e gerencia bordas da frota."""

        self._check_fleet_edges()
        self.game.aliens.update()

    def _check_fleet_edges(self) -> None:
        """Verifica se algum alienígena atingiu a borda da tela."""

        for alien in self.game.aliens.sprites():
            if alien.check_edges():
                for alien in self.game.aliens.sprites():
                    alien.rect.y += self.game.settings.fleet_drop_speed

                self.game.settings.fleet_direction *= -1
                break