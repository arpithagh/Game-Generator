import os
import gradio as gr
import base64
from langchain_openai import OpenAI

# Set your API Key
os.environ["OPENAI_API_KEY"] = 'your-key-here'
llm = OpenAI(model="text-davinci-003", temperature=0.7)

# Toggle to disable LLM during testing
USE_LLM = False

def convert_html_to_iframe(html_str, width="100%", height="650px"):
    """Convert full HTML string to iframe HTML with base64 encoded data URI."""
    b64_html = base64.b64encode(html_str.encode('utf-8')).decode('utf-8')
    iframe_html = f"<iframe src='data:text/html;base64,{b64_html}' style='border:none;' width='{width}' height='{height}'></iframe>"
    return iframe_html

def generate_game_html(description):
    try:
        if USE_LLM:
            refined_description = llm.run(f"Based on the description '{description}', suggest a game type.")
        else:
            refined_description = description  # Direct fallback

        description_lower = refined_description.lower()

        if any(word in description_lower for word in ['snake', 'eating', 'grow', 'food']):
            html = generate_snake_game(description)
        elif any(word in description_lower for word in ['pong', 'paddle', 'ball', 'bounce']):
            html = generate_pong_game(description)
        elif any(word in description_lower for word in ['flappy', 'bird', 'fly', 'jump', 'obstacle']):
            html = generate_flappy_game(description)
        elif any(word in description_lower for word in ['breakout', 'brick', 'break', 'blocks']):
            html = generate_breakout_game(description)
        elif any(word in description_lower for word in ['maze', 'labyrinth', 'navigate']):
            html = generate_maze_game(description)
        elif any(word in description_lower for word in ['dino']):
            html = generate_dino_game(description)
        else:
            html = generate_simple_clicker_game(description)

        return convert_html_to_iframe(html, width="100%", height="650px")
    
    except Exception as e:
        return f"<p style='color:red;'>Error generating game: {str(e)}</p>"

def generate_snake_game(description):
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Snake Game</title>
    <style>
        body { 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            margin: 0; 
            background: #111;
            font-family: Arial, sans-serif;
        }
        canvas { 
            border: 2px solid #fff; 
            background: #000;
        }
        .info {
            color: white;
            text-align: center;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div>
        <div class="info">
            <h2>Snake Game</h2>
            <p>Score: <span id="score">0</span></p>
            <p>Use WASD or Arrow Keys to move</p>
        </div>
        <canvas id="gameCanvas" width="400" height="400"></canvas>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const scoreElement = document.getElementById('score');

        const gridSize = 20;
        let snake = [{x: 200, y: 200}];
        let direction = {x: 0, y: 0};
        let food = {x: 100, y: 100};
        let score = 0;

        function drawGame() {
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = '#0f0';
            snake.forEach(segment => {
                ctx.fillRect(segment.x, segment.y, gridSize, gridSize);
            });

            ctx.fillStyle = '#f00';
            ctx.fillRect(food.x, food.y, gridSize, gridSize);
        }

        function moveSnake() {
            const head = {x: snake[0].x + direction.x, y: snake[0].y + direction.y};

            if (head.x < 0 || head.x >= canvas.width || head.y < 0 || head.y >= canvas.height) {
                resetGame();
                return;
            }

            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                resetGame();
                return;
            }

            snake.unshift(head);

            if (head.x === food.x && head.y === food.y) {
                score++;
                scoreElement.textContent = score;
                generateFood();
            } else {
                snake.pop();
            }
        }

        function generateFood() {
            food = {
                x: Math.floor(Math.random() * (canvas.width / gridSize)) * gridSize,
                y: Math.floor(Math.random() * (canvas.height / gridSize)) * gridSize
            };
        }

        function resetGame() {
            snake = [{x: 200, y: 200}];
            direction = {x: 0, y: 0};
            score = 0;
            scoreElement.textContent = score;
            generateFood();
        }

        document.addEventListener('keydown', (e) => {
            switch(e.key) {
                case 'ArrowUp':
                case 'w':
                case 'W':
                    if (direction.y === 0) direction = {x: 0, y: -gridSize};
                    break;
                case 'ArrowDown':
                case 's':
                case 'S':
                    if (direction.y === 0) direction = {x: 0, y: gridSize};
                    break;
                case 'ArrowLeft':
                case 'a':
                case 'A':
                    if (direction.x === 0) direction = {x: -gridSize, y: 0};
                    break;
                case 'ArrowRight':
                case 'd':
                case 'D':
                    if (direction.x === 0) direction = {x: gridSize, y: 0};
                    break;
            }
        });

        function gameLoop() {
            moveSnake();
            drawGame();
        }

        generateFood();
        drawGame();
        setInterval(gameLoop, 150);
    </script>
</body>
</html>
    """

def generate_pong_game(description):
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Pong Game</title>
    <style>
        body { 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            margin: 0; 
            background: #111;
            font-family: Arial, sans-serif;
        }
        canvas { 
            border: 2px solid #fff; 
            background: #000;
        }
        .info {
            color: white;
            text-align: center;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div>
        <div class="info">
            <h2>Pong Game</h2>
            <p>Player: <span id="playerScore">0</span> | AI: <span id="aiScore">0</span></p>
            <p>Use W/S or Up/Down arrows to move</p>
        </div>
        <canvas id="gameCanvas" width="600" height="400"></canvas>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        const game = {
            player: { x: 10, y: canvas.height/2 - 50, width: 10, height: 100, speed: 5, score: 0 },
            ai: { x: canvas.width - 20, y: canvas.height/2 - 50, width: 10, height: 100, speed: 3, score: 0 },
            ball: { x: canvas.width/2, y: canvas.height/2, size: 10, speedX: 4, speedY: 3 }
        };

        const keys = {};

        function draw() {
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.strokeStyle = '#fff';
            ctx.setLineDash([5, 15]);
            ctx.beginPath();
            ctx.moveTo(canvas.width/2, 0);
            ctx.lineTo(canvas.width/2, canvas.height);
            ctx.stroke();

            ctx.fillStyle = '#fff';
            ctx.fillRect(game.player.x, game.player.y, game.player.width, game.player.height);
            ctx.fillRect(game.ai.x, game.ai.y, game.ai.width, game.ai.height);

            ctx.beginPath();
            ctx.arc(game.ball.x, game.ball.y, game.ball.size, 0, Math.PI * 2);
            ctx.fill();
        }

        function update() {
            if (keys['ArrowUp'] || keys['w'] || keys['W']) {
                game.player.y = Math.max(0, game.player.y - game.player.speed);
            }
            if (keys['ArrowDown'] || keys['s'] || keys['S']) {
                game.player.y = Math.min(canvas.height - game.player.height, game.player.y + game.player.speed);
            }

            const aiCenter = game.ai.y + game.ai.height / 2;
            if (aiCenter < game.ball.y - 35) {
                game.ai.y += game.ai.speed;
            } else if (aiCenter > game.ball.y + 35) {
                game.ai.y -= game.ai.speed;
            }

            game.ball.x += game.ball.speedX;
            game.ball.y += game.ball.speedY;

            if (game.ball.y <= 0 || game.ball.y >= canvas.height) {
                game.ball.speedY = -game.ball.speedY;
            }

            if (game.ball.x <= game.player.x + game.player.width &&
                game.ball.y >= game.player.y &&
                game.ball.y <= game.player.y + game.player.height) {
                game.ball.speedX = -game.ball.speedX;
            }

            if (game.ball.x >= game.ai.x &&
                game.ball.y >= game.ai.y &&
                game.ball.y <= game.ai.y + game.ai.height) {
                game.ball.speedX = -game.ball.speedX;
            }

            if (game.ball.x < 0) {
                game.ai.score++;
                document.getElementById('aiScore').textContent = game.ai.score;
                resetBall();
            }
            if (game.ball.x > canvas.width) {
                game.player.score++;
                document.getElementById('playerScore').textContent = game.player.score;
                resetBall();
            }
        }

        function resetBall() {
            game.ball.x = canvas.width / 2;
            game.ball.y = canvas.height / 2;
            game.ball.speedX = -game.ball.speedX;
        }

        document.addEventListener('keydown', (e) => keys[e.key] = true);
        document.addEventListener('keyup', (e) => keys[e.key] = false);

        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }

        gameLoop();
    </script>
</body>
</html>
    """

def generate_flappy_game(description):
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Flappy Game</title>
    <style>
        body { 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            margin: 0; 
            background: #87CEEB;
            font-family: Arial, sans-serif;
            user-select: none;
        }
        canvas { 
            border: 2px solid #000; 
            background: linear-gradient(#87CEEB, #98FB98);
            display: block;
            margin: 0 auto;
        }
        .info {
            color: #000;
            text-align: center;
            margin-bottom: 10px;
        }
        #startMessage {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 28px;
            font-weight: bold;
            color: #fff;
            background: rgba(0,0,0,0.7);
            padding: 20px 40px;
            border-radius: 10px;
            cursor: pointer;
            user-select: none;
            z-index: 10;
        }
    </style>
</head>
<body>
    <div>
        <div class="info">
            <h2>Flappy Game</h2>
            <p>Score: <span id="score">0</span></p>
            <p>Press SPACE or click to jump</p>
        </div>
        <canvas id="gameCanvas" width="400" height="600"></canvas>
        <div id="startMessage">Click or Press SPACE to Start</div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const startMessage = document.getElementById('startMessage');
        const scoreEl = document.getElementById('score');

        const game = {
            bird: { x: 50, y: 300, size: 20, velocity: 0, gravity: 0.6, jump: -10 },
            pipes: [],
            score: 0,
            gameOver: false,
            running: false
        };

        function drawBird() {
            ctx.fillStyle = '#FFD700';
            ctx.beginPath();
            ctx.arc(game.bird.x, game.bird.y, game.bird.size, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#000';
            ctx.beginPath();
            ctx.arc(game.bird.x + 5, game.bird.y - 5, 3, 0, Math.PI * 2);
            ctx.fill();
        }

        function drawPipes() {
            ctx.fillStyle = '#228B22';
            game.pipes.forEach(pipe => {
                ctx.fillRect(pipe.x, 0, pipe.width, pipe.top);
                ctx.fillRect(pipe.x, pipe.bottom, pipe.width, canvas.height - pipe.bottom);
            });
        }

        function updateBird() {
            game.bird.velocity += game.bird.gravity;
            game.bird.y += game.bird.velocity;

            if (game.bird.y + game.bird.size > canvas.height || game.bird.y - game.bird.size < 0) {
                game.gameOver = true;
                game.running = false;
                showStartMessage("Game Over! Click or Press SPACE to Restart");
            }
        }

        function updatePipes() {
            if (game.pipes.length === 0 || game.pipes[game.pipes.length - 1].x < canvas.width - 250) {
                const gap = 180;
                const minTop = 50;
                const maxTop = canvas.height - gap - 50;
                const top = Math.random() * (maxTop - minTop) + minTop;
                game.pipes.push({
                    x: canvas.width,
                    width: 50,
                    top: top,
                    bottom: top + gap,
                    passed: false
                });
            }

            game.pipes.forEach((pipe, index) => {
                pipe.x -= 3;

                if (pipe.x + pipe.width < 0) {
                    game.pipes.splice(index, 1);
                }

                if (!pipe.passed && pipe.x + pipe.width < game.bird.x) {
                    pipe.passed = true;
                    game.score++;
                    scoreEl.textContent = game.score;
                }

                if (game.bird.x + game.bird.size > pipe.x && 
                    game.bird.x - game.bird.size < pipe.x + pipe.width) {
                    if (game.bird.y - game.bird.size < pipe.top || 
                        game.bird.y + game.bird.size > pipe.bottom) {
                        game.gameOver = true;
                        game.running = false;
                        showStartMessage("Game Over! Click or Press SPACE to Restart");
                    }
                }
            });
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawPipes();
            drawBird();
        }

        function jump() {
            if (!game.running) {
                startGame();
            } else {
                game.bird.velocity = game.bird.jump;
            }
        }

        function startGame() {
            game.bird.y = 300;
            game.bird.velocity = 0;
            game.pipes = [];
            game.score = 0;
            game.gameOver = false;
            game.running = true;
            scoreEl.textContent = '0';
            hideStartMessage();
        }

        function showStartMessage(msg=null) {
            startMessage.textContent = msg || "Click or Press SPACE to Start";
            startMessage.style.display = 'block';
        }

        function hideStartMessage() {
            startMessage.style.display = 'none';
        }

        function gameLoop() {
            if (game.running && !game.gameOver) {
                updateBird();
                updatePipes();
            }
            draw();
            requestAnimationFrame(gameLoop);
        }

        startMessage.addEventListener('click', jump);
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space') {
                e.preventDefault();
                jump();
            }
        });

        showStartMessage();
        gameLoop();
    </script>
</body>
</html>
    """


def generate_breakout_game(description):
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Breakout Game</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: #111;
            font-family: Arial, sans-serif;
        }
        canvas {
            border: 2px solid #fff;
            background: #000;
        }
        .info {
            color: white;
            text-align: center;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div>
        <div class="info">
            <h2>Breakout Game</h2>
            <p>Score: <span id="score">0</span> | Lives: <span id="lives">3</span></p>
            <p>Use mouse or A/D keys to move paddle. Press any key or click to restart.</p>
        </div>
        <canvas id="gameCanvas" width="480" height="320"></canvas>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        let game = {};
        const keys = {};
        const brickRows = 5;
        const brickCols = 8;
        const brickWidth = 55;
        const brickHeight = 20;
        const brickPadding = 5;
        const brickOffsetTop = 60;
        const brickOffsetLeft = 30;

        function resetGame() {
            game = {
                paddle: { x: canvas.width/2 - 40, y: canvas.height - 20, width: 80, height: 10, speed: 7 },
                ball: { x: canvas.width/2, y: canvas.height - 30, dx: 2, dy: -2, radius: 8 },
                bricks: [],
                score: 0,
                lives: 3,
                gameOver: false,
                won: false
            };

            for (let c = 0; c < brickCols; c++) {
                game.bricks[c] = [];
                for (let r = 0; r < brickRows; r++) {
                    game.bricks[c][r] = {
                        x: c * (brickWidth + brickPadding) + brickOffsetLeft,
                        y: r * (brickHeight + brickPadding) + brickOffsetTop,
                        status: 1,
                        color: "hsl(" + (r * 60) + ", 70%, 60%)"
                    };
                }
            }

            document.getElementById('score').textContent = game.score;
            document.getElementById('lives').textContent = game.lives;
        }

        function drawBall() {
            ctx.beginPath();
            ctx.arc(game.ball.x, game.ball.y, game.ball.radius, 0, Math.PI * 2);
            ctx.fillStyle = '#fff';
            ctx.fill();
        }

        function drawPaddle() {
            ctx.fillStyle = '#fff';
            ctx.fillRect(game.paddle.x, game.paddle.y, game.paddle.width, game.paddle.height);
        }

        function drawBricks() {
            for (let c = 0; c < brickCols; c++) {
                for (let r = 0; r < brickRows; r++) {
                    const brick = game.bricks[c][r];
                    if (brick.status === 1) {
                        ctx.fillStyle = brick.color;
                        ctx.fillRect(brick.x, brick.y, brickWidth, brickHeight);
                    }
                }
            }
        }

        function collisionDetection() {
            for (let c = 0; c < brickCols; c++) {
                for (let r = 0; r < brickRows; r++) {
                    const brick = game.bricks[c][r];
                    if (brick.status === 1 &&
                        game.ball.x > brick.x && game.ball.x < brick.x + brickWidth &&
                        game.ball.y > brick.y && game.ball.y < brick.y + brickHeight) {
                        game.ball.dy = -game.ball.dy;
                        brick.status = 0;
                        game.score += 10;
                        document.getElementById('score').textContent = game.score;

                        if (game.score === brickRows * brickCols * 10) {
                            game.won = true;
                        }
                    }
                }
            }
        }

        function updateBall() {
            game.ball.x += game.ball.dx;
            game.ball.y += game.ball.dy;

            if (game.ball.x < game.ball.radius || game.ball.x > canvas.width - game.ball.radius)
                game.ball.dx = -game.ball.dx;

            if (game.ball.y < game.ball.radius)
                game.ball.dy = -game.ball.dy;

            if (game.ball.y > canvas.height - game.ball.radius) {
                if (game.ball.x > game.paddle.x && game.ball.x < game.paddle.x + game.paddle.width) {
                    game.ball.dy = -game.ball.dy;
                } else {
                    game.lives--;
                    document.getElementById('lives').textContent = game.lives;
                    if (game.lives === 0) {
                        game.gameOver = true;
                    } else {
                        game.ball.x = canvas.width / 2;
                        game.ball.y = canvas.height - 30;
                        game.ball.dx = 2;
                        game.ball.dy = -2;
                        game.paddle.x = canvas.width / 2 - 40;
                    }
                }
            }
        }

        function updatePaddle() {
            if (keys['ArrowLeft'] || keys['a'] || keys['A']) {
                game.paddle.x = Math.max(0, game.paddle.x - game.paddle.speed);
            }
            if (keys['ArrowRight'] || keys['d'] || keys['D']) {
                game.paddle.x = Math.min(canvas.width - game.paddle.width, game.paddle.x + game.paddle.speed);
            }
        }

        function drawOverlay(text) {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#fff';
            ctx.font = '24px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(text, canvas.width / 2, canvas.height / 2);
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawBricks();
            drawBall();
            drawPaddle();

            if (game.gameOver) drawOverlay('GAME OVER - Click or Press Any Key to Restart');
            else if (game.won) drawOverlay('YOU WIN! Click or Press Any Key to Restart');
        }

        function gameLoop() {
            if (!game.gameOver && !game.won) {
                updateBall();
                updatePaddle();
                collisionDetection();
            }
            draw();
            requestAnimationFrame(gameLoop);
        }

        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            game.paddle.x = mouseX - game.paddle.width / 2;
            game.paddle.x = Math.max(0, Math.min(canvas.width - game.paddle.width, game.paddle.x));
        });

        document.addEventListener('keydown', (e) => {
            if (game.gameOver || game.won) resetGame();
            keys[e.key] = true;
        });

        document.addEventListener('keyup', (e) => keys[e.key] = false);
        canvas.addEventListener('click', () => {
            if (game.gameOver || game.won) resetGame();
        });

        resetGame();
        gameLoop();
    </script>
</body>
</html>
    """


def generate_maze_game(description="maze"):
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Maze Game</title>
    <style>
        body { 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            margin: 0; 
            background: #111;
            font-family: Arial, sans-serif;
        }
        canvas { 
            border: 2px solid #fff; 
            background: #000;
        }
        .info {
            color: white;
            text-align: center;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div>
        <div class="info">
            <h2>Maze Game</h2>
            <p>Find the exit! Use WASD or Arrow Keys</p>
            <p>Time: <span id="timer">0</span>s</p>
        </div>
        <canvas id="gameCanvas" width="480" height="480"></canvas>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        const cellSize = 20;
        const rows = canvas.height / cellSize;
        const cols = canvas.width / cellSize;

        const maze = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,0,1],
            [1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,1,0,1],
            [1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,1,0,1],
            [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
            [1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
            [1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1],
            [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1],
            [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1]
        ];

        const player = { x: 1, y: 1 };
        const exit = { x: 22, y: 23 };
        let startTime = Date.now();
        let gameWon = false;

        function drawMaze() {
            for (let row = 0; row < maze.length; row++) {
                for (let col = 0; col < maze[row].length; col++) {
                    const x = col * cellSize;
                    const y = row * cellSize;
                    
                    if (maze[row][col] === 1) {
                        ctx.fillStyle = '#333';
                        ctx.fillRect(x, y, cellSize, cellSize);
                    } else if (maze[row][col] === 2) {
                        ctx.fillStyle = '#0f0';
                        ctx.fillRect(x, y, cellSize, cellSize);
                    } else {
                        ctx.fillStyle = '#000';
                        ctx.fillRect(x, y, cellSize, cellSize);
                    }
                }
            }
        }

        function drawPlayer() {
            ctx.fillStyle = '#ff0';
            ctx.beginPath();
            ctx.arc(
                player.x * cellSize + cellSize/2, 
                player.y * cellSize + cellSize/2, 
                cellSize/3, 
                0, 
                Math.PI * 2
            );
            ctx.fill();
        }

        function movePlayer(dx, dy) {
            const newX = player.x + dx;
            const newY = player.y + dy;
            
            if (newY >= 0 && newY < maze.length && 
                newX >= 0 && newX < maze[newY].length && 
                maze[newY][newX] !== 1) {
                player.x = newX;
                player.y = newY;
                
                if (maze[newY][newX] === 2) {
                    gameWon = true;
                }
            }
        }

        function updateTimer() {
            if (!gameWon) {
                const elapsed = Math.floor((Date.now() - startTime) / 1000);
                document.getElementById('timer').textContent = elapsed;
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawMaze();
            drawPlayer();
            
            if (gameWon) {
                ctx.fillStyle = 'rgba(0, 255, 0, 0.8)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#fff';
                ctx.font = '30px Arial';
                ctx.textAlign = 'center';
                ctx.fillText('YOU WIN!', canvas.width/2, canvas.height/2);
                ctx.font = '20px Arial';
                const time = Math.floor((Date.now() - startTime) / 1000);
                ctx.fillText(`Time: ${time} seconds`, canvas.width/2, canvas.height/2 + 40);
            }
        }

        document.addEventListener('keydown', (e) => {
            if (!gameWon) {
                switch(e.key) {
                    case 'ArrowUp':
                    case 'w':
                    case 'W':
                        movePlayer(0, -1);
                        break;
                    case 'ArrowDown':
                    case 's':
                    case 'S':
                        movePlayer(0, 1);
                        break;
                    case 'ArrowLeft':
                    case 'a':
                    case 'A':
                        movePlayer(-1, 0);
                        break;
                    case 'ArrowRight':
                    case 'd':
                    case 'D':
                        movePlayer(1, 0);
                        break;
                }
            }
        });

        function gameLoop() {
            updateTimer();
            draw();
            requestAnimationFrame(gameLoop);
        }

        gameLoop();
    </script>
</body>
</html>
    """


def generate_simple_clicker_game(description):
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Simple Clicker Game</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: #222;
            color: white;
            font-family: Arial, sans-serif;
        }
        button {
            padding: 20px 40px;
            font-size: 2em;
            background: #0f0;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 0 10px #0f0;
            transition: background 0.3s ease;
        }
        button:hover {
            background: #0c0;
        }
        .score {
            margin-top: 20px;
            font-size: 2em;
        }
    </style>
</head>
<body>
    <h1>Simple Clicker Game</h1>
    <button id="clickerBtn">Click Me!</button>
    <div class="score">Score: <span id="score">0</span></div>

    <script>
        const btn = document.getElementById('clickerBtn');
        const scoreEl = document.getElementById('score');
        let score = 0;

        btn.addEventListener('click', () => {
            score++;
            scoreEl.textContent = score;
        });
    </script>
</body>
</html>
    """

def generate_dino_game(description="dino"):
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dino Game</title>
    <style>
        body {
            margin: 0;
            background: #f0f0f0;
            font-family: 'Segoe UI', sans-serif;
            overflow: hidden;
        }
        canvas {
            display: block;
            margin: 0 auto;
            background-color: #fff;
            border-bottom: 2px solid #555;
        }
        #startMessage {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 24px;
            font-weight: bold;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 20px 40px;
            border-radius: 10px;
            z-index: 10;
            cursor: pointer;
        }
        #scoreDisplay {
            position: absolute;
            top: 10px;
            right: 20px;
            font-size: 18px;
            color: #333;
        }
    </style>
</head>
<body>
    <div id="startMessage">Press SPACE or Click to Start</div>
    <div id="scoreDisplay">Score: <span id="score">0</span></div>

    <!-- Dino and Tree images -->
    <img id="dinoImage" src="https://i.postimg.cc/WdPC6ywY/free-vector-illustration-cute-green-dinosaur-kids-1060459-129.jpg" style="display:none;" />
    <img id="treeImage" src="https://i.postimg.cc/bSPZg3G0/pine-tree-illustration-flat-2d-vector-art-style-961038-14549.jpg" style="display:none;" />

    <canvas id="gameCanvas" width="800" height="300"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const startMessage = document.getElementById("startMessage");
        const scoreDisplay = document.getElementById("score");
        const dinoImg = document.getElementById("dinoImage");
        const treeImg = document.getElementById("treeImage");

        const dino = {
            x: 50,
            y: 250,
            width: 50,
            height: 50,
            velocityY: 0,
            gravity: 0.8,
            jumpPower: -16,
            maxFallSpeed: 12,
            grounded: true
        };

        let obstacles = [];
        let gameSpeed = 5;
        let score = 0;
        let running = false;
        let gameOver = false;

        function drawDino() {
            ctx.drawImage(dinoImg, dino.x, dino.y, dino.width, dino.height);
        }

        function drawObstacles() {
            obstacles.forEach(obs => {
                ctx.drawImage(treeImg, obs.x, obs.y, obs.width, obs.height);
            });
        }

        function updateDino() {
            dino.velocityY += dino.gravity;
            if (dino.velocityY > dino.maxFallSpeed) dino.velocityY = dino.maxFallSpeed;
            dino.y += dino.velocityY;

            if (dino.y >= 250) {
                dino.y = 250;
                dino.velocityY = 0;
                dino.grounded = true;
            }
        }

        function updateObstacles() {
            if (obstacles.length === 0 || obstacles[obstacles.length - 1].x < 500) {
                const height = 40 + Math.random() * 30;
                obstacles.push({
                    x: canvas.width,
                    y: 300 - height,
                    width: 30,
                    height: height,
                    passed: false
                });
            }

            obstacles.forEach((obs, index) => {
                obs.x -= gameSpeed;

                if (!obs.passed && obs.x + obs.width < dino.x) {
                    obs.passed = true;
                    score++;
                    scoreDisplay.textContent = score;
                }

                if (
                    dino.x < obs.x + obs.width &&
                    dino.x + dino.width > obs.x &&
                    dino.y < obs.y + obs.height &&
                    dino.y + dino.height > obs.y
                ) {
                    gameOver = true;
                    running = false;
                    showMessage("Game Over! Click or Press SPACE to Restart");
                }

                if (obs.x + obs.width < 0) {
                    obstacles.splice(index, 1);
                }
            });
        }

        function jump() {
            if (!running || gameOver) {
                startGame();
            } else if (dino.grounded) {
                dino.velocityY = dino.jumpPower;
                dino.grounded = false;
            }
        }

        function showMessage(msg = "Press SPACE or Click to Start") {
            startMessage.textContent = msg;
            startMessage.style.display = "block";
        }

        function hideMessage() {
            startMessage.style.display = "none";
        }

        function startGame() {
            obstacles = [];
            dino.y = 250;
            dino.velocityY = 0;
            dino.grounded = true;
            score = 0;
            gameOver = false;
            running = true;
            scoreDisplay.textContent = score;
            hideMessage();
        }

        function drawGround() {
            ctx.strokeStyle = "#000";
            ctx.beginPath();
            ctx.moveTo(0, 290);
            ctx.lineTo(canvas.width, 290);
            ctx.stroke();
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawGround();
            drawDino();
            drawObstacles();
        }

        function update() {
            if (running && !gameOver) {
                updateDino();
                updateObstacles();
            }
        }

        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }

        startMessage.addEventListener("click", jump);
        document.addEventListener("keydown", (e) => {
            if (e.code === "Space" || e.code === "Enter") {
                e.preventDefault();
                jump();
            }
        });

        let imagesLoaded = 0;
        function tryStartLoop() {
            imagesLoaded++;
            if (imagesLoaded === 2) {
                showMessage();
                gameLoop();
            }
        }

        dinoImg.onload = tryStartLoop;
        treeImg.onload = tryStartLoop;
    </script>
</body>
</html>
    """

def launch_gradio_app():
    with gr.Blocks(css="""
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(to right, #fdfbfb, #ebedee);
        }
        .centered {
            max-width: 600px;
            margin: auto;
            padding: 40px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }
        .output-area {
            max-width: 800px;
            margin: 30px auto 0 auto;
            padding: 20px;
        }
    """) as demo:

        with gr.Column(elem_classes="centered"):
            gr.Markdown("## 🎮 Game Generator with LangChain")

            description = gr.Textbox(
                label="Enter a game description", 
                placeholder="Try 'snake', 'pong', 'flappy bird' etc.",
                lines=1
            )
            submit_btn = gr.Button("Generate Game")

        # 👇 Output section now outside the white box
        with gr.Column(elem_classes="output-area"):
            output = gr.HTML(label="Generated Game", elem_id="game_output")

        # 🔄 Function to update output
        def update_output(desc):
            try:
                if not desc.strip():
                    return "<p style='color:red;'>Please enter a game description.</p>"
                html_output = generate_game_html(desc)
                print("DEBUG HTML OUTPUT:", html_output[:500])
                return html_output
            except Exception as e:
                return f"<p style='color:red;'>Error: {str(e)}</p>"

        # Connect logic
        submit_btn.click(update_output, inputs=description, outputs=output)
        description.submit(update_output, inputs=description, outputs=output)

    demo.launch()


if __name__ == "__main__":
    launch_gradio_app()
