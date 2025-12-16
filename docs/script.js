/**
 * What Changed - Demo Page Script
 * Language switching with dropdown menu
 */

(function () {
    'use strict';

    // Current language state
    let currentLang = 'en';
    let dropdownOpen = false;

    // Detect system language
    function detectLanguage() {
        var savedLang = localStorage.getItem('wc-lang');
        if (savedLang) {
            return savedLang;
        }

        var browserLang = navigator.language || navigator.userLanguage;
        if (browserLang && browserLang.indexOf('zh') === 0) {
            return 'zh';
        }
        return 'en';
    }

    // Apply language to all elements
    function applyLanguage(lang) {
        currentLang = lang;
        document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';

        // Update all elements with data-en and data-zh attributes
        var elements = document.querySelectorAll('[data-en][data-zh]');
        for (var i = 0; i < elements.length; i++) {
            elements[i].textContent = elements[i].getAttribute('data-' + lang);
        }

        // Update demo text visibility
        var enTexts = document.querySelectorAll('.demo-text-en');
        var zhTexts = document.querySelectorAll('.demo-text-zh');

        for (var j = 0; j < enTexts.length; j++) {
            enTexts[j].style.display = lang === 'en' ? 'block' : 'none';
        }
        for (var k = 0; k < zhTexts.length; k++) {
            zhTexts[k].style.display = lang === 'zh' ? 'block' : 'none';
        }

        // Update language button label
        var langLabel = document.getElementById('lang-label');
        if (langLabel) {
            langLabel.textContent = lang === 'en' ? 'EN' : '中';
        }

        // Update checkmarks
        var checkEn = document.getElementById('check-en');
        var checkZh = document.getElementById('check-zh');
        if (checkEn) checkEn.textContent = lang === 'en' ? '✓' : '';
        if (checkZh) checkZh.textContent = lang === 'zh' ? '✓' : '';

        // Save preference
        localStorage.setItem('wc-lang', lang);
    }

    // Toggle dropdown
    function toggleDropdown() {
        var dropdown = document.getElementById('lang-dropdown');
        if (!dropdown) return;

        dropdownOpen = !dropdownOpen;
        dropdown.classList.toggle('show', dropdownOpen);
    }

    // Close dropdown
    function closeDropdown() {
        var dropdown = document.getElementById('lang-dropdown');
        if (dropdown) {
            dropdownOpen = false;
            dropdown.classList.remove('show');
        }
    }

    // Select language
    function selectLanguage(lang) {
        applyLanguage(lang);
        closeDropdown();
    }

    // Initialize on DOM ready
    document.addEventListener('DOMContentLoaded', function () {
        // Detect and apply initial language
        var detectedLang = detectLanguage();
        applyLanguage(detectedLang);

        // Bind language toggle button
        var langBtn = document.getElementById('lang-btn');
        if (langBtn) {
            langBtn.addEventListener('click', function (e) {
                e.stopPropagation();
                toggleDropdown();
            });
        }

        // Bind language options
        var langOptions = document.querySelectorAll('.lang-option');
        for (var i = 0; i < langOptions.length; i++) {
            langOptions[i].addEventListener('click', function (e) {
                e.stopPropagation();
                var lang = this.getAttribute('data-lang');
                selectLanguage(lang);
            });
        }

        // Close dropdown when clicking outside
        document.addEventListener('click', function () {
            closeDropdown();
        });

        // Smooth reveal animations on scroll
        var sections = document.querySelectorAll('.section');

        if ('IntersectionObserver' in window) {
            var observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };

            var observer = new IntersectionObserver(function (entries) {
                for (var i = 0; i < entries.length; i++) {
                    if (entries[i].isIntersecting) {
                        entries[i].target.classList.add('visible');
                    }
                }
            }, observerOptions);

            for (var j = 0; j < sections.length; j++) {
                sections[j].classList.add('fade-in');
                observer.observe(sections[j]);
            }
        }

        console.log('What Changed Demo Page Loaded - Language: ' + detectedLang);
    });
})();
