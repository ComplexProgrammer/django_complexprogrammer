    //start game
    const startScreen = document.querySelector('.startScreen');
    
    startScreen.addEventListener('click', start);
    var playing = false;
    let score = 0;
    var k = {ArrowUp: 0, ArrowDown: 0, ArrowLeft: 0, ArrowRight: 0, w: 0, s: 0, a: 0, d: 0 };
    const ground = new Image();
    ground.src = "../../static/Games/Motorcycle/Images/Img_1.png";
    var c = document.getElementById('MotorcycleCanvas');
    c.width = window.screen.availWidth;
    c.height = window.screen.availHeight - 200;
    document.getElementById('MotorcycleBody').appendChild(c);
    var ctx = c.getContext("2d");
    ctx.drawImage(ground, 0, 0, c.width, c.height + 100);
    var t = 0;
    var speed = 0;
    var perm = [];
    loop();


    function start() {
        startScreen.classList.add('hide');

        t = 0;
        speed = 0;
        score = 0;

        player.x = 100;
        player.y = 0;
        player.ySpeed = 0;
        player.rot = 0;
        player.rSpeed = 0;
        playing = true;
        loop();

    }
    function stop() {
        playing = false;
        startScreen.classList.remove('hide');
        startScreen.innerHTML = "<div class='Rasm'></div><br /> O'yin tugadi <br /> Sizning yakuniy hisobingiz " + score +
        "<br /> O'yinni qayta boshlash uchun shu yerni bosing.";
    }

    while (perm.length < 255) {
        while (perm.includes(val = Math.floor(Math.random() * 255)));
        perm.push(val)
    }
    var lerp = (a, b, t) => a + (b - a) * (1 - Math.cos(t * Math.PI)) / 2;
    var noise = x => {
        x = x * 0.01 % 255;
        return lerp(perm[Math.floor(x)], perm[Math.ceil(x)], x - Math.floor(x));
    }
    var player = new function () {
        this.x = c.width / 2;
        this.x = 100;
        this.y = 0;
        this.ySpeed = 0;
        this.rot = 0;
        this.rSpeed = 0;
        this.img = new Image();
        this.img.src = "../../static/Games/Motorcycle/Images/tenor.gif";


        this.draw = function () {
            var p1 = c.height - noise(t + this.x) * 0.25;
            var p2 = c.height - noise(t + 5 + this.x) * 0.25;
            var grounder = 0;
            if (p1 - 15 > this.y) {
        this.ySpeed += 0.1;
            } else {
        this.ySpeed -= this.y - (p1 - 15);
                this.y = p1 - 15;
                grounder = 1;

            }
            if (grounder && Math.abs(this.rot) > Math.PI * 0.5) {
        stop();
                console.log(this.rot);
                //this.rSpeed = 5;
                //k.ArrowRight = 1;
                //k.d = 1;
                //this.x -= speed * 5;
            }
            var angle = Math.atan2((p2 - 15) - this.y, (this.x + 5) - this.x);
            this.y += this.ySpeed;
            if (grounder && playing) {
        this.rot -= (this.rot - angle) * 0.5;
                this.rSpeed = this.rSpeed - (angle - this.rot);
            }
            this.rSpeed += (k.ArrowDown - k.ArrowUp) * 0.05;
            this.rSpeed += (k.a - k.d) * 0.05;
            this.rot -= this.rSpeed * 0.01;
            if (this.rot > Math.PI) {
        this.rot = -Math.PI;
            }
            if (this.rot < -Math.PI) this.rot = Math.PI;
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(this.rot);
            ctx.drawImage(this.img, -15, -15, 30, 30);
            ctx.restore();
        }
    }

    function loop() {
        //ctx.fillStyle = "#19f";
        //ctx.fillRect(0, 0, c.width, c.height);
        ctx.drawImage(ground, 0, 0, c.width, c.height + 100);
        if (playing) {
        score++;
            speed -= (speed - (k.ArrowRight - k.ArrowLeft)) * 0.01;
            speed -= (speed - (k.d - k.a)) * 0.01;
            t += 10 * speed;
            ctx.fillStyle = "black";
            ctx.beginPath();
            ctx.moveTo(0, c.height);

            for (let i = 0; i < c.width;i++) {
                ctx.lineTo(i, c.height - noise(t + i) * 0.25);
            }
            ctx.lineTo(c.width, c.height);
            ctx.fill();
            player.draw();
            requestAnimationFrame(loop);
        }
    }
    onkeydown = d => k[d.key] = 1;
    onkeyup = d => k[d.key] = 0;