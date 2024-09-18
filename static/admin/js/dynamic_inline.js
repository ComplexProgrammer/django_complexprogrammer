document.addEventListener('DOMContentLoaded', function() {
    let totalForms = document.querySelector('#id_productdetail_set-TOTAL_FORMS');
    let addButton = document.createElement('button');
    addButton.type = 'button';
    addButton.innerText = 'Yangi mahsulot qo\'shish';
    addButton.style.margin = '10px 0';

    document.querySelector('.inline-group').appendChild(addButton);

    addButton.addEventListener('click', function() {
        let formCount = parseInt(totalForms.value);
        let newForm = document.querySelector('.dynamic-productdetail_set').cloneNode(true);

        newForm.innerHTML = newForm.innerHTML.replace(/__prefix__/g, formCount);
        document.querySelector('.inline-group tbody').appendChild(newForm);
        totalForms.value = formCount + 1;
    });
});
