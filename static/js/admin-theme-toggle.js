(function () {
	function onReady(fn) {
		if (document.readyState === 'loading') {
			document.addEventListener('DOMContentLoaded', fn);
		} else {
			fn();
		}
	}

	function applyTheme(theme) {
		var body = document.body;
		if (!body) return;
		body.classList.remove('admin-dark', 'admin-light');
		if (theme === 'dark') body.classList.add('admin-dark');
		else body.classList.add('admin-light');
	}

	function getTheme() {
		try { return localStorage.getItem('adminTheme') || 'light'; }
		catch (e) { return 'light'; }
	}

	function setTheme(theme) {
		try { localStorage.setItem('adminTheme', theme); } catch (e) {}
		applyTheme(theme);
	}

	function buildButton() {
		var btn = document.createElement('button');
		btn.type = 'button';
		btn.className = 'btn btn-sm btn-outline-secondary ms-2 admin-theme-toggle';
		btn.style.display = 'inline-flex';
		btn.style.alignItems = 'center';
		btn.style.gap = '6px';
		btn.setAttribute('data-bs-toggle', 'tooltip');
		btn.setAttribute('title', 'Kun/Tun rejimi');
		function updateLabel() {
			var theme = getTheme();
			btn.textContent = theme === 'dark' ? '☀️ Light' : '🌙 Dark';
			btn.setAttribute('aria-label', 'Toggle theme');
		}
		btn.addEventListener('click', function () {
			var next = getTheme() === 'dark' ? 'light' : 'dark';
			setTheme(next);
			updateLabel();
		});
		updateLabel();
		return btn;
	}

	function createToggle() {
		var nav = document.querySelector('.main-header .navbar, nav.navbar, header .navbar');
		var btn = buildButton();
		if (nav) {
			var right = nav.querySelector('.navbar-nav.ms-auto, .navbar-nav.ml-auto, .navbar-nav.me-auto + .navbar-nav, .navbar-nav:last-child');
			if (right) {
				var wrapper = document.createElement('div');
				wrapper.className = 'ms-2';
				wrapper.appendChild(btn);
				right.appendChild(wrapper);
			} else {
				nav.appendChild(btn);
			}
		}

		// Always add a floating action button as well (to ensure visibility)
		var fab = buildButton();
		fab.classList.remove('btn-outline-secondary');
		fab.classList.add('admin-theme-fab');
		document.body.appendChild(fab);
	}

	function autoThemeIfUnset() {
		var stored;
		try { stored = localStorage.getItem('adminTheme'); } catch (e) { stored = null; }
		if (!stored) {
			var prefersDark = false;
			try { prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches; } catch (e) {}
			setTheme(prefersDark ? 'dark' : 'light');
		}
	}

	function initTooltips() {
		try {
			if (window.bootstrap && bootstrap.Tooltip) {
				var triggers = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
				triggers.forEach(function (el) { new bootstrap.Tooltip(el); });
			}
		} catch (e) {}
	}

	// Apply immediately
	autoThemeIfUnset();
	applyTheme(getTheme());
	onReady(function () {
		autoThemeIfUnset();
		applyTheme(getTheme());
		createToggle();
		initTooltips();
	});
})();


