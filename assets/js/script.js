'use strict';

// Sidebar Toggle for Mobile
const sidebarElement = document.querySelector("[data-sidebar]");
document.querySelector("[data-sidebar-btn]").addEventListener("click", () => sidebarElement.classList.toggle("show-sidebar"));

// Modal Functionality for Testimonials
const modalElements = { 
    container: document.querySelector("[data-modal-container]"), 
    overlay: document.querySelector("[data-overlay]") 
};
const toggleModalDisplay = () => Object.values(modalElements).forEach(el => el.classList.toggle("visible"));

[document.querySelector("[data-modal-close-btn]"), modalElements.overlay].forEach(el => el.addEventListener("click", toggleModalDisplay));

document.querySelectorAll("[data-testimonials-item]").forEach(testimonial => {
    testimonial.addEventListener("click", () => {
        ["src", "alt", "innerHTML"].forEach(attribute => {
            document.querySelector(`[data-modal-${attribute}]`)[attribute] = testimonial.querySelector(`[data-testimonials-${attribute}]`)[attribute];
        });
        toggleModalDisplay();
    });
});

// Custom Select Dropdown for Portfolio Filter
const selectDropdown = document.querySelector("[data-select]");
selectDropdown.addEventListener("click", () => selectDropdown.classList.toggle("open"));

document.querySelectorAll("[data-select-item]").forEach(option => {
    option.addEventListener("click", function () {
        const filterValue = this.textContent.trim().toLowerCase();
        document.querySelector("[data-selecct-value]").textContent = this.textContent;
        selectDropdown.classList.toggle("open");
        applyFilter(filterValue);
    });
});

const applyFilter = filterValue => {
    document.querySelectorAll("[data-filter-item]").forEach(item => {
        const categories = item.dataset.category.split(',').map(cat => cat.trim().toLowerCase());
        item.classList.toggle("show-item", filterValue === "all" || categories.includes(filterValue));
    });
};

const filterButtons = document.querySelectorAll("[data-filter-btn]");
let previouslyClickedBtn = filterButtons[0];
filterButtons.forEach(btn => {
    btn.addEventListener("click", function () {
        const filterValue = this.textContent.toLowerCase();
        document.querySelector("[data-selecct-value]").textContent = this.textContent;
        applyFilter(filterValue);
        [previouslyClickedBtn, this].forEach(el => el.classList.toggle("active-button"));
        previouslyClickedBtn = this;
    });
});

// Contact Form Validation
const formInputs = document.querySelectorAll("[data-form-input]");
const submitButton = document.querySelector("[data-form-btn]");
const formElement = document.querySelector("[data-form]");

formInputs.forEach(inputField => {
    inputField.addEventListener("input", () => {
        submitButton.disabled = !formElement.checkValidity();
    });
});

// Page Navigation
const navigationElements = { 
    links: document.querySelectorAll("[data-nav-link]"), 
    pages: document.querySelectorAll("[data-page]") 
};

navigationElements.links.forEach((navLink, index) => {
    navLink.addEventListener("click", () => {
        navigationElements.pages.forEach((page, pageIndex) => {
            const isActive = pageIndex === index;
            page.classList.toggle("active-page", isActive);
            navLink.classList.toggle("selected", isActive);
        });
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});
