import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Configurações da janela
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Plataforma")

# Carrega a imagem de fundo
background_image = pygame.image.load("background.jpg")  # Substitua pelo caminho da sua imagem
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Redimensiona para caber na tela

# Carrega a imagem do jogador
player_image = pygame.image.load("pou.png")  # Substitua pelo caminho da sua imagem
player_image = pygame.transform.scale(player_image, (50, 50))  # Ajuste o tamanho da imagem para o tamanho do jogador

# Carrega a imagem da moeda (bitcoin)
coin_image = pygame.image.load("bitcoin.png")  # Substitua pelo caminho da imagem do bitcoin
coin_image = pygame.transform.scale(coin_image, (30, 30))  # Ajuste o tamanho da imagem da moeda

# Cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Configurações do jogador
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT - player_size - 10
player_velocity = 5
player_jump = 10
player_y_velocity = 0
is_jumping = False

# Configuração das plataformas (removendo 3 plataformas extras)
platforms = [
    {"rect": pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 20), "speed": 2, "direction": 1},
    {"rect": pygame.Rect(WIDTH // 2 - 120, HEIGHT - 180, 200, 20), "speed": 3, "direction": -1},
]

# Moedas (mantendo apenas as 3 primeiras moedas)
coins = [
    pygame.Rect(400, HEIGHT - 150, 30, 30),  # Moeda 1
    pygame.Rect(200, HEIGHT - 250, 30, 30),  # Moeda 2
    pygame.Rect(600, HEIGHT - 350, 30, 30),  # Moeda 3
]

# Perguntas e respostas com alternativas
questions = [
    {"question": "Por que é importante criar um orçamento mensal?", "options": ["Porque devemos ter controle das fianças", "Para sair gastando sem consciência", "Porque precisamos saber sobre nosso patrimônio mensal"], "answer": "Porque devemos ter controle das fianças"},
    {"question": "Qual é a regra dos 50-30-20 em finanças pessoais?", "options": ["50% Necessidades, 30% desejos e 20% investimentos e poupanças.", "50% Poupanças e Investimentos, 30% necessidades e 20% desejos", "50% desejos, 30% Poupanças e Investimentos e 20% necessidades"], "answer": "50% Necessidades, 30% desejos e 20% investimentos e poupanças."},
    {"question": "Como priorizar despesas essenciais em um planejamento financeiro?", "options": ["Ignorar Gastos com Saúde", "Criar uma Lista de Prioridades", "Focar Apenas no Presente e Ignorar o Futuro"], "answer": "Criar uma Lista de Prioridades"},
]

question_index = 0
show_question = False
selected_option = 0
score = 0  # Pontuação inicial do jogador

# Variável de controle de tela cheia
fullscreen = False

# Loop principal do jogo
clock = pygame.time.Clock()
running = True
while running:
    # Desenha a imagem de fundo
    window.blit(background_image, (0, 0))
    
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
            # Navegação nas opções durante uma pergunta
            if show_question:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(questions[question_index]["options"])
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(questions[question_index]["options"])
                elif event.key == pygame.K_RETURN:
                    # Verifica a resposta
                    if questions[question_index]["options"][selected_option] == questions[question_index]["answer"]:
                        score += random.randint(10, 50)  # Adiciona pontos
                    show_question = False
                    question_index += 1

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
        if player_rect.colliderect(platform["rect"]) and player_y_velocity >= 0:
            player_y = platform["rect"].top - player_size
            is_jumping = False
            player_y_velocity = 0

    # Verifica colisão com as moedas
    if not show_question and question_index < len(questions):  # Apenas coleta moedas se houver perguntas
        for coin in coins[:]:
            if player_rect.colliderect(coin):
                coins.remove(coin)  # Remove a moeda coletada
                show_question = True  # Exibe a pergunta
                selected_option = 0
                break

    # Atualiza o movimento das plataformas
    for platform in platforms:
        platform["rect"].x += platform["speed"] * platform["direction"]

        # Inverte a direção se a plataforma atingir os limites da tela
        if platform["rect"].left <= 0 or platform["rect"].right >= WIDTH:
            platform["direction"] *= -1

    # Desenha o jogador como imagem
    window.blit(player_image, (player_x, player_y))

    # Desenha plataformas e moedas (usando a imagem do bitcoin)
    for platform in platforms:
        pygame.draw.rect(window, BLUE, platform["rect"])
    for coin in coins:
        window.blit(coin_image, coin.topleft)  # Desenha a imagem do bitcoin no lugar da moeda

    # Exibe a pergunta e as opções se uma moeda for coletada
    if show_question and question_index < len(questions):
        font = pygame.font.Font(None, 36)
        question_surface = font.render(questions[question_index]["question"], True, BLACK)
        window.blit(question_surface, (WIDTH // 2 - question_surface.get_width() // 2, HEIGHT // 2 - 100))
        
        # Exibe as opções
        for i, option in enumerate(questions[question_index]["options"]):
            color = YELLOW if i == selected_option else BLACK
            option_surface = font.render(option, True, color)
            window.blit(option_surface, (WIDTH // 2 - option_surface.get_width() // 2, HEIGHT // 2 - 50 + i * 40))

    # Exibe a pontuação
    font = pygame.font.Font(None, 36)
    score_surface = font.render(f"Pontos: {score}", True, BLACK)
    window.blit(score_surface, (10, 10))

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(30)

# Finaliza o Pygame
pygame.quit()
sys.exit()
