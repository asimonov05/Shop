"use strict"

// Меню бургер

const iconMenu = document.querySelector('.burger__container');
const burgerMenu = document.querySelector('.burger__menu');
const burgerItem = document.querySelectorAll('.burger__item');
if (iconMenu) {
    iconMenu.addEventListener("click", function (e) {
        iconMenu.classList.toggle("_active");
        burgerMenu.classList.toggle("_active");
        for (let i = 0; i < 4; i++){
            burgerItem[i].classList.toggle("_active");
        }
    });
}

// Слайдер

let position = 0;
const slidesToShow = 1;
const slidesToScroll = 1;
const container = document.querySelector('.slider-container');
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