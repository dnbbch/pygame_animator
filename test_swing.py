import pygame
from game_animator import AnimatedCharacter

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Тест анимации: Swing Weapon (Удар оружием)")

# Создаём героя
hero = AnimatedCharacter(x=400, y=300, scale=3.0)

# Загружаем спрайт-лист
hero.load_master_sprite_sheet("platformer_sprites_base.png", frame_width=64, frame_height=64)

# Анимация Swing weapon: кадры 13-16 (4 stance + 8 run + 4 swing)
hero.add_animation_from_range("swing", 13, 16, speed=12)
hero.play_animation("swing")

# Основной цикл
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    hero.update()
    
    screen.fill((200, 50, 50))  # Красный фон
    screen.blit(hero.image, hero.rect)
    
    # Показываем информацию
    font = pygame.font.Font(None, 42)
    text = "SWING WEAPON (Удар оружием) - кадры 13-16"
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit() 