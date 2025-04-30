from flask import Flask, render_template_string

app = Flask(__name__)

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Flappy Bird</title>
  <style>
    body {
      margin: 0;
      overflow: hidden;
      background-color: skyblue;
    }
    canvas {
      display: block;
      background: #70c5ce;
    }
    #retryButton {
      display: none;
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      padding: 10px 20px;
      font-size: 20px;
      background-color: orange;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <canvas id="gameCanvas"></canvas>
  <button id="retryButton" onclick="startGame()">Retry</button>
  <script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const retryButton = document.getElementById("retryButton");

    canvas.width = 400;
    canvas.height = 600;

    let bird, pipes, isGameOver, score, highScore, frame;

    function resetGame() {
      bird = {
        x: 50,
        y: canvas.height / 2,
        radius: 15,
        velocity: 0,
        gravity: 0.4,
        jump: -8,
        color: "orange"
      };
      pipes = [];
      isGameOver = false;
      score = 0;
      frame = 0;
    }

    highScore = 0;

    function drawBird() {
      ctx.beginPath();
      ctx.arc(bird.x, bird.y, bird.radius, 0, Math.PI * 2);
      ctx.fillStyle = bird.color;
      ctx.fill();
      ctx.stroke();
    }

    function drawPipes() {
      pipes.forEach(pipe => {
        ctx.fillStyle = "green";
        ctx.fillRect(pipe.x, 0, 60, pipe.top);
        ctx.fillRect(pipe.x, pipe.top + 160, 60, canvas.height - pipe.top - 160);
      });
    }

    function updatePipes() {
      if (frame % 100 === 0) {
        const topHeight = Math.random() * (canvas.height - 160 - 100) + 50;
        pipes.push({ x: canvas.width, top: topHeight });
      }

      pipes.forEach((pipe, index) => {
        pipe.x -= 2;

        if (pipe.x + 60 < 0) {
          pipes.splice(index, 1);
          score++;
        }

        if (
          bird.x + bird.radius > pipe.x &&
          bird.x - bird.radius < pipe.x + 60 &&
          (bird.y - bird.radius < pipe.top || bird.y + bird.radius > pipe.top + 160)
        ) {
          isGameOver = true;
        }
      });
    }

    function drawScore() {
      ctx.fillStyle = "white";
      ctx.font = "24px Arial";
      ctx.fillText(`Score: ${score}`, 10, 30);
      ctx.fillText(`High Score: ${highScore}`, 10, 60);
    }

    function gameLoop() {
      if (isGameOver) {
        if (score > highScore) {
          highScore = score;
        }

        ctx.fillStyle = "black";
        ctx.font = "36px Arial";
        ctx.fillText("Game Over", canvas.width / 2 - 80, canvas.height / 2);
        ctx.fillText(`Score: ${score}`, canvas.width / 2 - 60, canvas.height / 2 + 40);
        ctx.fillText(`High Score: ${highScore}`, canvas.width / 2 - 100, canvas.height / 2 + 80);

        retryButton.style.display = "block";
        return;
      }

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      bird.velocity += bird.gravity;
      bird.y += bird.velocity;

      if (bird.y + bird.radius > canvas.height || bird.y - bird.radius < 0) {
        isGameOver = true;
      }

      drawBird();
      updatePipes();
      drawPipes();
      drawScore();

      frame++;
      requestAnimationFrame(gameLoop);
    }

    function flap() {
      if (!isGameOver) bird.velocity = bird.jump;
    }

    function startGame() {
      resetGame();
      retryButton.style.display = "none";
      gameLoop();
    }

    window.addEventListener("keydown", (e) => {
      if (e.code === "Space") flap();
    });

    window.addEventListener("mousedown", () => {
      flap();
    });

    startGame();
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_code)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)