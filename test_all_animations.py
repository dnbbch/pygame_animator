import pygame
from game_animator import AnimatedCharacter

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Тест всех анимаций - нажимайте цифры!")

# Создаём героя
hero = AnimatedCharacter(x=500, y=350, scale=3.0)

# Загружаем спрайт-лист
hero.load_master_sprite_sheet("platformer_sprites_base.png", frame_width=64, frame_height=64)

# Показываем сетку для проверки
hero.show_frame_grid()

# Добавляем ВСЕ анимации согласно описанию:
# Stance (4 frames) - кадры 1-4
hero.add_animation_from_range("stance", 1, 4, speed=20)

# Run (8 frames) - кадры 5-12  
hero.add_animation_from_range("run", 5, 12, speed=8)

# Swing weapon (4 frames) - кадры 13-16
hero.add_animation_from_range("swing", 13, 16, speed=10)

# Block (2 frames) - кадры 17-18
hero.add_animation_from_range("block", 17, 18, speed=15)

# Hit and Die (6 frames) - кадры 19-24
hero.add_animation_from_range("hit_die", 19, 24, speed=12)

# Cast spell (4 frames) - кадры 25-28
hero.add_animation_from_range("cast", 25, 28, speed=15)

# Shoot bow (4 frames) - кадры 29-32
hero.add_animation_from_range("shoot", 29, 32, speed=12)

# Walk (8 frames) - кадры 33-40
hero.add_animation_from_range("walk", 33, 40, speed=10)

# Duck (2 frames) - кадры 41-42
hero.add_animation_from_range("duck", 41, 42, speed=20)

# Jump and Fall (6 frames) - кадры 43-48
hero.add_animation_from_range("jump", 43, 48, speed=8)

# Ascend stairs (8 frames) - кадры 49-56
hero.add_animation_from_range("stairs_up", 49, 56, speed=10)

# Descend stairs (8 frames) - кадры 57-64
hero.add_animation_from_range("stairs_down", 57, 64, speed=10)

# Stand (1 frame) - последний кадр
hero.add_animation_from_range("stand", 65, 65, speed=60)

# Запускаем первую анимацию
current_animation = "stance"
hero.play_animation(current_animation)

# Словарь для переключения анимаций
animations = {
    pygame.K_1: "stance",
    pygame.K_2: "run", 
    pygame.K_3: "swing",
    pygame.K_4: "block",
    pygame.K_5: "hit_die",
    pygame.K_6: "cast",
    pygame.K_7: "shoot",
    pygame.K_8: "walk",
    pygame.K_9: "duck",
    pygame.K_0: "jump",
    pygame.K_q: "stairs_up",
    pygame.K_w: "stairs_down",
    pygame.K_e: "stand"
}

# Основной цикл
clock = pygame.time.Clock()
running = True

print("\n🎮 УПРАВЛЕНИЕ:")
print("1 - Stance (стойка)")
print("2 - Run (бег)")
print("3 - Swing weapon (удар)")
print("4 - Block (блок)")
print("5 - Hit and Die (урон)")
print("6 - Cast spell (магия)")
print("7 - Shoot bow (стрельба)")
print("8 - Walk (ходьба)")
print("9 - Duck (приседание)")
print("0 - Jump (прыжок)")
print("Q - Stairs up (вверх по лестнице)")
print("W - Stairs down (вниз по лестнице)")
print("E - Stand (стоять)")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in animations:
                current_animation = animations[event.key]
                hero.play_animation(current_animation)

    hero.update()
    
    screen.fill((64, 64, 64))  # Серый фон
    screen.blit(hero.image, hero.rect)
    
    # Показываем информацию
    font = pygame.font.Font(None, 42)
    text = f"Текущая анимация: {current_animation.upper()}"
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))
    
    # Показываем управление
    font_small = pygame.font.Font(None, 24)
    controls = [
        "1-Stance  2-Run  3-Swing  4-Block  5-Hit&Die",
        "6-Cast  7-Shoot  8-Walk  9-Duck  0-Jump",
        "Q-StairsUp  W-StairsDown  E-Stand"
    ]
    
    for i, control in enumerate(controls):
        control_surface = font_small.render(control, True, (200, 200, 200))
        screen.blit(control_surface, (10, 60 + i * 25))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit() 