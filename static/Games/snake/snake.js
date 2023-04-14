/*
Create by Learn Web Developement
Youtube channel : https://www.youtube.com/channel/UC8n8ftV94ZU_DJLOLtrpORA
*/

const cvs = document.getElementById("SnakeGame");
const ctx = cvs.getContext("2d");

// create the unit
let box = 32;
cvs.style.width = 1000+"px";
cvs.style.height = 1000 + "px";
//cvs.style.width = window.screen.availWidth-400+"px";
//cvs.style.height = window.screen.availHeight-200 + "px";
if (window.screen.availWidth < 768) {
    //box = box / 2;
    cvs.style.width = window.screen.availWidth + "px";
    cvs.style.height = window.screen.availHeight + "px";
}
//alert(window.screen.availWidth);
//alert(window.screen.availHeight);
// load images

const ground = new Image();
ground.src = "../../static/Games/Snake/img/ground.png";

const foodImg = new Image();
foodImg.src = "../../static/Games/Snake/img/food.png";

// load audio files

let dead = new Audio();
let eat = new Audio();
let up = new Audio();
let right = new Audio();
let left = new Audio();
let down = new Audio();

dead.src = "../../static/Games/Snake/audio/dead.mp3";
eat.src = "../../static/Games/Snake/audio/eat.mp3";
up.src = "../../static/Games/Snake/audio/up.mp3";
right.src = "../../static/Games/Snake/audio/right.mp3";
left.src = "../../static/Games/Snake/audio/left.mp3";
down.src = "../../static/Games/Snake/audio/down.mp3";

// create the snake

let snake = [];

snake[0] = {
    x : 9 * box,
    y : 10 * box
};

// create the food

let food = {
    x : Math.floor(Math.random()*17+1) * box,
    y : Math.floor(Math.random()*15+3) * box
}

// create the score var

let score = 0;
//refresh the game
function RefreshGame() {
    d = ''; 
    snake = [];
    snake[0] = {
        x: 9 * box,
        y: 10 * box
    };
    food = {
        x: Math.floor(Math.random() * 17 + 1) * box,
        y: Math.floor(Math.random() * 15 + 3) * box
    };
}
//start game
const startScreen = document.querySelector('.startScreen');

startScreen.addEventListener('click', start);
let game;
function start() {
    
    RefreshGame()
    cvs.classList.remove('hide');
    startScreen.classList.add('hide');
    score = 0;
    // call draw function every 100 ms

    game = setInterval(draw, 100);


}
let d='';
function endGame() {
    d = ''; 
    cvs.classList.add('hide');
    startScreen.classList.remove('hide');
    startScreen.innerHTML = "<div class='IlonchaRasmi'></div><br /> O'yin tugadi <br /> Sizning yakuniy hisobingiz " + score +
            "<br /> O'yinni qayta boshlash uchun shu yerni bosing.";
}
//control the snake



document.addEventListener("keydown", direction);

function direction(event) {
    let key = event.keyCode;
    if ((key == 37 || key == 65) && d != "RIGHT") {
        left.play();
        d = "LEFT";
    } else if ((key == 38 || key == 87) && d != "DOWN") {
        d = "UP";
        up.play();
    } else if ((key == 39 || key == 68) && d != "LEFT") {
        d = "RIGHT";
        right.play();
    } else if ((key == 40 || key == 83) && d != "UP") {
        d = "DOWN";
        down.play();
    }
}

// cheack collision function
function collision(head, array) {
    for (let i = 0; i < array.length; i++) {
        if (head.x == array[i].x && head.y == array[i].y) {
            return true;
        }
    }
    return false;
}

// draw everything to the canvas

function draw() {
    ctx.drawImage(ground, 0, 0);

    for (let i = 0; i < snake.length; i++) {
        ctx.fillStyle = (i == 0) ? "green" : "white";
        ctx.fillRect(snake[i].x, snake[i].y, box, box);


        ctx.strokeStyle = "red";
        ctx.strokeRect(snake[i].x, snake[i].y, box, box);
    }

    ctx.drawImage(foodImg, food.x, food.y);

    // old head position
    let snakeX = snake[0].x;
    let snakeY = snake[0].y;
    // which direction
    if (d == "LEFT") snakeX -= box;
    if (d == "UP") snakeY -= box;
    if (d == "RIGHT") snakeX += box;
    if (d == "DOWN") snakeY += box;

    // if the snake eats the food
    if (snakeX == food.x && snakeY == food.y) {
        score++;
        eat.play();
        food = {
            x: Math.floor(Math.random() * 17 + 1) * box,
            y: Math.floor(Math.random() * 15 + 3) * box
        }
        // we don't remove the tail
    } else {
        // remove the tail
        snake.pop();
    }

    // add new Head

    let newHead = {
        x: snakeX,
        y: snakeY
    }

    // game over

    if (snakeX < box || snakeX > 17 * box || snakeY < 3 * box || snakeY > 17 * box || collision(newHead, snake)) {

        endGame();
        clearInterval(game);
        dead.play();

    }

    snake.unshift(newHead);

    ctx.fillStyle = "white";
    ctx.font = "45px Changa one";
    ctx.fillText(score, 2 * box, 1.6 * box);
}

















