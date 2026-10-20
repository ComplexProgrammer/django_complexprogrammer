/*
 * Three.js (3D fon) faqat kerak bo'lganda yuklanadi.
 *
 * Telefon/planshetda, "harakatni kamaytirish" (prefers-reduced-motion) yoki trafik tejash
 * (Save-Data) yoqilganda 3D fon batareya va trafikni behuda sarflaydi, sahifani sekinlashtiradi.
 * Bunday holatda kutubxona umuman yuklanmaydi: o'rniga hech narsa qilmaydigan "soxta" THREE
 * qo'yiladi, shuning uchun sahifalardagi mavjud 3D kodi o'zgartirilmasdan xatosiz ishlaydi,
 * canvas esa yashiriladi.
 *
 * Ulash: <script src="/static/js/three-guard.js"></script>  (eski three.min.js tegi o'rniga)
 */
(function () {
  var SRC = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js";

  function media(q) {
    return !!(window.matchMedia && window.matchMedia(q).matches);
  }

  var conn = navigator.connection || {};
  var enabled =
    !media("(max-width: 991px)") &&
    !media("(pointer: coarse)") &&
    !media("(prefers-reduced-motion: reduce)") &&
    !conn.saveData;

  // Har qanday murojaatga o'zini qaytaradigan obyekt: new THREE.Scene(), scene.add(...),
  // mesh.rotation.x += 0.01 va h.k. hammasi jim bajariladi.
  function makeStub() {
    var proxy;
    var handler = {
      get: function (target, key) {
        if (key === Symbol.toPrimitive) return function () { return 0; };
        if (key === "length") return 0;
        if (key === "then") return undefined; // Promise deb o'ylanmasin
        if (key === "prototype") return target.prototype;
        return proxy;
      },
      set: function () { return true; },
      apply: function () { return proxy; },
      construct: function () { return proxy; },
    };
    proxy = new Proxy(function () {}, handler);
    return proxy;
  }

  window.CP3D = { enabled: enabled, makeStub: makeStub };

  if (enabled) {
    // Sinxron yuklash shart: sahifadagi 3D kodi shu tegdan keyin darhol THREE'ni ishlatadi
    document.write('<script src="' + SRC + '"><\/script>');
    // CDN ochilmasa (yoki brauzer document.write'ni bloklasa) sahifa baribir buzilmasin
    document.write("<script>window.THREE || (window.THREE = CP3D.makeStub());<\/script>");
  } else {
    window.THREE = makeStub();
    document.documentElement.classList.add("no-3d");
    var style = document.createElement("style");
    style.textContent =
      "html.no-3d #threejs-canvas, html.no-3d .threejs-canvas, html.no-3d #threejs-container{display:none!important}";
    document.head.appendChild(style);
  }
})();
