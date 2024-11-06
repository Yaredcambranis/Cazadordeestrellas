import pygame
import random
import os

# Inicialización de pygame
pygame.init()

# Configuración de pantalla y colores
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cazador de Estrellas")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuración de FPS
clock = pygame.time.Clock()
FPS = 60

# Cargar sonidos
pygame.mixer.music.load("assets/sounds/fondo.mp3")
pygame.mixer.music.set_volume(0.3)  # Ajusta el volumen de fondo
pygame.mixer.music.play(-1)  # Reproduce en bucle

explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
explosion_sound.set_volume(0.5)  # Ajusta el volumen de la explosión

# Cargar fondo
fondo = pygame.image.load("assets/images/fondo.png").convert()
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

# Archivos de puntuaciones
TOP_SCORES_FILE = "top_scores.txt"

# Cargar o crear archivo de puntuaciones
def cargar_puntuaciones():
    if os.path.exists(TOP_SCORES_FILE):
        with open(TOP_SCORES_FILE, "r") as file:
            scores = [int(line.strip()) for line in file]
        return sorted(scores, reverse=True)[:5]
    return [0] * 5

def guardar_puntuaciones(score):
    scores = cargar_puntuaciones()
    scores.append(score)
    scores = sorted(scores, reverse=True)[:5]
    with open(TOP_SCORES_FILE, "w") as file:
        for score in scores:
            file.write(f"{score}\n")

# Pantalla de inicio
def mostrar_pantalla_inicio():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Cazador de Estrellas", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    font = pygame.font.Font(None, 36)
    text = font.render("Presiona cualquier tecla para iniciar", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()
    esperar_tecla()

# Pantalla de game over
def mostrar_pantalla_game_over(score):
    guardar_puntuaciones(score)
    top_scores = cargar_puntuaciones()
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
    font = pygame.font.Font(None, 36)
    text = font.render(f"Puntuación: {score}", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    text = font.render("Top 5 Puntuaciones:", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 50))
    
    for i, top_score in enumerate(top_scores):
        text = font.render(f"{i + 1}. {top_score}", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 100 + 30 * i))

    text = font.render("Presiona cualquier tecla para reiniciar", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 100))
    pygame.display.flip()
    esperar_tecla()

def esperar_tecla():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Clase de la Nave
class Nave:
    def __init__(self):
        self.image = pygame.image.load("assets/images/nave.png").convert_alpha()
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Clase de Estrellas
class Estrella:
    def __init__(self, speed):
        self.image = pygame.image.load("assets/images/estrella.png").convert_alpha()
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def off_screen(self):
        return self.rect.top > HEIGHT

# Clase de Asteroides (Obstáculos)
class Asteroide:
    def __init__(self, speed):
        self.image = pygame.image.load("assets/images/asteroide.png").convert_alpha()
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def off_screen(self):
        return self.rect.top > HEIGHT

# Función de una partida
def partida():
    nave = Nave()
    estrellas = []
    asteroides = []
    score = 0
    level = 1
    estrella_speed = 3
    asteroide_speed = 5
    running = True

    while running:
        clock.tick(FPS)
        
        # Dibujar fondo
        screen.blit(fondo, (0, 0))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Movimiento de la nave
        keys = pygame.key.get_pressed()
        nave.move(keys)

        # Generación aleatoria de estrellas y asteroides
        if random.randint(1, 30) == 1:
            estrellas.append(Estrella(estrella_speed))
        if random.randint(1, 50) == 1:
            asteroides.append(Asteroide(asteroide_speed))

        # Movimiento y dibujo de estrellas
        for estrella in estrellas[:]:
            estrella.move()
            estrella.draw(screen)
            if estrella.off_screen():
                estrellas.remove(estrella)
            if nave.rect.colliderect(estrella.rect):
                estrellas.remove(estrella)
                score += 1

        # Movimiento y dibujo de asteroides
        for asteroide in asteroides[:]:
            asteroide.move()
            asteroide.draw(screen)
            if asteroide.off_screen():
                asteroides.remove(asteroide)
            if nave.rect.colliderect(asteroide.rect):
                explosion_sound.play()
                mostrar_pantalla_game_over(score)
                return

        # Subir nivel cada 10 puntos
        if score // 10 > level - 1:
            level += 1
            estrella_speed += 1
            asteroide_speed += 1

        nave.draw(screen)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Puntuación: {score} - Nivel: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

# Bucle principal
def main():
    while True:
        mostrar_pantalla_inicio()
        partida()

if __name__ == "__main__":
    main()
