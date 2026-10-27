/*
 * Markaziy bank kurslarini brauzerning o'zidan olish.
 *
 * Sayt serveri Germaniyada joylashgan va cbu.uz unga javob bermaydi (ulanish timeout bilan tugaydi),
 * shuning uchun serverdagi kurs eskirib qolishi mumkin. O'zbekistondagi foydalanuvchining brauzeri esa cbu.uz ni
 * ochadi va u CORS'ga ruxsat beradi (Access-Control-Allow-Origin: *). Sahifa avval server ma'lumotini ko'rsatadi,
 * keyin shu funksiya yangiroq kurs topsa — sahifa uni joyida yangilaydi.
 *
 * cpCbuLatest("24.10.2026") -> Promise: serverdagidan yangiroq sanali ro'yxat yoki null.
 */
(function () {
  var URL = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/";
  var TTL = 30 * 60 * 1000;  // sahifalar orasida qayta so'ramaslik uchun

  // "27.10.2026" -> "20261027" (sanalarni satr sifatida solishtirish uchun)
  function dateKey(d) {
    var p = String(d || "").split(".");
    return p.length === 3 ? p[2] + p[1] + p[0] : "";
  }

  function newer(list, serverDate) {
    return Array.isArray(list) && list.length && dateKey(list[0].Date) > dateKey(serverDate) ? list : null;
  }

  window.cpCbuLatest = function (serverDate) {
    try {
      var saved = JSON.parse(sessionStorage.getItem("cpCbuRates") || "null");
      if (saved && Date.now() - saved.t < TTL) return Promise.resolve(newer(saved.list, serverDate));
    } catch (e) {}
    if (!window.fetch) return Promise.resolve(null);
    var ctrl = window.AbortController ? new AbortController() : null;
    if (ctrl) setTimeout(function () { ctrl.abort(); }, 6000);  // xorijdan ochilmasa uzoq kutmaymiz
    return fetch(URL, ctrl ? { signal: ctrl.signal } : {})
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (list) {
        if (!Array.isArray(list)) return null;
        try { sessionStorage.setItem("cpCbuRates", JSON.stringify({ t: Date.now(), list: list })); } catch (e) {}
        return newer(list, serverDate);
      })
      .catch(function () { return null; });
  };
})();
