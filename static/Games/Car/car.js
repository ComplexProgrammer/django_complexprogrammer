
    const carGame = document.querySelector('.carGame');
    const score = document.querySelector('.score');
    const startScreen = document.querySelector('.startScreen');
    const gameArea = document.querySelector('.gameArea');

    startScreen.addEventListener('click', start);


        let player = {speed: 5, score: 0 };
        let keys = {ArrowUp: false, ArrowDown: false, ArrowLeft: false, ArrowRight: false, w: false, s: false, a: false, d: false, btn_arrow_left: false, btn_arrow_right: false, btn_arrow_up: false, btn_arrow_down: false };

        document.addEventListener('keydown', keyDown);
        document.addEventListener('keyup', keyUp);
        function keyDown(e) {
        e.preventDefault();
            keys[e.key] = true;
        }
        function keyUp(e) {
        e.preventDefault();
            keys[e.key] = false;
        }
        function isCollide(a, b) {
        aRec = a.getBoundingClientRect();
            bRec = b.getBoundingClientRect();
            return !((aRec.bottom < bRec.top) || (aRec.top > bRec.bottom) || (aRec.right < bRec.left) || (aRec.left > bRec.right));
        }
        function moveBackround() {
        let bg = document.querySelectorAll('.bg');

            bg.forEach(function (item) {

                if (item.y >= 700) {
        item.y -= 1311;
                }
                item.y += player.speed;
                item.style.top = item.y + "px";
            });
        }
        function moveLines() {
        let lines = document.querySelectorAll('.lines');
            lines.forEach(function (item) {
                if (item.y >= 3550) {
        item.y -= 3600;
                }
                item.y += player.speed;
                item.style.top = item.y + "px";
            });
        }
        function endGame() {
        player.start = false;
            startScreen.classList.remove('hide');
            startScreen.innerHTML = "<div class='HalokatRasmi'></div><br /> O'yin tugadi <br /> Sizning yakuniy hisobingiz " + player.score +
            "<br /> O'yinni qayta boshlash uchun shu yerni bosing.";
        }
        function moveEnemy(car) {
        let enemy = document.querySelectorAll('.enemy');
            enemy.forEach(function (item) {
                if (isCollide(car, item)) {
        document.getElementById('accident_sound').play();
                    console.log("Halokat");
                    endGame();
                }
                if (item.y >= 3550) {
        item.y = -150;
                    item.style.left = Math.floor(Math.random() * 340) + "px";
                }
                item.y += player.speed;
                item.style.top = item.y + "px";
            });
        }
        function gamePlay() {
        let car = document.querySelector('.car');
            let road = gameArea.getBoundingClientRect();
            if (player.start) {
                document.getElementById('driving_sound').play();
                moveLines();
                //moveBackround();
                moveEnemy(car);
                //road.bottom
                //window.screen.availWidth
                if ((keys.ArrowUp || keys.w || keys.btn_arrow_up) && player.y > (road.top + 70)) {
                    player.y -= player.speed;
                    //document.getElementById('go_sound').play();
                }
                if ((keys.ArrowDown || keys.s || keys.btn_arrow_down) && player.y < (window.screen.availHeight - 300)){
                    player.y += player.speed;
                    document.getElementById('stop_sound').play();
                }
                if ((keys.ArrowLeft || keys.a || keys.btn_arrow_left) && player.x > 0) {
                    player.x -= player.speed;
                }
                if ((keys.ArrowRight || keys.d || keys.btn_arrow_right) && player.x < (road.width - 60)){
                    player.x += player.speed;
                }
                car.style.top = player.y + "px";
                car.style.left = player.x + "px";
                window.requestAnimationFrame(gamePlay);
                player.score++;
                let ps = player.score - 1;
                score.innerText = "Hisob: " + ps;
            }
        }
        function start() {
        document.getElementById('starting_sound').play();
            gameArea.classList.remove('hide');
            startScreen.classList.add('hide');
            gameArea.innerHTML = "";
            player.start = true;
            player.score = 0;
            window.requestAnimationFrame(gamePlay);

            for (x = 0; x < 25; x++) {
        let roadLine = document.createElement('div');
                roadLine.setAttribute('class', 'lines');
                roadLine.y = (x * 150);
                roadLine.style.top = roadLine.y + "px";
                gameArea.appendChild(roadLine);
            }
            //for (x = 0; x < 10; x++) {
        //    let bg = document.createElement('div');
        //    bg.setAttribute('class', 'bg');
        //    bg.y = (x * 90);
        //    bg.style.top = bg.y + "px";
        //    carGame.appendChild(bg);
        //}
        let car = document.createElement('div');
            car.setAttribute('class', 'car');
            gameArea.appendChild(car);
            player.x = car.offsetLeft;
            player.y = car.offsetTop;

            let up = document.createElement('div');
            up.setAttribute('class', 'arrow_up');
            gameArea.appendChild(up);
            let down = document.createElement('div');
            down.setAttribute('class', 'arrow_down');
            gameArea.appendChild(down);
            let left = document.createElement('div');
            left.setAttribute('class', 'arrow_left');
            gameArea.appendChild(left);
            let right = document.createElement('div');
            right.setAttribute('class', 'arrow_right');
            gameArea.appendChild(right);
            const arrow_left = document.querySelector('.arrow_left');
            const arrow_right = document.querySelector('.arrow_right');
            const arrow_up = document.querySelector('.arrow_up');
            const arrow_down = document.querySelector('.arrow_down');
            arrow_left.addEventListener('mousedown', function (e) {
                keys['btn_arrow_left'] = true;
            });
            arrow_left.addEventListener('mouseup', function (e) {
                keys['btn_arrow_left'] = false;
            });
            arrow_right.addEventListener('mousedown', function (e) {
                keys['btn_arrow_right'] = true;
            });
            arrow_right.addEventListener('mouseup', function (e) {
                keys['btn_arrow_right'] = false;
            });
            arrow_up.addEventListener('mousedown', function (e) {
                keys['btn_arrow_up'] = true;
            });
            arrow_up.addEventListener('mouseup', function (e) {
                keys['btn_arrow_up'] = false;
            });
            arrow_down.addEventListener('mousedown', function (e) {
                keys['btn_arrow_down'] = true;
            });
            arrow_down.addEventListener('mouseup', function (e) {
                keys['btn_arrow_down'] = false;
            });

            arrow_left.addEventListener('touchstart', function (e) {
                keys['btn_arrow_left'] = true;
            });
            arrow_left.addEventListener('touchend', function (e) {
                keys['btn_arrow_left'] = false;
            });
            arrow_right.addEventListener('touchstart', function (e) {
                keys['btn_arrow_right'] = true;
            });
            arrow_right.addEventListener('touchend', function (e) {
                keys['btn_arrow_right'] = false;
            });
            arrow_up.addEventListener('touchstart', function (e) {
                keys['btn_arrow_up'] = true;
            });
            arrow_up.addEventListener('touchend', function (e) {
                keys['btn_arrow_up'] = false;
            });
            arrow_down.addEventListener('touchstart', function (e) {
                keys['btn_arrow_down'] = true;
            });
            arrow_down.addEventListener('touchend', function (e) {
                keys['btn_arrow_down'] = false;
            });
            for (x = 0; x < 16; x++) {
        let enemyCar = document.createElement('div');
                enemyCar.setAttribute('class', 'enemy');
                enemyCar.y = ((x + 1) * 225) * -1;
                enemyCar.style.top = enemyCar.y + "px";
                enemyCar.style.backgroundImage = randomCar();
                enemyCar.style.left = Math.floor(Math.random() * 340) + "px";
                gameArea.appendChild(enemyCar);
            }
        }
        function getRandomInt(max) {
            return Math.floor(Math.random() * Math.floor(max));
        }

        function randomCar() {
        let cars = [
                "url('../../static/Games/Car/Images/car1.png')",
                "url('../../static/Games/Car/Images/car2.png')",
                "url('../../static/Games/Car/Images/car3.png')",
                "url('../../static/Games/Car/Images/car4.png')",
                "url('../../static/Games/Car/Images/car5.png')",
                "url('../../static/Games/Car/Images/car6.png')",
                "url('../../static/Games/Car/Images/car7.png')",
                "url('../../static/Games/Car/Images/car8.png')",
            ];

            return cars[getRandomInt(8)];

        }
        function randomColor() {
        function c() {
            let hex = Math.floor(Math.random() * 256).toString(16);
            return ("0" + String(hex)).substr(-2);
        }
            return "#" + c + c() + c();
        }