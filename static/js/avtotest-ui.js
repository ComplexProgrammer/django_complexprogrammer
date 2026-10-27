/* Mavzu tugmasi va rasm kattalashtirish — templates/projects/avtotest.html dan ko'chirilgan (brauzer keshlaydi). */
// Initialize theme on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeButton(savedTheme);
}); function toggleTheme() {
    const body = document.documentElement;
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';

    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);

    updateThemeButton(newTheme);

    // Tugma animatsiyasi
    const button = document.getElementById('themeButton');
    button.style.transform = 'scale(0.95)';
    setTimeout(() => {
        button.style.transform = '';
    }, 150);
}

function updateThemeButton(theme) {
    const button = document.getElementById('themeButton');
    const icon = theme === 'light' ? 'fa-moon' : 'fa-sun';
    const text = theme === 'light' ? 'Tun' : 'Kun';
    const title = theme === 'light' ? 'Tun rejimiga o\'tish' : 'Kun rejimiga o\'tish';

    button.innerHTML = `<i class="fas ${icon}"></i><span class="theme-toggle-text">${text}</span>`;
    button.title = title;
}

// 3D parallax effect for list items
document.addEventListener('DOMContentLoaded', () => {
    const listItems = document.querySelectorAll('.list-group-item:not(.disabledDiv)');

    listItems.forEach(item => {
        item.addEventListener('mousemove', (e) => {
            const rect = item.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;

            item.style.transform = `
                perspective(1000px)
                translateZ(40px)
                rotateX(${rotateX}deg)
                rotateY(${rotateY}deg)
                translateX(12px)
                scale(1.05)
            `;
        });

        item.addEventListener('mouseleave', () => {
            item.style.transform = 'translateZ(0) rotateX(0deg) rotateY(0deg)';
        });
    });

    // 3D parallax effect for ticket cards
    const ticketCards = document.querySelectorAll('.ticket-card-inner');

    ticketCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 8;
            const rotateY = (centerX - x) / 8;

            card.style.transform = `
                perspective(1000px)
                translateZ(60px)
                rotateX(${rotateX}deg)
                rotateY(${rotateY}deg)
                scale(1.08)
            `;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateZ(0) rotateX(0deg) rotateY(0deg)';
        });
    });

    // Image Modal functionality
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const closeBtn = document.querySelector('.image-modal-close');
    const zoomInBtn = document.getElementById('zoomIn');
    const zoomOutBtn = document.getElementById('zoomOut');
    const resetZoomBtn = document.getElementById('resetZoom');

    let currentZoom = 1;
    let isDragging = false;
    let startX, startY, translateX = 0, translateY = 0;

    // Open modal when clicking on test images
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('test-image')) {
            modal.style.display = 'block';
            modalImg.src = e.target.src;
            currentZoom = 1;
            translateX = 0;
            translateY = 0;
            updateImageTransform();
        }
    });

    // Close modal
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
        currentZoom = 1;
        translateX = 0;
        translateY = 0;
    });

    // Close on background click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
            currentZoom = 1;
            translateX = 0;
            translateY = 0;
        }
    });

    // Close on ESC key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.style.display === 'block') {
            modal.style.display = 'none';
            currentZoom = 1;
            translateX = 0;
            translateY = 0;
        }
    });

    // Zoom controls
    zoomInBtn.addEventListener('click', () => {
        currentZoom = Math.min(currentZoom + 0.25, 5);
        updateImageTransform();
    });

    zoomOutBtn.addEventListener('click', () => {
        currentZoom = Math.max(currentZoom - 0.25, 0.5);
        updateImageTransform();
    });

    resetZoomBtn.addEventListener('click', () => {
        currentZoom = 1;
        translateX = 0;
        translateY = 0;
        updateImageTransform();
    });

    // Drag functionality
    modalImg.addEventListener('mousedown', (e) => {
        if (currentZoom > 1) {
            isDragging = true;
            startX = e.clientX - translateX;
            startY = e.clientY - translateY;
            modalImg.style.cursor = 'grabbing';
        }
    });

    document.addEventListener('mousemove', (e) => {
        if (isDragging) {
            translateX = e.clientX - startX;
            translateY = e.clientY - startY;
            updateImageTransform();
        }
    });

    document.addEventListener('mouseup', () => {
        if (isDragging) {
            isDragging = false;
            modalImg.style.cursor = 'move';
        }
    });

    // Mouse wheel zoom
    modalImg.addEventListener('wheel', (e) => {
        e.preventDefault();
        if (e.deltaY < 0) {
            currentZoom = Math.min(currentZoom + 0.1, 5);
        } else {
            currentZoom = Math.max(currentZoom - 0.1, 0.5);
        }
        updateImageTransform();
    });

    function updateImageTransform() {
        modalImg.style.transform = `translate(${translateX}px, ${translateY}px) scale(${currentZoom})`;
    }
});
