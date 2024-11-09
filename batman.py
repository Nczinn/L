import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Configurações da janela
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Plataforma")

# Cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Configurações do jogador
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT - player_size - 10
player_velocity = 5
player_jump = 10
player_y_velocity = 0
is_jumping = False

# Configuração das plataformas
platforms = [
    pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 20),
    pygame.Rect(150, HEIGHT - 200, 200, 20),
    pygame.Rect(500, HEIGHT - 300, 200, 20),
    pygame.Rect(100, HEIGHT - 400, 200, 20),  # Nova plataforma
    pygame.Rect(600, HEIGHT - 500, 200, 20),  # Nova plataforma
]

# Moedas
coins = [
    pygame.Rect(400, HEIGHT - 150, 20, 20),
    pygame.Rect(200, HEIGHT - 250, 20, 20),
    pygame.Rect(600, HEIGHT - 350, 20, 20),
    pygame.Rect(350, HEIGHT - 450, 20, 20),  # Nova moeda
    pygame.Rect(250, HEIGHT - 550, 20, 20),  # Nova moeda
    pygame.Rect(650, HEIGHT - 550, 20, 20),  # Nova moeda
]

# Perguntas e respostas
questions = [
    {"question": "Qual é a capital da França?", "answer": "Paris"},
    {"question": "Qual é a cor do céu durante o dia?", "answer": "Azul"},
    {"question": "Quantos continentes existem no mundo?", "answer": "7"},
    {"question": "Qual é o maior planeta do sistema solar?", "answer": "Jupiter"},
    {"question": "Quem pintou a Mona Lisa?", "answer": "Da Vinci"},
    {"question": "Qual é a fórmula da água?", "answer": "H2O"},
]

question_index = 0
show_question = False
user_answer = ""
score = 0  # Pontuação inicial do jogador

# Variável de controle de tela cheia
fullscreen = False

# Loop principal do jogo
clock = pygame.time.Clock()
running = True
while running:
    window.fill(WHITE)
    
    # Eventos do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Alterna para tela cheia com a tecla 'F'
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    window = pygame.display.set_mode((WIDTH, HEIGHT))
            # Entrada do usuário na tela de pergunta
            if show_question:
                if event.key == pygame.K_BACKSPACE:
                    user_answer = user_answer[:-1]
                elif event.key == pygame.K_RETURN:
                    # Verifica a resposta
                    if user_answer.lower() == questions[question_index]["answer"].lower():
                        show_question = False
                        user_answer = ""
                        question_index += 1
                        # Adiciona pontos aleatórios entre 10 e 50
                        score += random.randint(10, 50)
                    else:
                        show_question = False  # Se a resposta estiver errada, só fecha a pergunta
                        user_answer = ""
                        question_index += 1
                else:
                    user_answer += event.unicode

    # Movimento do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_velocity
    if keys[pygame.K_RIGHT]:
        player_x += player_velocity
    if not is_jumping:
        if keys[pygame.K_SPACE]:
            is_jumping = True
            player_y_velocity = -player_jump

    # Gravidade e pulo
    player_y += player_y_velocity
    player_y_velocity += 0.5  # Gravidade

    # Verifica colisão com o chão
    if player_y >= HEIGHT - player_size - 10:
        player_y = HEIGHT - player_size - 10
        is_jumping = False

    # Verifica colisão com as plataformas
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    for platform in platforms:
        if player_rect.colliderect(platform) and player_y_velocity >= 0:
            player_y = platform.top - player_size
            is_jumping = False
            player_y_velocity = 0

    # Verifica colisão com as moedas
    if not show_question and question_index < len(questions):  # Apenas coleta moedas se houver perguntas
        for coin in coins[:]:
            if player_rect.colliderect(coin):
                coins.remove(coin)  # Remove a moeda coletada
                show_question = True  # Exibe a pergunta
                break

    # Desenha o jogador, plataformas e moedas
    pygame.draw.rect(window, BLUE, player_rect)
    for platform in platforms:
        pygame.draw.rect(window, BLUE, platform)
    for coin in coins:
        pygame.draw.rect(window, YELLOW, coin)

    # Exibe a pergunta se uma moeda for coletada e houver mais perguntas
    if show_question and question_index < len(questions):
        font = pygame.font.Font(None, 36)
        question_surface = font.render(questions[question_index]["question"], True, (0, 0, 0))
        window.blit(question_surface, (WIDTH // 2 - question_surface.get_width() // 2, HEIGHT // 2 - 50))
        answer_surface = font.render(user_answer, True, (0, 0, 0))
        window.blit(answer_surface, (WIDTH // 2 - answer_surface.get_width() // 2, HEIGHT // 2))

    # Exibe a pontuação
    font = pygame.font.Font(None, 36)
    score_surface = font.render(f"Pontos: {score}", True, (0, 0, 0))
    window.blit(score_surface, (10, 10))

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(30)

# Finaliza o Pygame
pygame.quit()
sys.exit()
