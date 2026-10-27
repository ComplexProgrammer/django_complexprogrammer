/* Three.js 3D fon — templates/projects/avtotest.html dan ko'chirilgan (brauzer keshlaydi). */
// Three.js Scene Setup for Avto Test - Road/Driving Theme
let scene, camera, renderer, particles, cars = [], roadLines = [], trafficLights = [];
let mouseX = 0, mouseY = 0;

function initThreeJS() {
    const canvas = document.getElementById('threejs-canvas');
    if (!canvas) return;

    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 50;
    camera.position.y = 5;

    renderer = new THREE.WebGLRenderer({
        canvas,
        alpha: true,
        antialias: true
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);

    // Create road-themed particles (asphalt texture effect)
    createRoadParticles();

    // Create 3D cars
    createCars();

    // Create road lines
    createRoadLines();

    // Create traffic lights
    createTrafficLights();

    // Add lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffa500, 0.8);
    directionalLight.position.set(10, 20, 10);
    scene.add(directionalLight);

    const pointLight1 = new THREE.PointLight(0xff0000, 2, 50);
    pointLight1.position.set(-20, 10, 0);
    scene.add(pointLight1);

    const pointLight2 = new THREE.PointLight(0x00ff00, 2, 50);
    pointLight2.position.set(20, 10, 0);
    scene.add(pointLight2);

    // Mouse movement listener
    document.addEventListener('mousemove', (event) => {
        mouseX = (event.clientX / window.innerWidth) * 2 - 1;
        mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
    });

    // Window resize handler
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    animate();
}

function createRoadParticles() {
    const geometry = new THREE.BufferGeometry();
    const vertices = [];
    const colors = [];

    for (let i = 0; i < 1500; i++) {
        vertices.push(
            Math.random() * 200 - 100,
            Math.random() * 100 - 50,
            Math.random() * 200 - 100
        );

        // Road colors: dark gray, yellow, white
        const colorOptions = [
            new THREE.Color(0x2c2c2c), // Dark asphalt
            new THREE.Color(0xffd700), // Yellow lines
            new THREE.Color(0xffffff), // White lines
            new THREE.Color(0x444444)  // Gray
        ];
        const color = colorOptions[Math.floor(Math.random() * colorOptions.length)];
        colors.push(color.r, color.g, color.b);
    }

    geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
        size: 0.6,
        vertexColors: true,
        transparent: true,
        opacity: 0.6,
        blending: THREE.AdditiveBlending
    });

    particles = new THREE.Points(geometry, material);
    scene.add(particles);
}

function createCars() {
    // Create simple 3D car shapes
    const carConfigs = [
        { color: 0xff0000, position: { x: -25, y: 0, z: -20 }, speed: 0.02 },
        { color: 0x0000ff, position: { x: 25, y: 0, z: -15 }, speed: 0.015 },
        { color: 0x00ff00, position: { x: -20, y: 0, z: -25 }, speed: 0.018 },
        { color: 0xffff00, position: { x: 15, y: 0, z: -10 }, speed: 0.022 }
    ];

    carConfigs.forEach((config) => {
        const carGroup = new THREE.Group();

        // Car body
        const bodyGeometry = new THREE.BoxGeometry(2, 1, 3);
        const bodyMaterial = new THREE.MeshPhongMaterial({
            color: config.color,
            transparent: true,
            opacity: 0.4,
            shininess: 100
        });
        const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
        carGroup.add(body);

        // Car top (cabin)
        const topGeometry = new THREE.BoxGeometry(1.5, 0.8, 2);
        const topMaterial = new THREE.MeshPhongMaterial({
            color: config.color,
            transparent: true,
            opacity: 0.3,
            shininess: 80
        });
        const top = new THREE.Mesh(topGeometry, topMaterial);
        top.position.y = 0.9;
        carGroup.add(top);

        // Wheels (simple circles)
        const wheelGeometry = new THREE.CylinderGeometry(0.3, 0.3, 0.2, 16);
        const wheelMaterial = new THREE.MeshPhongMaterial({ color: 0x111111 });

        const wheel1 = new THREE.Mesh(wheelGeometry, wheelMaterial);
        wheel1.position.set(-0.8, -0.5, 1);
        wheel1.rotation.z = Math.PI / 2;
        carGroup.add(wheel1);

        const wheel2 = new THREE.Mesh(wheelGeometry, wheelMaterial);
        wheel2.position.set(0.8, -0.5, 1);
        wheel2.rotation.z = Math.PI / 2;
        carGroup.add(wheel2);

        const wheel3 = new THREE.Mesh(wheelGeometry, wheelMaterial);
        wheel3.position.set(-0.8, -0.5, -1);
        wheel3.rotation.z = Math.PI / 2;
        carGroup.add(wheel3);

        const wheel4 = new THREE.Mesh(wheelGeometry, wheelMaterial);
        wheel4.position.set(0.8, -0.5, -1);
        wheel4.rotation.z = Math.PI / 2;
        carGroup.add(wheel4);

        carGroup.position.set(config.position.x, config.position.y, config.position.z);
        carGroup.userData = { speed: config.speed, initialZ: config.position.z };

        cars.push(carGroup);
        scene.add(carGroup);
    });
}

function createRoadLines() {
    // Create yellow road dividing lines
    for (let i = 0; i < 10; i++) {
        const lineGeometry = new THREE.BoxGeometry(0.3, 0.1, 3);
        const lineMaterial = new THREE.MeshBasicMaterial({
            color: 0xffd700,
            transparent: true,
            opacity: 0.5
        });
        const line = new THREE.Mesh(lineGeometry, lineMaterial);

        line.position.set(0, -2, -30 + i * 8);
        line.userData = { speed: 0.1 };

        roadLines.push(line);
        scene.add(line);
    }
}

function createTrafficLights() {
    // Create traffic light poles
    const lightConfigs = [
        { position: { x: -30, y: 5, z: -20 }, color: 0xff0000 },
        { position: { x: 30, y: 5, z: -15 }, color: 0xffff00 },
        { position: { x: -25, y: 5, z: -30 }, color: 0x00ff00 }
    ];

    lightConfigs.forEach((config) => {
        const lightGeometry = new THREE.SphereGeometry(0.8, 16, 16);
        const lightMaterial = new THREE.MeshPhongMaterial({
            color: config.color,
            emissive: config.color,
            emissiveIntensity: 0.5,
            transparent: true,
            opacity: 0.6
        });
        const light = new THREE.Mesh(lightGeometry, lightMaterial);

        light.position.set(config.position.x, config.position.y, config.position.z);
        light.userData = {
            pulseSpeed: Math.random() * 0.02 + 0.01,
            pulsePhase: Math.random() * Math.PI * 2
        };

        trafficLights.push(light);
        scene.add(light);
    });
}

function animate() {
    requestAnimationFrame(animate);

    const time = Date.now() * 0.001;

    // Rotate particles slowly
    if (particles) {
        particles.rotation.y += 0.0005;
    }

    // Animate cars moving along the road
    cars.forEach((car) => {
        car.position.z += car.userData.speed;
        car.rotation.y += 0.005;

        // Loop cars when they go off screen
        if (car.position.z > 50) {
            car.position.z = car.userData.initialZ;
        }
    });

    // Animate road lines moving
    roadLines.forEach((line) => {
        line.position.z += line.userData.speed;

        // Loop lines
        if (line.position.z > 50) {
            line.position.z = -50;
        }
    });

    // Animate traffic lights pulsing
    trafficLights.forEach((light) => {
        const pulse = Math.sin(time * light.userData.pulseSpeed + light.userData.pulsePhase) * 0.3 + 0.7;
        light.material.emissiveIntensity = pulse;
        light.scale.setScalar(0.8 + pulse * 0.2);
    });

    // Gentle camera movement based on mouse
    camera.position.x += (mouseX * 3 - camera.position.x) * 0.02;
    camera.position.y += (mouseY * 2 + 5 - camera.position.y) * 0.02;
    camera.lookAt(0, 0, 0);

    renderer.render(scene, camera);
}

// 3D fon — bezak: telefon, sekin internet va "kamroq animatsiya" sozlamasida yuklanmaydi (sahifa tezligi uchun)
window.addEventListener('load', function () {
    var c = navigator.connection || {};
    if (window.innerWidth < 1024 || c.saveData || /2g/.test(c.effectiveType || '') ||
        window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    (window.requestIdleCallback || function (cb) { setTimeout(cb, 1500); })(function () {
        var s = document.createElement('script');
        s.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
        s.async = true;
        s.onload = function () {
            initThreeJS();
            updateThreeJSTheme(document.documentElement.getAttribute('data-theme') || 'light');
        };
        document.head.appendChild(s);
    });
});

// Update Three.js theme based on dark/light mode
function updateThreeJSTheme(theme) {
    if (!particles || !cars.length) return;

    if (theme === 'dark') {
        particles.material.opacity = 0.5;
        cars.forEach(car => {
            car.children.forEach(child => {
                if (child.material && child.material.transparent) {
                    child.material.opacity *= 0.8;
                }
            });
        });
        trafficLights.forEach(light => {
            light.material.emissiveIntensity *= 1.2;
        });
    } else {
        particles.material.opacity = 0.6;
        cars.forEach(car => {
            car.children.forEach(child => {
                if (child.material && child.material.transparent) {
                    child.material.opacity = 0.4;
                }
            });
        });
    }
}

// Hook into existing theme toggle
const originalToggleTheme = window.toggleTheme;
if (originalToggleTheme) {
    window.toggleTheme = function () {
        originalToggleTheme();
        setTimeout(() => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            updateThreeJSTheme(currentTheme);
        }, 100);
    };
}
