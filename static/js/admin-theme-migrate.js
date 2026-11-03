/* Eski Jazzmin kun/tun tugmasi localStorage.adminTheme ga oddiy matn ("light"/"dark") yozgan.
   Unfold (Alpine $persist) şu kalitni JSON sifatida öqiydi va "light" da xato berib, sahifa skriptlarini
   toxtatadi. Alpine yuklanişidan oldin qiymatni JSON ga ögiramiz (UNFOLD["SCRIPTS"] — defer'siz). */
(function () {
    try {
        var value = localStorage.getItem("adminTheme");
        if (value === null) return;
        try {
            JSON.parse(value);
        } catch (e) {
            var theme = ["light", "dark", "auto"].indexOf(value) >= 0 ? value : "auto";
            localStorage.setItem("adminTheme", JSON.stringify(theme));
        }
    } catch (e) { /* localStorage yopiq — heç narsa qilmaymiz */ }
})();
