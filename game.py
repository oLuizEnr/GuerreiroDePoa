import pygame as pg

# Inícia o jogo
pg.init()
jogando = True # Usado no loop que mantém o jogo rodando. Enquanto for verdadeiro o jogo continua

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

# Loop que mantém o jogo rodando
while jogando:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            jogando = False
    tela.fill(preto)
    pg.display.flip()

# Encerra o jogo
pg.quit()