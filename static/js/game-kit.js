/*
 * O'yinlar uchun umumiy panel: joriy hisob, shaxsiy rekord (brauzerda saqlanadi),
 * "Yangi rekord!" xabari va natijani ulashish (Telegram va boshqalar).
 *
 *   CPGame.init({ id: "snake", title: "Snake", mount: element })  // panel mount'dan keyin
 *   CPGame.init({ id: "car", title: "Car", before: element })     // yoki element'dan oldin
 *   CPGame.score(n)   — joriy hisobni ko'rsatish
 *   CPGame.over(n)    — o'yin tugadi: rekord bo'lsa saqlanadi
 *   CPGame.swipe(el, fn) — telefonda barmoq surish: fn("left"|"right"|"up"|"down")
 */
(function () {
  var T = {
    uz: { score: "Hisob", best: "Rekord", record: "🎉 Yangi rekord!", share: "Ulashish",
          msg: "{game} o'yinida {score} ball to'pladim! Rekordimni yangilab ko'r 👇" },
    ru: { score: "Счёт", best: "Рекорд", record: "🎉 Новый рекорд!", share: "Поделиться",
          msg: "Я набрал {score} очков в {game}! Попробуй побить мой рекорд 👇" },
    en: { score: "Score", best: "Best", record: "🎉 New record!", share: "Share",
          msg: "I scored {score} in {game}! Try to beat my record 👇" },
  };
  var lang = (document.documentElement.lang || "uz").slice(0, 2);
  var t = T[lang] || T.uz;

  var state = { id: "", title: "", best: 0, last: 0, els: {} };

  function load(key) {
    try { return parseInt(localStorage.getItem(key), 10) || 0; } catch (e) { return 0; }
  }
  function save(key, value) {
    try { localStorage.setItem(key, String(value)); } catch (e) {}
  }
  function key() { return "cpGameBest:" + state.id; }

  function render() {
    state.els.score.textContent = state.last;
    state.els.best.textContent = state.best;
    state.els.share.hidden = state.best <= 0;
  }

  function init(opts) {
    state.id = opts.id;
    state.title = opts.title || opts.id;
    state.best = load(key());

    var box = document.createElement("div");
    box.className = "cp-game-bar";
    box.innerHTML =
      '<span>' + t.score + ': <b data-k="score">0</b></span>' +
      '<span>🏆 ' + t.best + ': <b data-k="best">0</b></span>' +
      '<span class="cp-game-flash" data-k="flash" hidden>' + t.record + '</span>' +
      '<button type="button" data-k="share">📤 ' + t.share + '</button>';
    ["score", "best", "flash", "share"].forEach(function (k) {
      state.els[k] = box.querySelector('[data-k="' + k + '"]');
    });
    state.els.share.addEventListener("click", share);

    var style = document.createElement("style");
    style.textContent =
      ".cp-game-bar{display:flex;flex-wrap:wrap;align-items:center;gap:8px 16px;margin:10px 0;padding:10px 14px;" +
      "border-radius:12px;background:rgba(79,70,229,.08);border:1px solid rgba(79,70,229,.25);font-size:1rem}" +
      ".cp-game-bar b{font-size:1.15rem}.cp-game-flash{color:#16a34a;font-weight:700}" +
      ".cp-game-bar button{margin-left:auto;border:0;border-radius:10px;padding:6px 12px;background:#4f46e5;color:#fff;font-weight:600}";
    document.head.appendChild(style);

    var mount = opts.mount || document.querySelector("h1");
    if (opts.before && opts.before.parentNode) {
      opts.before.parentNode.insertBefore(box, opts.before);
    } else if (mount && mount.parentNode) {
      mount.parentNode.insertBefore(box, mount.nextSibling);
    } else {
      document.body.insertBefore(box, document.body.firstChild);
    }
    render();
  }

  function score(n) {
    state.last = Math.max(0, n | 0);
    if (state.els.score) state.els.score.textContent = state.last;
  }

  function over(n) {
    score(n);
    if (state.last > state.best) {
      state.best = state.last;
      save(key(), state.best);
      if (state.els.flash) {
        state.els.flash.hidden = false;
        setTimeout(function () { state.els.flash.hidden = true; }, 4000);
      }
      if (window.gtag) window.gtag("event", "game_record", { game: state.id, score: state.best });
    }
    if (state.els.best) render();
  }

  function share() {
    var text = t.msg.replace("{game}", state.title).replace("{score}", state.best);
    var url = location.origin + location.pathname;
    if (navigator.share) {
      navigator.share({ title: state.title, text: text, url: url }).catch(function () {});
    } else {
      window.open("https://t.me/share/url?url=" + encodeURIComponent(url) + "&text=" + encodeURIComponent(text), "_blank", "noopener");
    }
    if (window.gtag) window.gtag("event", "share", { method: "game", content_id: state.id });
  }

  function swipe(el, fn) {
    var x0 = null, y0 = null;
    el.addEventListener("touchstart", function (e) {
      x0 = e.touches[0].clientX; y0 = e.touches[0].clientY;
    }, { passive: true });
    el.addEventListener("touchmove", function (e) {
      if (x0 !== null) e.preventDefault(); // surish paytida sahifa aylanib ketmasin
    }, { passive: false });
    el.addEventListener("touchend", function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
      x0 = y0 = null;
      if (Math.max(Math.abs(dx), Math.abs(dy)) < 20) return fn("tap");
      fn(Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? "right" : "left") : (dy > 0 ? "down" : "up"));
    });
  }

  window.CPGame = { init: init, score: score, over: over, swipe: swipe };
})();
