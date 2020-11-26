let burgerButton = document.getElementById('burger-button');
let sideNav = document.getElementById('side-nav');
let topBar = document.getElementById('top-bar');
let mainContent = document.getElementById('main-content');
let breadcrumbs = document.getElementById('bread-crumbs');
let overlay = document.getElementById('side-nav-overlay');
let requestPath = window.location.pathname;

function setActiveModule(path, elm_id, showSubMenu = false) {
    let elm = document.getElementById(elm_id);
    if (requestPath.split('/')[1] === path) {
        elm.classList.add('active-module');

        if (showSubMenu) {
            $(elm.nextElementSibling).show()
        }
    }
}

$(document).ready(function () {
    setActiveModule('user-accounts', 'user-accounts-nav');
    setActiveModule('finance', 'finance-module');
    setActiveModule('birds', 'birds-module');
    setActiveModule('reports', 'reports-module');
    setActiveModule('eggs', 'eggs-module');
});

if (window.matchMedia('(min-width: 1450px)').matches) {
    $(burgerButton).click(function () {
        // burgerButton.classList.toggle('change');
        sideNav.classList.toggle('slideOutLeft');
        topBar.classList.toggle('top-bar-clicked');
        if (topBar.classList.contains('top-bar-clicked')) {
            topBar.style.width = '100%';
            mainContent.style.width = '100%';
            breadcrumbs.style.width = '100%';
            if (sideNav.classList.contains('slideInLeft')) {
                sideNav.classList.remove('slideInLeft')
            }
        } else {
            topBar.style.width = '85%';
            mainContent.style.width = '85%';
            breadcrumbs.style.width = '85%';
            sideNav.classList.toggle('slideInLeft');
        }

    });
}

if (window.matchMedia('(max-width: 1449px)').matches) {
    $(burgerButton).click(function () {
        if (sideNav.classList.contains('slideInLeft')) {
            sideNav.classList.remove('slideInLeft');
            sideNav.classList.remove('slideOutLeft');
        }
        sideNav.classList.toggle('slideInLeft');
        sideNav.style.display = 'block';
        overlay.classList.toggle('fadIn');
        overlay.style.display = 'block';
        $(overlay).fadeIn(600)
    });
    $(overlay).click(function () {
        sideNav.classList.toggle('slideOutLeft');
        sideNav.style.display = 'none';
        overlay.style.display = 'none';
    });
}

function dropDownMenu(elm) {
    let subMenu = elm.nextElementSibling;
    $(subMenu).slideToggle();
}

function confirmModal(form_id, title) {
    let modalBtn = document.getElementById('confirm-modal-button');
    let modalTitle = document.getElementById('confirm-modal-title');
    modalTitle.innerHTML = title;
    $(modalBtn).click(function () {
        document.getElementById(form_id).submit();
    });
}


