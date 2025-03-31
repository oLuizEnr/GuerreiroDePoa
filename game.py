import pygame as pg

# Inícia o jogo
pg.init()
jogando = True # Usado no loop que mantém o jogo rodando. Enquanto for verdadeiro o jogo continua
clock = pg.time.Clock() # A definir a taxa de quadros

# Configura a tela do jogo
telaLargura = 640
telaAltura = 480
tela = pg.display.set_mode((telaLargura, telaAltura)) # set_mode() recebe tupla com largura e altura e monta a tela
pg.display.set_caption('WOP - Warrior Of Poá') # set_caption() define o título do jogo ao executar

# Cores em sistema rgb
vermelho = (255,0,0)
verde = (0,255,0)
azul = (0,0,255)
branco = (255,255,255)
preto = (0,0,0)

playerPosicao = pg.Vector2(telaLargura/2,telaAltura/2)

# Loop que mantém o jogo rodando
while jogando:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            jogando = False

    tela.fill(preto) # Preenche a tela de preto

    pg.draw.circle(tela,branco,playerPosicao,40) # Desenha um circulo na tela, branco, na posição do player, de raio 40

    # "Move" o circulo mudando sua posição em seus 2 eixos ao apertar a, w, s ou d
    teclas = pg.key.get_pressed()
    if teclas[pg.K_w]:
        playerPosicao.y -= 30 # Quando w, a posição y diminui (y = 0 é o topo da tela, diminuir o y é subir o objeto)
    if teclas[pg.K_s]:
        playerPosicao.y += 30 # Quando s, a posição y aumenta (y = 0 é o topo da tela, aumentar o y é descer o objeto)
    if teclas[pg.K_a]:
        playerPosicao.x -= 30 # Quando a, a posição x diminui (x = 0 esquerda, diminuir é levar para a esquerda)
    if teclas[pg.K_d]:
        playerPosicao.x += 30 # Quando d, a posição x aumetna (x = 0 esquerda, aumentar é levar para a direita)

    pg.display.flip() #
    
    clock.tick(60) / 1000

# Encerra o jogo
pg.quit()