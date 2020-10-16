let burgerButton = document.getElementById('burger-button');
let sideNav = document.getElementById('side-nav');
let topBar = document.getElementById('top-bar');
let mainContent = document.getElementById('main-content');
let breadcrumbs = document.getElementById('bread-crumbs');
let overlay = document.getElementById('side-nav-overlay');
let requestPath = window.location.pathname;

function setActiveModule(path, module, showSubMenu = false) {
    if (requestPath.includes(path)) {
        module.classList.add('active-module');

        if (showSubMenu) {
            $(module.nextElementSibling).show()
        }
    }
}

$(document).ready(function () {
    let userAccountModule = document.getElementById('user-accounts');
    let userAccountsNav = document.getElementById('user-accounts-nav');
    setActiveModule('/user-accounts', userAccountModule, true);
    setActiveModule('/user-accounts', userAccountsNav);


    let financeModule = document.getElementById('finance-module');
    setActiveModule('/finance', financeModule);

    let financePurchaseModule = document.getElementById('finance-purchases-module');
    setActiveModule('/finance/purchases', financePurchaseModule, true);

    let medFeedsModule = document.getElementById('med-feeds-module');
    let medsModule = document.getElementById('medicine-module');
    let feedsModule = document.getElementById('feeds-module');
    setActiveModule('meds-feeds/', medFeedsModule);

    let reportModule = document.getElementById('reports-module');
    setActiveModule('/reports', reportModule);
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


