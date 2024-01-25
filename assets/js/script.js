'use strict';

// Sidebar Toggle for Mobile
const sidebar = document.querySelector("[data-sidebar]");
document.querySelector("[data-sidebar-btn]").addEventListener("click", () => sidebar.classList.toggle("active"));

// Modal Functionality for Testimonials
const modal = { container: document.querySelector("[data-modal-container]"), overlay: document.querySelector("[data-overlay]") };
const toggleModal = () => [modal.container, modal.overlay].forEach(el => el.classList.toggle("active"));

[document.querySelector("[data-modal-close-btn]"), modal.overlay].forEach(el => el.addEventListener("click", toggleModal));

document.querySelectorAll("[data-testimonials-item]").forEach(item => {
    item.addEventListener("click", () => {
        ["src", "alt", "innerHTML"].forEach(attr => document.querySelector(`[data-modal-${attr}]`)[attr] = item.querySelector(`[data-testimonials-${attr}]`)[attr]);
        toggleModal();
    });
});

// Custom Select Dropdown for Portfolio Filter
const select = document.querySelector("[data-select]");
select.addEventListener("click", () => select.classList.toggle("active"));

document.querySelectorAll("[data-select-item]").forEach(item => {
    item.addEventListener("click", function () {
        const value = this.innerText.toLowerCase();
        document.querySelector("[data-selecct-value]").innerText = this.innerText;
        select.classList.toggle("active");
        filterFunc(value);
    });
});

const filterFunc = value => document.querySelectorAll("[data-filter-item]").forEach(item => item.classList.toggle("active", value === "all" || item.dataset.category.split(',').map(cat => cat.trim().toLowerCase()).includes(value)));

const filterBtn = document.querySelectorAll("[data-filter-btn]");
let lastBtn = filterBtn[0];
filterBtn.forEach(btn => {
    btn.addEventListener("click", function () {
        const value = this.innerText.toLowerCase();
        document.querySelector("[data-selecct-value]").innerText = this.innerText;
        filterFunc(value);
        [lastBtn, this].forEach(el => el.classList.toggle("active"));
        lastBtn = this;
    });
});

// Contact Form Validation
document.querySelectorAll("[data-form-input]").forEach(input => {
    input.addEventListener("input", () => document.querySelector("[data-form-btn]").disabled = !document.querySelector("[data-form]").checkValidity());
});

// Page Navigation
const navigation = { links: document.querySelectorAll("[data-nav-link]"), pages: document.querySelectorAll("[data-page]") };
navigation.links.forEach((link, index) => {
    link.addEventListener("click", () => {
        navigation.pages.forEach((page, pageIndex) => {
            [page, navigation.links[pageIndex]].forEach(el => el.classList.toggle("active", pageIndex === index));
        });
        window.scrollTo(0, 0);
    });
});
