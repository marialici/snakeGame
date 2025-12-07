import random

import pyglet
from pyglet import gl, shapes
from pyglet.window import key

# Janela / constantes
TITULO = "Snake Game"
LARGURA = 600
ALTURA = 600
TAM_BLOCO = 25
PAINEL_ALTURA = 50
INTERVALO = 0.12  # 120 ms

# Cores
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
VERMELHO = (255, 0, 0)
VERDE = (20, 120, 20)

som_comer = pyglet.media.load("sons/eat.wav", streaming=False)
som_morte = pyglet.media.load("sons/hit.wav", streaming=False)

try:
    with open("recorde.txt", "r") as f:
        recorde = int(f.read())
except:
    recorde = 0

# Estado inicial
x, y = 275, 275
direcao = "parado"
tamanho_cobra = 2
cauda = [(x, y)]

posicoes_x = [i for i in range(0, LARGURA, TAM_BLOCO)]
posicoes_y = [i for i in range(PAINEL_ALTURA, ALTURA, TAM_BLOCO)]

comida = (random.choice(posicoes_x), random.choice(posicoes_y))
pausado = False

# Janela e elementos gráficos
janela = pyglet.window.Window(LARGURA, ALTURA, TITULO)
janela.set_vsync(False)

gl.glClearColor(1.0, 1.0, 1.0, 1.0)
batch = pyglet.graphics.Batch()

# Painel superior
painel = shapes.Rectangle(
    0, ALTURA - PAINEL_ALTURA, LARGURA, PAINEL_ALTURA, color=AZUL, batch=batch
)

pontuacao_label = pyglet.text.Label(
    text=f"Pontuação: {tamanho_cobra - 2}", font_size=20, x=10, y=ALTURA - 30, batch=batch, color=AMARELO + (255,)
)
recorde_label = pyglet.text.Label(
    text=f"Recorde: {recorde}", font_size=20, x=LARGURA - 150, y=ALTURA - 30, batch=batch, color=AMARELO + (255,)
)
label_pausa = pyglet.text.Label(
    text="Jogo Pausado", x=LARGURA // 2, y=ALTURA // 2, font_size=40, anchor_x="center", anchor_y="center", color=(0, 0, 0, 255)
)


def sortear_comida():
    return (random.choice(posicoes_x), random.choice(posicoes_y))


def converter_y_para_pyglet(y_orig):
    return ALTURA - y_orig - TAM_BLOCO  # converte y do jogo para y do pyglet


@janela.event
def on_draw():
    janela.clear()
    batch.draw()

    if pausado:
        label_pausa.draw()

    # desenhar comida
    cx, cy = comida
    comida_rect = shapes.Rectangle(
        cx, converter_y_para_pyglet(cy), TAM_BLOCO, TAM_BLOCO, color=VERMELHO)
    comida_rect.draw()

    # desenhar cobra
    for (bx, by) in cauda:
        bloco = shapes.Rectangle(bx, converter_y_para_pyglet(
            by), TAM_BLOCO, TAM_BLOCO, color=VERDE)
        bloco.draw()

    if pausado:
        label_pausa.draw()


@janela.event
def on_key_press(symbol, modifiers):
    global direcao, pausado
    print("Tecla pressionada:", symbol)

    if symbol == key.SPACE:
        pausado = not pausado
        return
    if pausado:
        return

    if symbol == key.RIGHT and direcao != "esquerda":
        direcao = "direita"
    elif symbol == key.LEFT and direcao != "direita":
        direcao = "esquerda"
    elif symbol == key.UP and direcao != "baixo":
        direcao = "cima"
    elif symbol == key.DOWN and direcao != "cima":
        direcao = "baixo"


def resetar_jogo():
    global x, y, direcao, cauda, tamanho_cobra, comida, recorde

    pontuacao = tamanho_cobra - 2
    if pontuacao > recorde:
        recorde = pontuacao
        with open("recorde.txt", "w") as f:
            f.write(str(recorde))

    x, y = 275, 275
    direcao = "parado"
    tamanho_cobra = 2
    cauda = [(x, y)]
    comida = sortear_comida()
    som_morte.play()


def atualizar(dt):
    global x, y, cauda, tamanho_cobra, comida

    if pausado or direcao == "parado":
        return

    if direcao == "direita":
        x += TAM_BLOCO
    elif direcao == "esquerda":
        x -= TAM_BLOCO
    elif direcao == "cima":
        y -= TAM_BLOCO
    elif direcao == "baixo":
        y += TAM_BLOCO

    nova_cabeca = (x, y)
    cauda.insert(0, nova_cabeca)

    # Comer
    if nova_cabeca == comida:
        tamanho_cobra += 1
        comida = sortear_comida()
        som_comer.play()
    else:
        cauda = cauda[:tamanho_cobra]

    # Colisões
    bateu_borda = (x < 0 or x > LARGURA - TAM_BLOCO or y <
                   PAINEL_ALTURA or y > ALTURA - TAM_BLOCO)
    bateu_corpo = nova_cabeca in cauda[1:]

    if bateu_borda or bateu_corpo:
        resetar_jogo()

    pontuacao_label.text = f"Pontuação: {tamanho_cobra - 2}"
    recorde_label.text = f"Recorde: {recorde}"


pyglet.clock.schedule_interval(atualizar, INTERVALO)

# para garantir que a tela está aberta.
print("Jogo iniciado! clique na janela e use as setas para jogar.")
pyglet.app.run()
