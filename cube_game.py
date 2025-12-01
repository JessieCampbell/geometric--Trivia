import pygame
import sys
import random
import os


def run_cube():
    pygame.init()
    WIDTH, HEIGHT = 800, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Juego del Cubo - Desintegración")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Georgia", 28)

    # Colores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (200, 0, 0)
    BLUE = (0, 0, 200)
    GRAY = (150, 150, 150)

    # Ruta de música
    ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")
    music_path = os.path.join(ASSETS_PATH, "cubo.mp3")

    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"⚠️ No se pudo cargar la música del juego del cubo: {e}")

    # -----------------------------
    # FONDO
    # -----------------------------
    try:
        background_path = os.path.join(ASSETS_PATH, "Sample2.png")
        background = pygame.image.load(background_path).convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    except Exception as e:
        print(f"⚠️ No se encontró la imagen de fondo: {e}")
        background = None

    bg_scroll = 0

    # Cubo (jugador)
    cube = pygame.Rect(100, 300, 40, 40)
    gravity = 0
    jump = -12

    # Obstáculos
    obstacles = []
    spawn_timer = 0
    score = 0
    running = True

    # Efecto de desintegración
    particles = []
    cube_destroyed = False
    explosion_timer = 0

    while running:

        # ------------------------
        # Fondo ANIMADO
        # ------------------------
        if background:
            bg_scroll = (bg_scroll + 1) % WIDTH
            screen.blit(background, (-bg_scroll, 0))
            screen.blit(background, (WIDTH - bg_scroll, 0))
        else:
            screen.fill((180, 200, 255))

        # ------------------------
        # EVENTOS
        # ------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE and not cube_destroyed and cube.bottom >= 340:
                    gravity = jump

        # Física del cubo
        if not cube_destroyed:
            gravity += 0.8
            cube.y += gravity
            if cube.bottom > 340:
                cube.bottom = 340
                gravity = 0

        # Generación de obstáculos
        if not cube_destroyed:
            spawn_timer += 1
            if spawn_timer > 60:
                spawn_timer = 0
                obstacle = pygame.Rect(WIDTH, 300, 40, 40)
                obstacles.append(obstacle)

        # Mover obstáculos y detectar colisiones
        for obstacle in list(obstacles):
            obstacle.x -= 6
            if obstacle.right < 0:
                obstacles.remove(obstacle)
                if not cube_destroyed:
                    score += 1
            pygame.draw.rect(screen, RED, obstacle)

            if not cube_destroyed and cube.colliderect(obstacle):
                cube_destroyed = True
                explosion_timer = 60

                # Crear partículas
                for _ in range(40):
                    particles.append({
                        "x": cube.centerx,
                        "y": cube.centery,
                        "vx": random.uniform(-5, 5),
                        "vy": random.uniform(-8, -1),
                        "size": random.randint(3, 6),
                        "color": BLUE,
                        "life": random.randint(20, 40)
                    })

        # Actualizar partículas
        for p in list(particles):
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.3
            p["life"] -= 1

            if p["life"] <= 0:
                particles.remove(p)
            else:
                pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), p["size"])

        # Dibujar cubo
        if not cube_destroyed:
            pygame.draw.rect(screen, BLUE, cube)

        # Suelo
        pygame.draw.line(screen, BLACK, (0, 340), (WIDTH, 340), 3)

        # Puntaje
        score_text = font.render(f"Puntaje: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Fin de explosión
        if cube_destroyed:
            explosion_timer -= 1
            if explosion_timer <= 0 and not particles:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.quit()
