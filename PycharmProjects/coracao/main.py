import turtle

# Configuração da janela
window = turtle.Screen()
window.bgcolor("pink")
window.title("Feliz dia dos namorados!")

# Configuração da caneta
pen = turtle.Turtle()
pen.color("red")
pen.fillcolor("red")
pen.pensize(3)
pen.speed(7)

# Desenho do coração no centro da tela
pen.up()
pen.goto(0, 0)  # Posiciona a caneta no centro
pen.down()

pen.begin_fill()
pen.left(140)  # Define o ângulo inicial para começar a desenhar o coração
pen.forward(112)  # Define o tamanho inicial do lado esquerdo do coração

# Desenho da curva do lado esquerdo do coração
for _ in range(200):
    pen.right(1)
    pen.forward(1)

pen.left(120)  # Move para o lado direito do coração

# Desenho da curva do lado direito do coração
for _ in range(200):
    pen.right(1)
    pen.forward(1)

pen.forward(112)  # Finaliza a parte inferior do coração
pen.end_fill()

# Posiciona a caneta para escrever a mensagem
pen.up()
pen.goto(0, -120)  # Move a caneta para baixo do coração, onde o texto será escrito
pen.down()
pen.color("black")

# Escreve a mensagem na tela
pen.write(
    "Para você que roubou meu coração. Eu  admiro-te muito , princesa!",
    align="center",
    font=("Arial", 12, "bold")  # Define o tamanho da fonte como 12
)

pen.hideturtle()
turtle.done()
