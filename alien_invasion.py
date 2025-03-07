import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from gameStats import GameStats


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.game_active = True
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height),pygame.FULLSCREEN)
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.screen_width = self.screen.get_rect().width
        print(self.settings.screen_height,self.settings.screen_width)
        pygame.display.set_caption("Alien Invasion")
        
        #Create an instance to store game statistics.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self.background = self.settings.bg_color


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
                self._check_events() 
                if self.game_active:
                     
                  self.ship.update()
                  self._update_bullets()
                  self._update_alliens()

                self._update_screen()
                self.clock.tick(60)
    
    def _check_events(self):
        """Check for any events and return them."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                     self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                     self._check_keyup_events(event)

    def _update_screen(self):
        """Update the screen with the latest changes."""
        self.screen.fill(self.background)
        for bullet in self.bullets.sprites():
             bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        # Make the most recently drawn screen visible.
        pygame.display.flip()


    def _check_keydown_events(self,event):
        """Responds to keydown presses"""
        if event.key == pygame.K_RIGHT:
              self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
              self.ship.moving_left = True
        elif event.key == pygame.K_q:
              sys.exit()
        elif event.key == pygame.K_SPACE:
             self._fire_bullet()


    def _check_keyup_events(self,event):
          """Responds to keydown presses"""
          if event.key == pygame.K_RIGHT:
             self.ship.moving_right = False
          elif event.key == pygame.K_LEFT:
             self.ship.moving_left = False

    def _fire_bullet(self):
         """Create a new bullet and add it to the bullets group"""
         if len(self.bullets) < self.settings.bullet_allowed:  
           new_bullet = Bullet(self)
           self.bullets.add(new_bullet)
    
    def _update_bullets(self):
         """Update positon of bullets and get rid of old bullets.""" 
  
    
        # Update bullet position.
         self.bullets.update()
        
        # Look for alien-ship collisions.
         if pygame.sprite.spritecollideany(self.ship,self.aliens):
              print("Ship hit!!!")

        # Get rid of bullets that have disappeared
         for bullet in self.bullets.copy():
             if bullet.rect.bottom <= 0:
                  self.bullets.remove(bullet)
         self._check_bullet_alien_collision()
        
       

    def _check_bullet_alien_collision(self):
         
        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien
         collision = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)

         if not self.aliens:
              
              #Destroy existing bullets and create new fleet.
              self.bullets.empty()
              self._create_fleet()
         
    
    def _create_fleet(self):
      # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 6 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self,current_x,current_y):
        new_alien = Alien(self)
        new_alien.x = current_x
        new_alien.rect.x = new_alien.x
        new_alien.rect.y = current_y
        self.aliens.add(new_alien)
    
    def _update_alliens(self):
         self._check_fleet_edges()
         self.aliens.update()

         if pygame.sprite.spritecollideany(self.ship,self.aliens):
              self._ship_hit()

         self._check_aliens_bottom()
   
    def _check_fleet_edges(self):
         
         for alien in self.aliens.sprites():
              if alien.check_edges():
                   self._change_fleet_direction()
                   break
    
    def _change_fleet_direction(self):
         
         for alien in self.aliens.sprites():
              alien.rect.y += self.settings.fleet_drop_speed
         
         self.settings.fleet_direction *= -1 

    def _ship_hit(self):
         
         
         if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()
            #pause
            sleep(0.5)
         else:
            self.game_active = False
              


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
             if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break


          

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

