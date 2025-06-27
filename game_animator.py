import pygame
import json
import os

class AnimatedCharacter(pygame.sprite.Sprite):
    """
    Универсальный класс для создания анимированных персонажей
    Наследуется от pygame.sprite.Sprite для полной совместимости!
    
    Поддерживает ДВА режима:
    1. Отдельный спрайт-лист для каждой анимации
    2. Один большой спрайт-лист со всеми анимациями (автопарсинг)
    
    Поддерживает ТРИ режима направлений:
    1. AUTO_FLIP - автоматическое зеркалирование (по умолчанию)
    2. SEPARATE_DIRECTIONS - отдельные анимации для каждого направления
    3. NO_FLIP - без зеркалирования
    """
    
    # Константы для режимов направлений
    AUTO_FLIP = "auto_flip"
    SEPARATE_DIRECTIONS = "separate_directions"  
    NO_FLIP = "no_flip"
    
    def __init__(self, x=0, y=0, scale=1.0, direction_mode=AUTO_FLIP):
        """
        Создаем нового персонажа
        x, y - позиция на экране
        scale - размер (1.0 = обычный, 2.0 = в два раза больше)
        direction_mode - режим обработки направлений:
            AUTO_FLIP - автоматическое зеркалирование
            SEPARATE_DIRECTIONS - отдельные анимации для лево/право
            NO_FLIP - без зеркалирования
        """
        # ВАЖНО: Инициализируем родительский класс pygame.sprite.Sprite
        super().__init__()
        
        self.x = x
        self.y = y
        self.scale = scale
        self.direction_mode = direction_mode
        
        # Словарь всех анимаций персонажа
        self.animations = {}
        self.current_animation = None
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10
        
        # Направление персонажа
        self.facing_right = True
        
        # Размеры текущего кадра
        self.current_frame_width = 64
        self.current_frame_height = 64
        
        # Для режима "один большой спрайт-лист"
        self.master_sprite_sheet = None
        self.master_frame_width = 64
        self.master_frame_height = 64
        self.master_columns = 8  # Сколько кадров в строке
        self.next_frame_index = 0  # Следующий свободный кадр в большом спрайт-листе
        
        # ВАЖНО: Атрибуты для pygame.sprite.Sprite
        self.image = pygame.Surface((self.current_frame_width, self.current_frame_height), pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y, self.current_frame_width, self.current_frame_height)
        
        # Дополнительные атрибуты для удобства
        self._original_image = None  # Храним оригинальное изображение для поворотов/масштабирования
    
    def set_direction_mode(self, mode):
        """
        Устанавливаем режим обработки направлений
        mode - AUTO_FLIP, SEPARATE_DIRECTIONS или NO_FLIP
        """
        if mode in [self.AUTO_FLIP, self.SEPARATE_DIRECTIONS, self.NO_FLIP]:
            self.direction_mode = mode
            print(f"🔄 Режим направлений изменен на: {mode}")
        else:
            print(f"❌ Неизвестный режим направлений: {mode}")
    
    def set_facing_direction(self, facing_right):
        """
        Устанавливаем направление персонажа вручную
        facing_right - True для правого направления, False для левого
        """
        self.facing_right = facing_right
    
    def load_master_sprite_sheet(self, sprite_file, frame_width=64, frame_height=64, columns=8):
        """
        Загружаем ОДИН БОЛЬШОЙ спрайт-лист со всеми анимациями
        sprite_file - путь к файлу с большим спрайт-листом
        frame_width, frame_height - размер одного кадра
        columns - сколько кадров в одной строке
        """
        try:
            self.master_sprite_sheet = pygame.image.load(sprite_file)
            self.master_frame_width = frame_width
            self.master_frame_height = frame_height
            self.master_columns = columns
            self.next_frame_index = 0
            print(f"✅ Загружен мастер спрайт-лист: {sprite_file} ({frame_width}x{frame_height}, {columns} колонок)")
            return True
        except Exception as e:
            print(f"❌ Не удалось загрузить мастер спрайт-лист: {sprite_file}")
            print(f"   Ошибка: {e}")
            return False
    
    def add_animation_from_master(self, name, frames, speed=10, loop=True):
        """
        Добавляем анимацию из БОЛЬШОГО спрайт-листа (автопарсинг)
        name - имя анимации
        frames - количество кадров
        speed - скорость анимации
        loop - повторять ли анимацию
        
        Кадры берутся ПОСЛЕДОВАТЕЛЬНО из большого спрайт-листа!
        """
        if self.master_sprite_sheet is None:
            print(f"❌ Сначала загрузите мастер спрайт-лист через load_master_sprite_sheet()")
            return False
        
        # Вычисляем позиции кадров
        frame_positions = []
        for i in range(frames):
            current_index = self.next_frame_index + i
            
            # Вычисляем строку и колонку
            row = current_index // self.master_columns
            col = current_index % self.master_columns
            
            # Вычисляем пиксельные координаты
            x = col * self.master_frame_width
            y = row * self.master_frame_height
            
            frame_positions.append((x, y))
        
        self.animations[name] = {
            'mode': 'master',
            'sprite_image': self.master_sprite_sheet,
            'frame_width': self.master_frame_width,
            'frame_height': self.master_frame_height,
            'frames': frames,
            'speed': speed,
            'loop': loop,
            'finished': False,
            'frame_positions': frame_positions
        }
        
        # Сдвигаем указатель на следующие свободные кадры
        self.next_frame_index += frames
        
        # Если это первая анимация, делаем её текущей
        if self.current_animation is None:
            self.current_animation = name
            self.animation_speed = speed
            self.current_frame_width = self.master_frame_width
            self.current_frame_height = self.master_frame_height
            self._update_sprite_attributes()
        
        print(f"✅ Добавлена анимация из мастер-листа: {name} ({frames} кадров)")
        return True
    
    def add_animation(self, name, sprite_file, frame_width=64, frame_height=64, frames=4, speed=10, loop=True):
        """
        Добавляем анимацию с ОТДЕЛЬНЫМ спрайт-листом
        name - имя анимации (например, "walk", "jump", "idle")
        sprite_file - путь к файлу спрайт-листа для этой анимации
        frame_width, frame_height - размер одного кадра в пикселях
        frames - количество кадров в анимации
        speed - скорость анимации (больше = медленнее)
        loop - повторять ли анимацию
        """
        try:
            # Загружаем спрайт-лист для этой анимации
            sprite_image = pygame.image.load(sprite_file)
            
            self.animations[name] = {
                'mode': 'separate',
                'sprite_image': sprite_image,
                'frame_width': frame_width,
                'frame_height': frame_height,
                'frames': frames,
                'speed': speed,
                'loop': loop,
                'finished': False
            }
            
            # Если это первая анимация, делаем её текущей
            if self.current_animation is None:
                self.current_animation = name
                self.animation_speed = speed
                self.current_frame_width = frame_width
                self.current_frame_height = frame_height
                self._update_sprite_attributes()
            
            print(f"✅ Загружена отдельная анимация: {name} ({frame_width}x{frame_height}, {frames} кадров)")
            return True
            
        except Exception as e:
            print(f"❌ Не удалось загрузить анимацию {name}: {sprite_file}")
            print(f"   Ошибка: {e}")
            return False
    
    def add_directional_animation(self, base_name, left_sprite, right_sprite, frame_width=64, frame_height=64, frames=4, speed=10, loop=True):
        """
        Добавляем анимацию с ОТДЕЛЬНЫМИ спрайтами для левого и правого направлений
        base_name - базовое имя анимации (например, "walk")
        left_sprite - спрайт для движения влево
        right_sprite - спрайт для движения вправо
        """
        # Добавляем анимации с суффиксами направлений
        left_success = self.add_animation(f"{base_name}_left", left_sprite, frame_width, frame_height, frames, speed, loop)
        right_success = self.add_animation(f"{base_name}_right", right_sprite, frame_width, frame_height, frames, speed, loop)
        
        if left_success and right_success:
            print(f"✅ Добавлена направленная анимация: {base_name} (лево/право)")
            return True
        else:
            print(f"❌ Не удалось добавить направленную анимацию: {base_name}")
            return False
    
    def _update_sprite_attributes(self):
        """
        Обновляем атрибуты pygame.sprite.Sprite (image и rect)
        """
        # Обновляем размеры image и rect
        scaled_width = int(self.current_frame_width * self.scale)
        scaled_height = int(self.current_frame_height * self.scale)
        
        self.image = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        
        # Обновляем rect, сохраняя позицию
        old_center = self.rect.center if hasattr(self, 'rect') else (self.x, self.y)
        self.rect = pygame.Rect(0, 0, scaled_width, scaled_height)
        self.rect.center = old_center
        
        # Синхронизируем x, y с rect
        self.x = self.rect.x
        self.y = self.rect.y
    
    def play_animation(self, name, reset=True):
        """
        Запускаем анимацию
        name - имя анимации
        reset - начать с первого кадра
        """
        # Если используем режим отдельных направлений, выбираем правильную анимацию
        if self.direction_mode == self.SEPARATE_DIRECTIONS:
            direction_suffix = "_right" if self.facing_right else "_left"
            
            # Проверяем, есть ли анимация с направлением
            directional_name = f"{name}{direction_suffix}"
            if directional_name in self.animations:
                name = directional_name
            elif name in self.animations:
                # Если нет направленной анимации, используем базовую
                pass
            else:
                print(f"❌ Анимация {name} не найдена")
                return
        
        if name in self.animations:
            if self.current_animation != name or reset:
                self.current_animation = name
                self.current_frame = 0
                self.animation_timer = 0
                
                # Обновляем параметры текущей анимации
                animation = self.animations[name]
                self.animation_speed = animation['speed']
                self.current_frame_width = animation['frame_width']
                self.current_frame_height = animation['frame_height']
                animation['finished'] = False
                
                # Обновляем атрибуты спрайта
                self._update_sprite_attributes()
    
    def update(self):
        """
        Обновляем анимацию (вызывать каждый кадр игры)
        Совместимо с pygame.sprite.Group.update()!
        """
        if self.current_animation is None:
            return
        
        animation = self.animations[self.current_animation]
        
        # Увеличиваем таймер
        self.animation_timer += 1
        
        # Время сменить кадр?
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame += 1
            
            # Закончились кадры?
            if self.current_frame >= animation['frames']:
                if animation['loop']:
                    self.current_frame = 0  # Начинаем сначала
                else:
                    self.current_frame = animation['frames'] - 1
                    animation['finished'] = True
        
        # Обновляем изображение спрайта
        self._update_image()
    
    def _update_image(self):
        """
        Обновляем изображение спрайта для текущего кадра анимации
        """
        if self.current_animation is None:
            return
        
        animation = self.animations[self.current_animation]
        sprite_image = animation['sprite_image']
        frame_width = animation['frame_width']
        frame_height = animation['frame_height']
        
        # Определяем позицию кадра в зависимости от режима
        if animation['mode'] == 'master' or animation['mode'] == 'range':
            # Режим большого спрайт-листа или диапазона - используем заранее вычисленные позиции
            frame_x, frame_y = animation['frame_positions'][self.current_frame]
        else:
            # Режим отдельного спрайт-листа - кадры идут слева направо
            frame_x = self.current_frame * frame_width
            frame_y = 0
        
        # Вырезаем кадр
        frame_rect = (frame_x, frame_y, frame_width, frame_height)
        frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        frame_surface.blit(sprite_image, (0, 0), frame_rect)
        
        # Применяем зеркалирование в зависимости от режима направлений
        if self.direction_mode == self.AUTO_FLIP and not self.facing_right:
            # Автоматическое зеркалирование
            frame_surface = pygame.transform.flip(frame_surface, True, False)
        elif self.direction_mode == self.NO_FLIP:
            # Никогда не зеркалим
            pass
        # Для SEPARATE_DIRECTIONS зеркалирование не нужно - у нас отдельные спрайты
        
        # Масштабируем, если нужно
        if self.scale != 1.0:
            new_width = int(frame_width * self.scale)
            new_height = int(frame_height * self.scale)
            frame_surface = pygame.transform.scale(frame_surface, (new_width, new_height))
        
        # Обновляем изображение спрайта
        self.image = frame_surface
        self._original_image = frame_surface.copy()
    
    def move(self, dx, dy):
        """
        Двигаем персонажа
        dx, dy - смещение по x и y
        """
        self.x += dx
        self.y += dy
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Автоматически определяем направление (если не отключено)
        if self.direction_mode != self.NO_FLIP:
            if dx > 0:
                self.facing_right = True
            elif dx < 0:
                self.facing_right = False
    
    def set_position(self, x, y):
        """
        Устанавливаем позицию персонажа
        """
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
    
    def get_rect(self):
        """
        Получаем прямоугольник для проверки столкновений
        Совместимо с pygame.sprite!
        """
        return self.rect
    
    def is_animation_finished(self):
        """
        Проверяем, закончилась ли текущая анимация
        """
        if self.current_animation is None:
            return True
        return self.animations[self.current_animation]['finished']
    
    # ДОПОЛНИТЕЛЬНЫЕ МЕТОДЫ ДЛЯ СОВМЕСТИМОСТИ С pygame.sprite
    
    def kill(self):
        """
        Удаляем спрайт из всех групп (стандартный метод pygame.sprite.Sprite)
        """
        super().kill()
    
    def alive(self):
        """
        Проверяем, жив ли спрайт (стандартный метод pygame.sprite.Sprite)
        """
        return super().alive()
    
    def groups(self):
        """
        Возвращаем список групп, в которых находится спрайт
        """
        return super().groups()

    def add_animation_from_range(self, name, start_frame, end_frame, speed=10, loop=True):
        """
        Добавляем анимацию, выбирая ЛЮБЫЕ кадры из большого спрайт-листа
        name - имя анимации
        start_frame - номер первого кадра (начиная с 1, не с 0!)
        end_frame - номер последнего кадра (включительно)
        speed - скорость анимации
        loop - повторять ли анимацию
        
        Примеры:
        add_animation_from_range("idle", 1, 4)     # Кадры 1-4
        add_animation_from_range("walk", 5, 12)    # Кадры 5-12  
        add_animation_from_range("jump", 30, 32)   # Последние 3 кадра
        """
        if self.master_sprite_sheet is None:
            print(f"❌ Сначала загрузите мастер спрайт-лист через load_master_sprite_sheet()")
            return False
        
        # Проверяем корректность диапазона
        if start_frame < 1:
            print(f"❌ Номер кадра не может быть меньше 1! Указано: {start_frame}")
            return False
        
        if end_frame < start_frame:
            print(f"❌ Конечный кадр ({end_frame}) не может быть меньше начального ({start_frame})")
            return False
        
        # Вычисляем общее количество кадров в спрайт-листе
        sprite_width = self.master_sprite_sheet.get_width()
        sprite_height = self.master_sprite_sheet.get_height()
        total_columns = sprite_width // self.master_frame_width
        total_rows = sprite_height // self.master_frame_height
        total_frames = total_columns * total_rows
        
        if end_frame > total_frames:
            print(f"❌ В спрайт-листе всего {total_frames} кадров, а запрошен кадр {end_frame}")
            return False
        
        # Вычисляем позиции выбранных кадров
        frame_positions = []
        frames_count = end_frame - start_frame + 1
        
        for i in range(frames_count):
            # Переводим из нумерации "с 1" в нумерацию "с 0"
            frame_index = (start_frame - 1) + i
            
            # Вычисляем строку и колонку
            row = frame_index // self.master_columns
            col = frame_index % self.master_columns
            
            # Вычисляем пиксельные координаты
            x = col * self.master_frame_width
            y = row * self.master_frame_height
            
            frame_positions.append((x, y))
        
        self.animations[name] = {
            'mode': 'range',
            'sprite_image': self.master_sprite_sheet,
            'frame_width': self.master_frame_width,
            'frame_height': self.master_frame_height,
            'frames': frames_count,
            'speed': speed,
            'loop': loop,
            'finished': False,
            'frame_positions': frame_positions,
            'start_frame': start_frame,
            'end_frame': end_frame
        }
        
        # Если это первая анимация, делаем её текущей
        if self.current_animation is None:
            self.current_animation = name
            self.animation_speed = speed
            self.current_frame_width = self.master_frame_width
            self.current_frame_height = self.master_frame_height
            self._update_sprite_attributes()
        
        print(f"✅ Добавлена анимация из диапазона: {name} (кадры {start_frame}-{end_frame}, всего {frames_count})")
        return True
    
    def show_frame_grid(self):
        """
        Показывает сетку кадров для удобства выбора диапазонов
        """
        if self.master_sprite_sheet is None:
            print("❌ Сначала загрузите мастер спрайт-лист")
            return
        
        sprite_width = self.master_sprite_sheet.get_width()
        sprite_height = self.master_sprite_sheet.get_height()
        total_columns = sprite_width // self.master_frame_width
        total_rows = sprite_height // self.master_frame_height
        
        print(f"\n🗂️  СЕТКА КАДРОВ ({total_columns} колонок × {total_rows} строк):")
        print("=" * (total_columns * 5))
        
        for row in range(total_rows):
            line = ""
            for col in range(total_columns):
                frame_number = row * total_columns + col + 1  # Нумерация с 1
                line += f"[{frame_number:2d}]"
            print(f"Строка {row + 1}: {line}")
        
        print("=" * (total_columns * 5))
        print(f"📊 Всего кадров: {total_columns * total_rows}")
        print("💡 Нумерация начинается с 1 (не с 0)!")
        print("\nПримеры использования:")
        print("hero.add_animation_from_range('idle', 1, 4)      # Первые 4 кадра")
        print("hero.add_animation_from_range('walk', 5, 12)     # Кадры 5-12")
        print(f"hero.add_animation_from_range('jump', {total_columns * total_rows - 2}, {total_columns * total_rows})  # Последние 3 кадра")


class AnimationPresets:
    """
    Готовые настройки анимаций для разных типов персонажей
    """
    
    @staticmethod
    def setup_platformer_hero(character, sprite_sheet_name):
        """
        Настройка для платформера (герой с мечом)
        """
        character.add_animation("idle", sprite_sheet_name, row=0, frames=4, speed=15)
        character.add_animation("walk", sprite_sheet_name, row=1, frames=8, speed=8)
        character.add_animation("run", sprite_sheet_name, row=2, frames=8, speed=5)
        character.add_animation("jump", sprite_sheet_name, row=3, frames=4, speed=6, loop=False)
        character.add_animation("attack", sprite_sheet_name, row=4, frames=6, speed=4, loop=False)
        character.add_animation("hit", sprite_sheet_name, row=5, frames=3, speed=8, loop=False)
        character.add_animation("die", sprite_sheet_name, row=6, frames=4, speed=10, loop=False)
    
    @staticmethod
    def setup_simple_character(character, sprite_sheet_name):
        """
        Простая настройка для начинающих
        """
        character.add_animation("idle", sprite_sheet_name, row=0, frames=4, speed=12)
        character.add_animation("walk", sprite_sheet_name, row=1, frames=4, speed=8)
        character.add_animation("jump", sprite_sheet_name, row=2, frames=4, speed=6)


class GameAnimator(pygame.sprite.Group):
    """
    Менеджер для управления всеми анимациями в игре
    Наследуется от pygame.sprite.Group для полной совместимости!
    """
    
    def __init__(self):
        # Инициализируем родительский класс pygame.sprite.Group
        super().__init__()
    
    def add_character(self, character):
        """
        Добавляем персонажа в группу (совместимо с pygame.sprite.Group)
        """
        self.add(character)
    
    def update_all(self):
        """
        Обновляем все персонажи (можно использовать стандартный update())
        """
        self.update()  # Стандартный метод pygame.sprite.Group
    
    def draw_all(self, screen):
        """
        Рисуем всех персонажей (можно использовать стандартный draw())
        """
        self.draw(screen)  # Стандартный метод pygame.sprite.Group


# Функции-помощники для быстрого создания персонажей

def create_hero_separate_sprites(x=0, y=0, scale=1.0, 
                                idle_sprite="idle.png", 
                                walk_sprite="walk.png", 
                                jump_sprite="jump.png",
                                frame_size=64):
    """
    Создаем героя с ОТДЕЛЬНЫМИ спрайт-листами для каждой анимации
    """
    hero = AnimatedCharacter(x, y, scale)
    hero.add_animation("idle", idle_sprite, frame_size, frame_size, frames=4, speed=15)
    hero.add_animation("walk", walk_sprite, frame_size, frame_size, frames=4, speed=8)
    hero.add_animation("jump", jump_sprite, frame_size, frame_size, frames=4, speed=6)
    return hero

def create_hero_master_sprite(x=0, y=0, scale=1.0, 
                             master_sprite="all_animations.png", 
                             frame_size=64, columns=8):
    """
    Создаем героя с ОДНИМ БОЛЬШИМ спрайт-листом
    """
    hero = AnimatedCharacter(x, y, scale)
    hero.load_master_sprite_sheet(master_sprite, frame_size, frame_size, columns)
    
    # Добавляем анимации по порядку (кадры берутся последовательно!)
    hero.add_animation_from_master("idle", frames=4, speed=15)  # Кадры 0-3
    hero.add_animation_from_master("walk", frames=8, speed=8)   # Кадры 4-11  
    hero.add_animation_from_master("jump", frames=4, speed=6)   # Кадры 12-15
    
    return hero

def create_custom_hero(x=0, y=0, scale=1.0):
    """
    Создаем героя для полной настройки вручную
    """
    return AnimatedCharacter(x, y, scale) 