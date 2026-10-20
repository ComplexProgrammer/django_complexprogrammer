/*
 * /tests/?topic_id=N — bilet (mavzu) savollarini yechish sahifasi. Oldin AngularJS'da edi.
 *
 * Ma'lumot: /tests/GetQuestions/?topic_id=N&with_answers=1 (savollar javoblari bilan, bitta so'rovda)
 *           /tests/GetTopics/?book_id=M (keyingi biletga o'tish uchun)
 * Natijalar brauzerda (localStorage): testsAnswers — berilgan javoblar, testsResults — bilet natijalari,
 * testsMistakes — xato qilingan savollar (/tests/xatolar/ sahifasi uchun).
 */
(function () {
  var cfgEl = document.getElementById("ts-topic");
  if (!cfgEl) return;
  var topic = JSON.parse(cfgEl.textContent);
  var lang = (document.documentElement.lang || "uz").slice(0, 2);
  var NAME = lang === "ru" ? "name_ru_ru" : lang === "en" ? "name_en_us" : "name_uz_uz";
  var EXPL = lang === "ru" ? "explanation_ru_ru" : lang === "en" ? "explanation_en_us" : "explanation_uz_uz";

  var TEXTS = {
    uz: { question: "{n}-savol", result: "{t} natijasi", unmarked: "Belgilanmagan savollar: {n} ta",
          right: "To'g'ri javob: {n} ta", wrong: "Noto'g'ri javob: {n} ta", ok: "To'g'ri javob", bad: "Noto'g'ri javob",
          timeout: "Vaqt tugadi", error: "Xatolik yuz berdi. Internetni tekshirib, sahifani yangilang.",
          kbd: "Klaviatura: 1–{n} — javob, ←/→ — savollar", zoom: "Rasmni kattalashtirish uchun bosing" },
    ru: { question: "Вопрос {n}", result: "Результат: {t}", unmarked: "Неотмеченные вопросы: {n}",
          right: "Правильных ответов: {n}", wrong: "Неправильных ответов: {n}", ok: "Правильный ответ", bad: "Неправильный ответ",
          timeout: "Время вышло", error: "Произошла ошибка. Проверьте интернет и обновите страницу.",
          kbd: "Клавиатура: 1–{n} — ответ, ←/→ — вопросы", zoom: "Нажмите, чтобы увеличить изображение" },
    en: { question: "Question {n}", result: "{t} result", unmarked: "Unmarked questions: {n}",
          right: "Correct answers: {n}", wrong: "Incorrect answers: {n}", ok: "Correct answer", bad: "Incorrect answer",
          timeout: "Time is up", error: "Something went wrong. Check your connection and reload the page.",
          kbd: "Keyboard: 1–{n} to answer, ←/→ to navigate", zoom: "Click to enlarge image" },
  };
  var T = TEXTS[lang] || TEXTS.uz;
  function t(key, vars) {
    var s = T[key] || "";
    Object.keys(vars || {}).forEach(function (k) { s = s.replace("{" + k + "}", vars[k]); });
    return s;
  }

  var $ = function (id) { return document.getElementById(id); };
  var els = {
    timer: $("timer"), pages: $("tsPages"), title: $("tsQTitle"), image: $("tsQImage"), answers: $("tsAnswers"),
    expl: $("tsExpl"), kbd: $("tsKbd"), loader: $("conn"), close: $("tsClose"),
    unmarked: $("tsUnmarked"), right: $("tsRight"), wrong: $("tsWrong"), cont: $("tsContinue"), nextTopic: $("tsNextTopic"),
  };
  var modalEl = $("staticBackdrop");
  var modal = window.bootstrap ? new bootstrap.Modal(modalEl, { keyboard: false }) : null;

  var state = {
    questions: [], current: null, topics: [], time: 3600, paused: false, finished: false,
    answers: loadAnswers(),
  };

  // --- localStorage ---
  function loadObj(key, def) {
    try { return JSON.parse(localStorage.getItem(key)) || def; } catch (e) { return def; }
  }
  function saveObj(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) {}
  }
  function loadAnswers() {
    try {
      if (localStorage.getItem("testsAnswers")) return loadObj("testsAnswers", []);
      // Eski versiya javoblarni cookie'da saqlardi — bir marta ko'chiramiz
      var m = document.cookie.match(/(?:^|;\s*)selected_answers=([^;]*)/);
      if (m && m[1]) {
        var parsed = JSON.parse(decodeURIComponent(m[1]));
        saveObj("testsAnswers", parsed);
        document.cookie = "selected_answers=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/";
        return parsed;
      }
    } catch (e) {}
    return [];
  }
  function saveAnswers() { saveObj("testsAnswers", state.answers); }
  function mine() { return state.answers.filter(function (a) { return a.topic_id == topic.id; }); }
  function answerFor(q) {
    for (var i = 0; i < state.answers.length; i++) if (state.answers[i].question_id == q.id) return state.answers[i];
    return null;
  }
  function rememberMistake(q, right) {
    var mistakes = loadObj("testsMistakes", {});
    if (right) delete mistakes[q.id];
    else mistakes[q.id] = { topic_id: topic.id, book_id: topic.book_id, t: Date.now() };
    saveObj("testsMistakes", mistakes);
  }
  function saveResult() {
    var results = loadObj("testsResults", {});
    var list = mine();
    var correct = list.filter(function (a) { return a.right; }).length;
    var prev = results[topic.id] || {};
    results[topic.id] = {
      correct: correct, wrong: list.length - correct, total: state.questions.length,
      attempts: (prev.attempts || 0) + 1, best: Math.max(prev.best || 0, correct),
      book_id: topic.book_id, date: Date.now(),
    };
    saveObj("testsResults", results);
  }

  // --- yordamchilar ---
  function play(id) {
    var a = $(id);
    if (a && a.play) { try { var p = a.play(); if (p && p.catch) p.catch(function () {}); } catch (e) {} }
  }
  function notify(ok, text) {
    if (window.alertify) (ok ? alertify.success : alertify.error)(text);
  }
  function loading(on) { if (els.loader) els.loader.style.visibility = on ? "visible" : "hidden"; }
  function getJSON(url) {
    return fetch(url, { credentials: "same-origin" }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    });
  }

  // --- vaqt ---
  function showTime(sec) {
    var m = Math.floor(sec / 60), s = Math.floor(sec % 60);
    els.timer.textContent = (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
  }
  function startTimer() {
    showTime(state.time);
    var timer = setInterval(function () {
      if (state.paused || state.finished) return;
      state.time--;
      showTime(state.time);
      if (state.time < 1) {
        clearInterval(timer);
        els.timer.textContent = t("timeout");
        finish();
      }
    }, 1000);
  }

  // --- natija oynasi ---
  function counts() {
    var list = mine(), right = list.filter(function (a) { return a.right; }).length;
    return { right: right, wrong: list.length - right, unmarked: state.questions.length - list.length };
  }
  function showModal(canContinue) {
    var c = counts();
    els.unmarked.textContent = t("unmarked", { n: c.unmarked });
    els.unmarked.hidden = c.unmarked === 0;
    els.right.textContent = t("right", { n: c.right });
    els.right.hidden = c.right === 0;
    els.wrong.textContent = t("wrong", { n: c.wrong });
    els.wrong.hidden = c.wrong === 0;
    els.close.hidden = els.cont.hidden = !canContinue;
    els.nextTopic.hidden = !nextTopic();
    state.paused = true;
    if (modal) modal.show();
  }
  function finish() {
    state.finished = true;
    showModal(false);
  }
  function nextTopic() {
    for (var i = 0; i < state.topics.length; i++) if (state.topics[i].number == topic.number + 1) return state.topics[i];
    return null;
  }
  function restartTopic(target) {
    state.answers = state.answers.filter(function (a) { return a.topic_id != target.id; });
    saveAnswers();
    location.href = "/tests?topic_id=" + target.id;
  }

  // --- savollar ---
  function renderPages() {
    els.pages.innerHTML = "";
    state.questions.forEach(function (q) {
      var li = document.createElement("li");
      var a = answerFor(q);
      li.className = "page-item" + (q === state.current ? " active" : "");
      var link = document.createElement("a");
      link.className = "page-link" + (a ? (a.right ? " bg-success text-white" : " bg-danger text-white") : "");
      link.href = "#";
      link.textContent = q.number;
      link.addEventListener("click", function (e) { e.preventDefault(); show(q); });
      li.appendChild(link);
      els.pages.appendChild(li);
    });
    var active = els.pages.querySelector(".active");
    if (active && active.scrollIntoView && els.pages.scrollHeight > els.pages.clientHeight) {
      els.pages.scrollTop = active.offsetTop - els.pages.offsetTop - 40;
    }
  }
  function visibleAnswers(q) {
    return (q.answers || []).filter(function (a) { return a[NAME]; });
  }
  function show(q, silent) {
    state.current = q;
    var chosen = answerFor(q);
    els.title.textContent = "";
    els.title.appendChild(document.createTextNode(t("question", { n: q.number })));
    els.title.appendChild(document.createElement("br"));
    els.title.appendChild(document.createTextNode(q[NAME] || q.name_uz_uz || ""));
    if (q.image) {
      els.image.src = "/media/" + q.image;
      els.image.title = t("zoom");
      els.image.hidden = false;
    } else {
      els.image.hidden = true;
      els.image.removeAttribute("src");
    }
    els.answers.innerHTML = "";
    var list = visibleAnswers(q);
    list.forEach(function (ans) {
      var item = document.createElement("a");
      item.href = "#";
      item.className = "list-group-item list-group-item-action";
      item.id = "answer" + ans.id;
      var radio = document.createElement("input");
      radio.type = "radio";
      radio.name = "answer" + q.id;
      radio.tabIndex = -1;
      radio.checked = !!chosen && chosen.id == ans.id;
      item.appendChild(radio);
      item.appendChild(document.createTextNode(" " + ans[NAME]));
      if (chosen) {
        item.classList.add("disabledDiv");
        if (ans.right) item.classList.add("list-group-item-success");
        else if (chosen.id == ans.id) item.classList.add("list-group-item-danger");
      }
      item.addEventListener("click", function (e) { e.preventDefault(); choose(ans); });
      els.answers.appendChild(item);
    });
    var expl = q[EXPL] || "";
    els.expl.textContent = expl ? "💡 " + expl : "";
    els.expl.hidden = !(chosen && expl);
    els.kbd.textContent = list.length ? t("kbd", { n: list.length }) : "";
    renderPages();
    if (!silent) play("click");
  }
  function choose(ans) {
    var q = state.current;
    if (!q || answerFor(q) || state.finished) return;
    state.answers.push({ topic_id: topic.id, question_id: q.id, id: ans.id, right: !!ans.right, time: state.time });
    saveAnswers();
    rememberMistake(q, ans.right);
    play(ans.right ? "right" : "wrong");
    notify(ans.right, ans.right ? t("ok") : t("bad"));
    show(q, true);
    if (mine().length >= state.questions.length) {
      saveResult();
      finish();
    } else if (ans.right) {
      // To'g'ri javobdan keyin keyingi javobsiz savolga avtomatik o'tamiz
      setTimeout(function () { if (state.current === q) goNextUnanswered(); }, 900);
    }
  }
  function goNextUnanswered() {
    var n = state.questions.length, start = state.questions.indexOf(state.current);
    for (var step = 1; step <= n; step++) {
      var q = state.questions[(start + step) % n];
      if (!answerFor(q)) return show(q);
    }
  }
  function move(delta) {
    var i = state.questions.indexOf(state.current) + delta;
    if (i >= 0 && i < state.questions.length) show(state.questions[i]);
  }

  // --- hodisalar ---
  $("tsPrev").addEventListener("click", function (e) { e.preventDefault(); move(-1); });
  $("tsNext").addEventListener("click", function (e) { e.preventDefault(); move(1); });
  $("tsStop").addEventListener("click", function (e) { e.preventDefault(); if (!state.finished) showModal(true); });
  els.nextTopic.addEventListener("click", function () { var n = nextTopic(); if (n) restartTopic(n); });
  $("tsRestart").addEventListener("click", function () { restartTopic(topic); });
  $("tsBack").addEventListener("click", function () { location.href = "/tests?book_id=" + topic.book_id; });
  els.image.addEventListener("click", function () {
    if (window.openImageModal && els.image.src) window.openImageModal(els.image.src);
  });
  modalEl.addEventListener("hide.bs.modal", function () { if (!state.finished) state.paused = false; });
  document.addEventListener("keydown", function (e) {
    var q = state.current;
    if (!q || e.ctrlKey || e.metaKey || e.altKey) return;
    var tag = (e.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea" || tag === "select" || e.target.isContentEditable) return;
    if (document.querySelector(".modal.show")) return;
    if (/^[1-9]$/.test(e.key)) {
      var a = visibleAnswers(q)[parseInt(e.key, 10) - 1];
      if (a && !answerFor(q)) { e.preventDefault(); choose(a); }
    } else if (e.key === "ArrowRight") {
      move(1);
    } else if (e.key === "ArrowLeft") {
      move(-1);
    }
  });

  // --- yuklash ---
  mine().forEach(function (a) { if (a.time < state.time) state.time = a.time; });
  loading(true);
  getJSON("/tests/GetTopics/?book_id=" + encodeURIComponent(topic.book_id))
    .then(function (data) { state.topics = data; })
    .catch(function () {});
  getJSON("/tests/GetQuestions/?topic_id=" + encodeURIComponent(topic.id) + "&with_answers=1")
    .then(function (data) {
      loading(false);
      state.questions = data.sort(function (a, b) { return a.number - b.number; });
      if (!state.questions.length) return;
      // Birinchi javob berilmagan savoldan davom etamiz
      var first = state.questions.filter(function (q) { return !answerFor(q); })[0];
      show(first || state.questions[0], true);
      if (!first) finish();
      else startTimer();
    })
    .catch(function (err) {
      loading(false);
      if (window.console) console.error("GetQuestions", err);
      notify(false, t("error"));
    });
})();
