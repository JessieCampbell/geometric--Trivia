
import pygame
import sys
import quiz_game
import cube_game
import os

# ---------------------------
# MENÚ
# ---------------------------

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menú Principal - Universo de Juegos")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (100, 150, 255)
BLUE = (30, 30, 180)
HOVER_COLOR = (180, 200, 255)

# Fuentes
FONT_TITLE = pygame.font.SysFont("Georgia", 48)
FONT_OPTION = pygame.font.SysFont("Georgia", 32)
FONT_FOOTER = pygame.font.SysFont("Georgia", 20)

clock = pygame.time.Clock()

# ---------------------------
# RECURSOS
# ---------------------------
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")
# Música
try:
    pygame.mixer.music.load(os.path.join(ASSETS_PATH, "menu.mp3"))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)  # Repetir en bucle
except:
    print("⚠️ No se encontró la música de fondo")

# Efectos de sonido
try:
    click_sound = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "click.wav"))
    hover_sound = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "hover.wav"))
except:
    click_sound = hover_sound = None

# Fondo e imagen
try:
    background = pygame.image.load("assets/Sample.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except:
    print("⚠️ No se encontró la imagen de fondo")
    background = None


# ---------------------------
# FUNCIONES AUXILIARES
# ---------------------------
# Función auxiliar que hace la parte del texto centreado
def draw_centered_text(surface, text, font, color, center_x, center_y):
    """Dibuja texto centrado en pantalla."""
    img = font.render(text, True, color)
    rect = img.get_rect(center=(center_x, center_y))
    surface.blit(img, rect)

print(help(draw_centered_text))
# ---------------------------
# MENÚ PRINCIPAL
# ---------------------------

def main_menu():
    """
    Muestra el menú principal con dos opciones:
    - Juego de Trivia
    - Juego del Cubo
    Incluye música, fondo y efectos de sonido.
    """
    quiz_rect = pygame.Rect(250, 250, 300, 70)
    cube_rect = pygame.Rect(250, 370, 300, 70)

    hover_quiz = hover_cube = False
    bg_scroll = 0

    running = True
    while running:
        # Control de fondo animado

        if background:
            bg_scroll = (bg_scroll + 1) % WIDTH
            screen.blit(background, (-bg_scroll, 0))
            screen.blit(background, (WIDTH - bg_scroll, 0))
        else:
            screen.fill((180, 200, 255))

        # Título principal
        draw_centered_text(screen, " UNIVERSO DE JUEGOS", FONT_TITLE, BLACK, WIDTH // 2, 120)


        # Posición del mouse
        mouse_pos = pygame.mouse.get_pos()

        # ---- Botón de Trivia ----
        if quiz_rect.collidepoint(mouse_pos):
            color_quiz = HOVER_COLOR
            if not hover_quiz and hover_sound:
                hover_sound.play()
            hover_quiz = True
        else:
            color_quiz = LIGHT_BLUE
            hover_quiz = False

        pygame.draw.rect(screen, color_quiz, quiz_rect)
        pygame.draw.rect(screen, BLACK, quiz_rect, 3)
        draw_centered_text(screen, "Jugar Trivia", FONT_OPTION, BLACK, quiz_rect.centerx, quiz_rect.centery)

        # ---- Botón del Cubo ----
        if cube_rect.collidepoint(mouse_pos):
            color_cube = HOVER_COLOR
            if not hover_cube and hover_sound:
                hover_sound.play()
            hover_cube = True
        else:
            color_cube = LIGHT_BLUE
            hover_cube = False

        pygame.draw.rect(screen, color_cube, cube_rect)
        pygame.draw.rect(screen, BLACK, cube_rect, 3)
        draw_centered_text(screen, "Jugar Cubo", FONT_OPTION, BLACK, cube_rect.centerx, cube_rect.centery)

        # Pie de página
        draw_centered_text(screen, "Haz clic en una opción para comenzar", FONT_FOOTER, BLACK, WIDTH // 2, 550)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if quiz_rect.collidepoint(mouse_pos):
                    if click_sound:
                        click_sound.play()
                    quiz_game.run_quiz()

                elif cube_rect.collidepoint(mouse_pos):
                    if click_sound:
                        click_sound.play()
                    cube_game.run_cube()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()
