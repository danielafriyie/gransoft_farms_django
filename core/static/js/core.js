let burgerButton = document.getElementById('burger-button');
let sideNav = document.getElementById('side-nav');
let topBar = document.getElementById('top-bar');
let mainContent = document.getElementById('main-content');
let breadcrumbs = document.getElementById('bread-crumbs');
let overlay = document.getElementById('side-nav-overlay');

$(document).ready(function () {
    let userAccountModule = document.getElementById('user-accounts');
    let financeModule = document.getElementById('finance-module');
    let reportModule = document.getElementById('reports-module');
    let requestPath = window.location.pathname;

    if (requestPath.includes('/user-accounts')) {
        userAccountModule.classList.add('active-module');
        $(userAccountModule.nextElementSibling).show();
    }
    if (requestPath.includes('/finance')) {
        financeModule.classList.add('active-module');
        $(financeModule.nextElementSibling).show()
    }

    if (requestPath.includes('/reports')) {
        reportModule.classList.add('active-module');
    }
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


