/* Bilet yechish (AngularJS controller); bilet raqami window.CP_BILET da — templates/projects/avtotest.html dan ko'chirilgan (brauzer keshlaydi). */
var myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'), {
    keyboard: false
});
var app = angular.module("App", []);
app.controller("avtotest", ["$scope", "$http", "$filter", function ($scope, $http, $filter) {
    var timeH = document.getElementById("timer");
    $scope.isPaused = false;
    $scope.timeout = false;
    $scope.savol_raqami = 1;
    $scope.bilet = window.CP_BILET || 0;
$scope.time = 900;
$scope.togri_javob_soni = 0;
$scope.notogri_javob_soni = 0;
$scope.javoblar = [];
$scope.data = [];
//setCookie("javoblar", JSON.stringify($scope.javoblar), 365);
if ($scope.bilet != 0) {
    checkJavoblar();
    LoadData();
}
$scope.mValue = null;
$scope.back = function () {
    window.location.href = "/avtotest";
}
$scope.nextbilet = function (value) {
    if ($scope.bilet == value) {
        $scope.javoblar = $scope.javoblar.filter(word => word.bilet != $scope.bilet);
        saveJavoblar();
    }
    window.location.href = "/avtotest/" + value;
}
$scope.showModal = function () {
    $scope.isPaused = true;
    $scope.timeout = true;
    myModal.show();
}
$('#timer').on('click', function (e) {
    e.preventDefault();
    //$scope.isPaused = !$scope.isPaused;
});
$("#staticBackdrop").on('hide.bs.modal', function () {
    $scope.isPaused = false;
});
function startTimer(timeSecond) {
    displayTime(timeSecond);
    const countDown = setInterval(() => {
        if (!$scope.isPaused) {
            timeSecond--;
            $scope.time = timeSecond;
            displayTime(timeSecond);
            if (timeSecond == 0 || timeSecond < 1) {
                endCount();
                clearInterval(countDown);
            }
        }
    }, 1000);
}

function displayTime(second) {
    const min = Math.floor(second / 60);
    const sec = Math.floor(second % 60);
    timeH.innerHTML = `${min < 10 ? "0" : ""}${min}:${sec < 10 ? "0" : ""}${sec}`;
}

function endCount() {
    timeH.innerHTML = "Vaqt tugadi";
    myModal.show();
}
// Javoblar localStorage'da saqlanadi: cookie ~4 KB bilan cheklangani sababli
// 8-10 biletdan keyin progress yo'qolib qolardi.
function saveJavoblar() {
    try { localStorage.setItem("avtotestJavoblar", JSON.stringify($scope.javoblar)); } catch (e) {}
}
function loadJavoblar() {
    try {
        var raw = localStorage.getItem("avtotestJavoblar");
        if (raw) return JSON.parse(raw);
        // Eski cookie'dagi ma'lumotni bir marta ko'chiramiz
        var old = getCookie("javoblar");
        if (old) {
            var parsed = JSON.parse(old);
            localStorage.setItem("avtotestJavoblar", old);
            document.cookie = "javoblar=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/";
            return parsed;
        }
    } catch (e) {}
    return [];
}
// Yakunlangan biletlar natijasi va xato savollar — bilet qayta boshlansa ham saqlanib qoladi
function loadObj(key) {
    try { return JSON.parse(localStorage.getItem(key) || "{}"); } catch (e) { return {}; }
}
function saveObj(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) {}
    if (window.cpSync) window.cpSync.schedule();
}
function rememberAnswer(questionId, correct) {
    var mistakes = loadObj("avtotestMistakes");
    if (correct) delete mistakes[questionId];
    else mistakes[questionId] = { bilet: $scope.bilet, t: Date.now() };
    saveObj("avtotestMistakes", mistakes);
}
function saveResult() {
    var results = loadObj("avtotestResults");
    var mine = $scope.javoblar.filter(function (w) { return w.bilet == $scope.bilet; });
    var correct = mine.filter(function (w) {
        var q = $scope.data.find(function (d) { return d.id == w.id; });
        return q && q.javob === w.javob;
    }).length;
    var prev = results[$scope.bilet] || { attempts: 0 };
    results[$scope.bilet] = {
        correct: correct,
        wrong: mine.length - correct,
        attempts: (prev.attempts || 0) + 1,
        best: Math.max(prev.best || 0, correct),
        time: 900 - $scope.time,
        date: Date.now()
    };
    saveObj("avtotestResults", results);
    offerLogin();
}
// Mehmonga bilet natijasi oynasida: "natijani saqlash uchun Telegram orqali kiring"
function offerLogin() {
    if (window.CP_LOGGED_IN) return;
    var body = document.querySelector("#staticBackdrop .modal-body");
    if (!body || body.querySelector(".cp-save-cta")) return;
    var L = {
        uz: ["💾 Natijangizni saqlang", "Telegram orqali kiring — natijalar telefon va kompyuterda saqlanadi, haftalik reytingda qatnashasiz.", "Telegram orqali kirish"],
        ru: ["💾 Сохраните результат", "Войдите через Telegram — результаты сохранятся на телефоне и компьютере, и вы попадёте в недельный рейтинг.", "Войти через Telegram"],
        en: ["💾 Save your result", "Log in with Telegram — results sync between phone and computer, and you join the weekly leaderboard.", "Log in with Telegram"]
    }[(document.documentElement.lang || "uz").slice(0, 2)] || null;
    if (!L) return;
    var box = document.createElement("div");
    box.className = "cp-save-cta p-3 mt-2 rounded border border-primary";
    box.innerHTML = "<b></b><p class='mb-2 small'></p><a class='btn btn-primary btn-sm'></a>";
    box.querySelector("b").textContent = L[0];
    box.querySelector("p").textContent = L[1];
    var a = box.querySelector("a");
    a.textContent = "✈️ " + L[2];
    a.href = (window.CP_LANG_PREFIX || "") + "/profil/";
    body.appendChild(box);
    if (window.gtag) window.gtag("event", "login_offer", { place: "bilet_result" });
}
function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
function checkJavoblar() {
    $scope.javoblar = loadJavoblar();
    if ($scope.javoblar.filter(word => word.bilet == $scope.bilet).length == 10) {
        $scope.javoblar = $scope.javoblar.filter(word => word.bilet != $scope.bilet);
        saveJavoblar();
    }
    else {
        if ($scope.javoblar.filter(word => word.bilet == $scope.bilet).length != 0) {
                    // $scope.isPaused = true; $scope.timeout = true; myModal.show();
                }
    }
    $scope.javoblar.filter(word => word.bilet == $scope.bilet).forEach((element) => {
        if (element.time < $scope.time) {
            $scope.time = element.time;
        }
    });
    startTimer($scope.time);

}
$scope.b = function (value) {
    myFunction(value);
}
function myFunction(value) {
    $scope.savol_raqami = value;
    $scope.savol = $scope.data[value - 1];
    $scope.id = $scope.savol.id;
    $scope.mValue = $scope.savol.berilgan_javob + $scope.id;
    document.getElementById('click').play();
    var element = document.getElementsByClassName('page-item');
    for (var i = 0; i < element.length; i++) {
        element[i].classList.remove('active');
    }
    document.getElementById('savol' + value).classList.add('active');
}
function setJavob(javob) {
    var obj = {
        id: $scope.savol.id,
        bilet: $scope.bilet,
        time: $scope.time,
        javob: javob,
    };

    if ($scope.javoblar.find(element => element.id == obj.id)) {
        return; // bu savolga allaqachon javob berilgan
    }
    $scope.javoblar.push(obj);
    saveJavoblar();
    $scope.savol.berilgan_javob = javob;
    rememberAnswer($scope.savol.id, javob === $scope.savol.javob);
    if (window.cpSync) window.cpSync.answered(javob === $scope.savol.javob);

    $scope.mValue = javob + $scope.id;
    if (javob === $scope.savol.javob) {
        $scope.togri_javob_soni = $scope.togri_javob_soni + 1;
        document.getElementById('right').play();
        document.getElementById(javob + $scope.id).classList.add('list-group-item-success');
        document.getElementById('ab' + $scope.savol_raqami).classList.add('bg-success');
        alertify.success("To`g`ri javob");
    }
    else {
        $scope.notogri_javob_soni = $scope.notogri_javob_soni + 1;
        document.getElementById('wrong').play();
        document.getElementById(javob + $scope.id).classList.add('list-group-item-danger');
        document.getElementById('ab' + $scope.savol_raqami).classList.add('bg-danger');
        alertify.error("Noto`g`ri javob");
    }
    document.getElementById('A' + $scope.id).classList.add('disabledDiv');
    document.getElementById('B' + $scope.id).classList.add('disabledDiv');
    document.getElementById('C' + $scope.id).classList.add('disabledDiv');
    document.getElementById('D' + $scope.id).classList.add('disabledDiv');
    if ($scope.javoblar.filter(word => word.bilet == $scope.bilet).length == 10) {
        $scope.isPaused = true;
        $scope.timeout = false;
        saveResult();
        myModal.show();
    } else if (javob === $scope.savol.javob) {
        // To'g'ri javobdan keyin keyingi javobsiz savolga avtomatik o'tamiz
        setTimeout(function () { $scope.$apply(goNextUnanswered); }, 900);
    }
}
function goNextUnanswered() {
    for (var step = 1; step <= $scope.data.length; step++) {
        var n = (($scope.savol_raqami - 1 + step) % $scope.data.length) + 1;
        if (!$scope.data[n - 1].berilgan_javob) { myFunction(n); return; }
    }
}
// Klaviatura: 1-4 yoki A-D — javob, ←/→ — oldingi/keyingi savol
document.addEventListener("keydown", function (e) {
    if (!$scope.data.length || e.ctrlKey || e.metaKey || e.altKey) return;
    var tag = (e.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea" || tag === "select") return;
    var key = e.key.toUpperCase();
    var map = { "1": "A", "2": "B", "3": "C", "4": "D", "A": "A", "B": "B", "C": "C", "D": "D" };
    if (map[key]) {
        var letter = map[key];
        var field = "javob_" + letter.toLowerCase();
        if ($scope.savol && $scope.savol[field] && !$scope.savol.berilgan_javob) {
            e.preventDefault();
            $scope.$apply(function () { $scope.ok(letter); });
        }
    } else if (e.key === "ArrowRight" && $scope.savol_raqami < $scope.data.length) {
        $scope.$apply(function () { myFunction($scope.savol_raqami + 1); });
    } else if (e.key === "ArrowLeft" && $scope.savol_raqami > 1) {
        $scope.$apply(function () { myFunction($scope.savol_raqami - 1); });
    }
});
$scope.ok = function (javob) {
    setJavob(javob);
    //setTimeout(myFunction, 3000, $scope.savol_raqami+1);
}

function LoadData() {
    document.getElementById('conn').style.visibility = "visible";
    $('#hh').modal({
        backdrop: 'static',
        keyboard: false
    })
    $http({
        method: 'GET',
        url: "/GetSavol?bilet=" + $scope.bilet,
        dataType: "json"
    }).then(function (d) {
        d.data.forEach((item) => {
            berilgan_javob = '';
            if ($scope.javoblar.find(element => element.id == item.id)) {
                berilgan_javob = $scope.javoblar.find(element => element.id == item.id).javob;
            }
            var obj = {
                id: item.id,
                bilet: item.bilet,
                javob: item.javob,
                javob_a: item.javob_a,
                javob_a_en: item.javob_a_en,
                javob_a_ru: item.javob_a_ru,
                javob_b: item.javob_b,
                javob_b_en: item.javob_b_en,
                javob_b_ru: item.javob_b_ru,
                javob_c: item.javob_c,
                javob_c_en: item.javob_c_en,
                javob_c_ru: item.javob_c_ru,
                javob_d: item.javob_d,
                javob_d_en: item.javob_d_en,
                javob_d_ru: item.javob_d_ru,
                raqam: item.raqam,
                rasm: item.rasm,
                savol: item.savol,
                savol_en: item.savol_en,
                savol_ru: item.savol_ru,
                berilgan_javob: berilgan_javob,
            };
            $scope.data.push(obj);
        });
        let raqam = 0;
        $scope.data = $scope.data.sort(function (a, b) { return a.raqam - b.raqam });
        $scope.data.forEach((element) => {
            if (element.raqam > raqam && raqam == element.raqam - 1 && element.berilgan_javob != '') {
                raqam = element.raqam;
            }
            if (element.berilgan_javob) {
                if (element.javob == element.berilgan_javob) {
                    $scope.togri_javob_soni = $scope.togri_javob_soni + 1;
                    document.getElementById('ab' + element.raqam).classList.add('bg-success');
                }
                else {
                    $scope.notogri_javob_soni = $scope.notogri_javob_soni + 1;
                    document.getElementById('ab' + element.raqam).classList.add('bg-danger');
                }
            }
        });
        $scope.savol = $scope.data[raqam];
        $scope.id = $scope.savol.id;
        $scope.savol_raqami = raqam + 1;
        document.getElementById('savol' + $scope.savol_raqami).classList.add('active');

        $("#hh").modal('hide');
        document.getElementById('conn').style.visibility = "hidden";
    }, function (error) {
        $("#hh").modal('hide');
        document.getElementById('conn').style.visibility = "hidden";
        console.log("error in GetSavol -> ", error);
        alertify.error("Xatolik yuz berdi");
    });
}
  }]);
