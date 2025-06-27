# game-animator

Библиотека для создания анимированных спрайтов в pygame и расширенными возможностями управления анимацией.

## Описание

game-animator предоставляет высокоуровневый API для работы с анимированными персонажами в игровых проектах на pygame. Библиотека поддерживает загрузку спрайт-листов, автоматическое управление кадрами анимации, зеркалирование спрайтов.

## Основные возможности

- Полная совместимость с pygame.sprite.Sprite и pygame.sprite.Group
- Поддержка больших спрайт-листов с автоматическим парсингом кадров
- Гибкая система выбора кадров анимации (диапазоны, отдельные кадры)
- Автоматическое и ручное управление направлением спрайтов
- Масштабирование спрайтов
- Система управления скоростью анимации
- Инструменты отладки для визуализации структуры спрайт-листов

## Установка

Убедитесь, что у вас установлен pygame:

```bash
pip install pygame
```

Скопируйте файл `game_animator.py` в директорию вашего проекта.

## Быстрый старт

```python
import pygame
from game_animator import AnimatedCharacter

pygame.init()
screen = pygame.display.set_mode((800, 600))

# Создание анимированного персонажа
hero = AnimatedCharacter(x=400, y=300)

# Загрузка спрайт-листа
hero.load_master_sprite_sheet("sprites.png", frame_width=64, frame_height=64)

# Добавление анимаций
hero.add_animation_from_range("idle", 1, 4, speed=15)
hero.add_animation_from_range("run", 5, 12, speed=8)

# Запуск анимации
hero.play_animation("idle")

# Основной цикл
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    hero.update()
    
    screen.fill((0, 0, 0))
    screen.blit(hero.image, hero.rect)
    pygame.display.flip()
    
    clock.tick(60)

pygame.quit()
```

## API Reference

### Класс AnimatedCharacter

#### Конструктор

```python
AnimatedCharacter(x=0, y=0, scale=1.0, direction_mode=AUTO_FLIP)
```

**Параметры:**
- `x, y` (int): Начальная позиция персонажа
- `scale` (float): Масштаб спрайта (1.0 = оригинальный размер)
- `direction_mode` (int): Режим управления направлением спрайта

**Режимы направления:**
- `AnimatedCharacter.AUTO_FLIP`: Автоматическое зеркалирование при движении влево
- `AnimatedCharacter.NO_FLIP`: Отключение зеркалирования
- `AnimatedCharacter.SEPARATE_DIRECTIONS`: Использование отдельных спрайтов для разных направлений

#### Методы загрузки спрайтов

```python
load_master_sprite_sheet(filename, frame_width, frame_height)
```

Загружает спрайт-лист и автоматически разбивает его на кадры.

**Параметры:**
- `filename` (str): Путь к файлу спрайт-листа
- `frame_width, frame_height` (int): Размеры одного кадра в пикселях

```python
add_animation_from_range(name, start_frame, end_frame, speed=10, loop=True)
```

Создает анимацию из диапазона кадров.

**Параметры:**
- `name` (str): Имя анимации
- `start_frame, end_frame` (int): Номера первого и последнего кадра (нумерация с 1)
- `speed` (int): Скорость анимации (больше = медленнее)
- `loop` (bool): Зацикливание анимации

```python
add_animation_from_frames(name, frame_list, speed=10, loop=True)
```

Создает анимацию из списка конкретных кадров.

```python
add_directional_animation(base_name, left_frames, right_frames, speed=10, loop=True)
```

Добавляет анимации для разных направлений (требует SEPARATE_DIRECTIONS режим).

#### Методы управления анимацией

```python
play_animation(name)
```

Запускает указанную анимацию.

```python
update()
```

Обновляет текущий кадр анимации. Должен вызываться в каждом кадре игрового цикла.

```python
is_animation_finished()
```

Возвращает True, если текущая анимация завершена (для незацикленных анимаций).

#### Методы позиционирования

```python
move(dx, dy)
```

Перемещает персонажа на указанное смещение.

```python
set_position(x, y)
```

Устанавливает абсолютную позицию персонажа.

```python
set_facing_direction(direction)
```

Устанавливает направление персонажа ("left" или "right").

#### Утилиты

```python
show_frame_grid()
```

Отображает окно с визуализацией всех кадров спрайт-листа с номерами.

```python
set_scale(scale)
```

Изменяет масштаб спрайта во время выполнения.

### Класс GameAnimator

Расширенная версия pygame.sprite.Group для управления группами анимированных персонажей.

```python
animator = GameAnimator()
animator.add(hero1, hero2, hero3)
animator.update()
animator.draw(screen)
```

## Примеры использования

### Создание персонажа с управлением

```python
import pygame
from game_animator import AnimatedCharacter

pygame.init()
screen = pygame.display.set_mode((800, 600))

hero = AnimatedCharacter(x=400, y=300, scale=2.0)
hero.load_master_sprite_sheet("platformer_sprites.png", 64, 64)

# Настройка анимаций
hero.add_animation_from_range("idle", 1, 4, speed=15)
hero.add_animation_from_range("run", 5, 12, speed=8)
hero.add_animation_from_range("jump", 43, 48, speed=12)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        hero.move(-5, 0)
        hero.play_animation("run")
    elif keys[pygame.K_RIGHT]:
        hero.move(5, 0)
        hero.play_animation("run")
    elif keys[pygame.K_SPACE]:
        hero.play_animation("jump")
    else:
        hero.play_animation("idle")
    
    hero.update()
    
    screen.fill((135, 206, 235))
    screen.blit(hero.image, hero.rect)
    pygame.display.flip()
    
    clock.tick(60)

pygame.quit()
```

### Работа с группами спрайтов

```python
from game_animator import AnimatedCharacter, GameAnimator

# Создание группы анимированных персонажей
characters = GameAnimator()

# Добавление нескольких персонажей
for i in range(5):
    character = AnimatedCharacter(x=i*100, y=300)
    character.load_master_sprite_sheet("enemy_sprites.png", 32, 32)
    character.add_animation_from_range("patrol", 1, 8, speed=10)
    character.play_animation("patrol")
    characters.add(character)

# В игровом цикле
characters.update()
characters.draw(screen)

# Проверка коллизий
collisions = pygame.sprite.spritecollide(player, characters, False)
```

### Отладка спрайт-листов

```python
# Для отладки и понимания структуры спрайт-листа
hero = AnimatedCharacter()
hero.load_master_sprite_sheet("sprites.png", 64, 64)
hero.show_frame_grid()  # Покажет окно с пронумерованными кадрами
```

## Требования

- Python 3.6+
- pygame 2.0+

## Структура спрайт-листов

Библиотека ожидает, что спрайт-листы организованы в виде сетки. Нумерация кадров начинается с 1 и идет слева направо, сверху вниз:

![platformer_sprites_base](https://github.com/user-attachments/assets/b4f79d7d-dddb-4e6a-add6-35ce6621ebb4)

## Производительность

- Все кадры анимации загружаются в память при инициализации
- Анимация работает через переключение между предварительно загруженными поверхностями
- Масштабирование выполняется один раз при создании анимации
- Зеркалирование кэшируется для оптимизации производительности
