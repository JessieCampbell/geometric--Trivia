
import pygame
import sys
import os
import time

# ---------------------------------------------------------
# PANTALLA JUEGO
# ---------------------------------------------------------
def show_game_over(screen, WIDTH, HEIGHT, FONT, SMALL_FONT, BLACK, WHITE, score, wrong, total):

    screen.fill(WHITE)

    msg = FONT.render("Juego Terminado", True, BLACK)
    score_msg = FONT.render(f"Puntaje final: {score}/{total}", True, BLACK)
    wrong_msg = SMALL_FONT.render(f"Preguntas falladas: {wrong}", True, BLACK)

    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 200))
    screen.blit(score_msg, (WIDTH//2 - score_msg.get_width()//2, 260))
    screen.blit(wrong_msg, (WIDTH//2 - wrong_msg.get_width()//2, 310))

    pygame.display.flip()
    pygame.time.delay(3000)


# ---------------------------------------------------------
# JUEGO PRINCIPAL DE TRIVIA
# ---------------------------------------------------------
def run_quiz():

    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Juego de Trivia")

    FONT = pygame.font.SysFont("Georgia", 30)
    SMALL_FONT = pygame.font.SysFont("Georgia", 30)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 0)
    GREEN = (0, 200, 0)
    RED = (200, 0, 0)

    # RUTA DE ASSETS
    ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

    # -----------------------------
    # MÚSICA DE FONDO
    # -----------------------------
    music_path = os.path.join(ASSETS_PATH, "trivia.mp3")
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"⚠️ No se pudo cargar la música del quiz: {e}")

    # -----------------------------
    # FONDO
    # -----------------------------
    try:
        bg_path = os.path.join("assets/fondo_trivia.png")
        background = pygame.image.load(bg_path).convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    except Exception as e:
        print(f"⚠️ No se encontró la imagen de fondo: {e}")
        background = None

    # -----------------------------
    # PREGUNTAS
    # -----------------------------
    questions = [
        {"text": "¿Cuánto es 69 + 30?", "options": ["98", "100", "99", "90"], "answer": 2},
        {"text": "¿Capital de Francia?", "options": ["Roma", "Madrid", "París", "Lisboa"], "answer": 2},
        {"text": "¿Cuántos huesos tiene el cuerpo humano?", "options": ["106", "206", "160", "306"], "answer": 1},
        {"text": "¿En qué año inició la Segunda Guerra Mundial?", "options": ["1941", "1919", "1939", "2000"], "answer": 2},
        {"text": "¿Dios griego de la guerra?", "options": ["Zeus", "Hera", "Apolo", "Ares"], "answer": 3},
        {"text": "¿Padre de la Biología?", "options": ["Aristóteles", "Hooke", "Swerland", "Edison"], "answer": 0},
        {"text": "Colores primarios:", "options": ["Rojo, Amarillo, Verde", "Amarillo, Verde, Azul", "Rojo, Verde, Azul", "Amarillo, Rojo, Azul"], "answer": 3},
        {"text": "Continente con más países:", "options": ["Europa", "África", "Oceanía", "América"], "answer": 1},
        {"text": "Único país de Centroamérica que irá al mundial:", "options": ["Panamá", "Costa Rica", "El Salvador", "Guatemala"], "answer": 0},
        {"text": "¿Mejor colegio de Colón?", "options": ["Santa María", "Guardia Vega", "Rufo", "Abel Bravo"], "answer": 3},
    ]

    score = 0
    wrong = 0
    q_index = 0
    running = True
    selected_option = None
    show_feedback = False
    feedback_timer = 0

    # TIEMPO POR PREGUNTA
    QUESTION_TIME_MS = 10_000
    question_start_ms = pygame.time.get_ticks()

    clock = pygame.time.Clock()

    # ---------------------------------------------------------
    # LOOP PRINCIPAL
    # ---------------------------------------------------------
    while running:

        dt = clock.tick(60)

        # FONDO
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(WHITE)

        # FINAL DEL QUIZ
        if q_index >= len(questions):
            break

        # PREGUNTA ACTUAL
        question = questions[q_index]

        # Texto de pregunta
        text = FONT.render(question["text"], True, BLACK)

        screen.blit(text, (100, 100))

        # TIEMPO RESTANTE
        now = pygame.time.get_ticks()
        elapsed = now - question_start_ms
        remaining_ms = max(0, QUESTION_TIME_MS - elapsed)
        remaining_s = remaining_ms // 1000
        timer_surf = FONT.render(f"Tiempo: {remaining_s}s", True, BLACK)
        screen.blit(timer_surf, (WIDTH - 200, 20))

        # OPCIONES
        rects = []
        for i, opt in enumerate(question["options"]):
            rect = pygame.Rect(150, 200 + i * 80, 500, 60)

            if show_feedback:
                if i == question["answer"]:
                    color = GREEN
                elif i == selected_option:
                    color = RED
                else:
                    color = BLUE
            else:
                color = BLUE

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, WHITE, rect, 2)

            txt = FONT.render(opt, True, WHITE)
            screen.blit(txt, (rect.x + 10, rect.y + 15))

            rects.append(rect)

        # EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not show_feedback:
                pos = pygame.mouse.get_pos()
                for i, rect in enumerate(rects):
                    if rect.collidepoint(pos):
                        selected_option = i
                        show_feedback = True
                        feedback_timer = pygame.time.get_ticks()

                        if i == question["answer"]:
                            score += 1
                        else:
                            wrong += 1
                        break

        # TIEMPO AGOTADO
        if not show_feedback and remaining_ms <= 0:
            show_feedback = True
            wrong += 1  # no respondió
            feedback_timer = pygame.time.get_ticks()

        # TIEMPO MOSTRANDO FEEDBACK
        if show_feedback:
            if pygame.time.get_ticks() - feedback_timer >= 1000:
                show_feedback = False
                selected_option = None
                q_index += 1
                question_start_ms = pygame.time.get_ticks()

        # SCORE
        score_surf = FONT.render(f"Puntaje: {score}/{len(questions)}", True, BLACK)
        screen.blit(score_surf, (30, 30))

        pygame.display.flip()

    # FIN DEL JUEGO
    show_game_over(screen, WIDTH, HEIGHT, FONT, SMALL_FONT, BLACK, WHITE, score, wrong, len(questions))

    pygame.quit()
