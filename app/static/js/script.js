"use strict"
// Меню бургер

const iconMenu = document.querySelector('.burger__container');
const burgerMenu = document.querySelector('.burger__menu');
const burgerItem = document.querySelectorAll('.burger__item');
if (iconMenu) {
    iconMenu.addEventListener("click", function (e) {
        iconMenu.classList.toggle("_active");
        burgerMenu.classList.toggle("_active");
        for (let i = 0; i < 4; i++) {
            burgerItem[i].classList.toggle("_active");
        }
    });
};

// Слайдер

let position = 0;
const slidesToShow = 1;
const slidesToScroll = 1;
const container = document.querySelector('.slider-container');
if (container) {
    const track = document.querySelector('.slider-track');
    const items = document.querySelectorAll('.slider-item');
    const btnPrev = document.querySelector('.btn-prev');
    const btnNext = document.querySelector('.btn-next');
    const itemsCount = items.length;
    const itemWidth = container.clientWidth / slidesToShow;
    const movePosition = slidesToScroll * itemWidth;

    const checkBtns = () => {
        btnPrev.disabled = position === 0;
        btnNext.disabled = position <= -(itemsCount - slidesToShow) * itemWidth;
    };

    items.forEach((item) => {
        item.style.minWidth = `${itemWidth}px`;
    });

    const setPosition = () => {
        track.style.transform = `translateX(${position}px)`;
    };

    btnPrev.addEventListener('click', () => {
        const itemsLeft = Math.abs(position) / itemWidth;

        position += itemsLeft >= slidesToScroll ? movePosition : itemsLeft * itemWidth;
        console.log(position)
        setPosition();
        checkBtns();
    });

    btnNext.addEventListener('click', () => {
        const itemsLeft = itemsCount - (Math.abs(position) + slidesToShow * itemWidth) / itemWidth;

        position -= itemsLeft >= slidesToScroll ? movePosition : itemsLeft * itemWidth;
        console.log(position)
        setPosition();
        checkBtns();
    });
    checkBtns();
};
//AJAX

function sendRequest(method, url, body = null) {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open(method, url);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = () => {
            if (xhr.status >= 400) {
                reject(xhr.response);
            } else {
                resolve(xhr.response);
            };
        };
        xhr.onerror = () => {
            reject(xhr.response);
        };
        xhr.send(JSON.stringify(body));
    });
};

//cart

const checkboxs = document.querySelectorAll('.product__choise');

if (checkboxs) {
    for (let i = 0; i < checkboxs.length; i++) {
        checkboxs[i].addEventListener('click', () => {
            const checkboxs = document.querySelectorAll('.product__choise');
            if (checkboxs[i].firstElementChild.checked === true) {
                checkboxs[i].firstElementChild.checked = false;
            } else {
                checkboxs[i].firstElementChild.checked = true
            };
            checkboxs[i].classList.toggle("active");
        });
    };
};

const buyBtn = document.querySelector('.cart__buyBtn');
if (buyBtn) {
    buyBtn.addEventListener('click', () => {
        const checkedItems = document.querySelectorAll('input[type=checkbox]');
        let b = {
            'id': [],
            'action': 'buy'
        };
        for (let i = 0; i < checkedItems.length; i++) {
            if (checkedItems[i].checked === true) {
                b['id'].push(checkedItems[i].id);
            };
        };
        console.log(b);
        console.log(sendRequest('POST', 'http://jsonplaceholder.typicode.com/posts', b));
    });
}

function findAncector(el, cls) {
    while ((el = el.parentElement) && !el.classList.contains(cls));
    return el;
}

const deleteBtn = document.querySelector(".cart__clear");
if (deleteBtn) {
    deleteBtn.addEventListener('click', () => {
        const checkedItems = document.querySelectorAll('input[type=checkbox]');
        var items = document.querySelectorAll(".product");
        let b = {
            'id': [],
            'action': 'delete'
        };
        for (let i = 0; i < checkedItems.length; i++) {
            b['id'].push(checkedItems[i].id);
            items[i].remove();
        };
        console.log(b);
        console.log(sendRequest('POST', 'http://jsonplaceholder.typicode.com/posts', b));
    })
}

const crossBtn = document.querySelectorAll('.product__delete');
if (crossBtn) {
    for (let i = 0; i < crossBtn.length; i++) {
        crossBtn[i].addEventListener('click', () => {
            let b = {
                'id': [crossBtn[i].id],
                'action': 'delete'
            };
            console.log(b);
            console.log(sendRequest('POST', 'http://jsonplaceholder.typicode.com/posts', b));
            findAncector(crossBtn[i], "product").remove();
        })
    }
}
