// PC Ramduhawma's Homepage - Main JavaScript
// Minimal JS for theme modes, mobile menu and lightbox

// Retro / Modern mode switch (same content, two eras)
(function() {
    var KEY = 'pc-theme';

    function read() {
        try {
            var t = localStorage.getItem(KEY);
            return t === 'modern' ? 'modern' : 'retro';
        } catch (e) {
            return 'retro';
        }
    }

    function paint(t, animate) {
        if (t !== 'modern') t = 'retro';
        var modern = t === 'modern';
        document.documentElement.dataset.theme = t;
        if (document.body) document.body.dataset.theme = t;
        try { localStorage.setItem(KEY, t); } catch (e) {}
        document.querySelectorAll('[data-theme-toggle]').forEach(function(btn) {
            btn.setAttribute('aria-pressed', modern ? 'true' : 'false');
            btn.setAttribute('aria-label', modern ? 'Return to retro mode' : 'Switch to modern mode');
            var label = btn.querySelector('[data-theme-label]');
            if (label) label.textContent = modern ? 'Retro' : 'Modern';
            var icon = btn.querySelector('[data-theme-icon]');
            if (icon) icon.textContent = modern ? '🖥️' : '✨';
        });
        if (animate && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            document.documentElement.classList.add('theme-fade');
            setTimeout(function() {
                document.documentElement.classList.remove('theme-fade');
            }, 320);
        }
    }

    window.pcTheme = { get: read, set: function(t) { paint(t, true); } };

    document.addEventListener('DOMContentLoaded', function() {
        paint(read(), false);
        document.querySelectorAll('[data-theme-toggle]').forEach(function(btn) {
            btn.addEventListener('click', function() {
                paint(document.documentElement.dataset.theme === 'modern' ? 'retro' : 'modern', true);
            });
        });
    });
})();

document.addEventListener('DOMContentLoaded', function() {
    var menuBtn = document.getElementById('mobileMenuBtn');
    var sidebar = document.getElementById('sidebar');
    var menuIcon = menuBtn ? menuBtn.querySelector('span') : null;

    function setMenu(open) {
        if (!sidebar || !menuBtn) return;
        sidebar.classList.toggle('active', open);
        menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
        if (menuIcon) menuIcon.innerHTML = open ? '&#10005;' : '&#9776;';
    }

    if (menuBtn && sidebar) {
        menuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            setMenu(!sidebar.classList.contains('active'));
        });

        sidebar.querySelectorAll('a').forEach(function(link) {
            link.addEventListener('click', function() {
                if (window.innerWidth <= 768) setMenu(false);
            });
        });
    }

    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768 && sidebar && sidebar.classList.contains('active')) {
            if (!sidebar.contains(e.target) && !menuBtn.contains(e.target)) {
                setMenu(false);
            }
        }
    });

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar && sidebar.classList.contains('active')) {
            setMenu(false);
        }
    });

    window.addEventListener('resize', function() {
        if (window.innerWidth > 768 && sidebar && sidebar.classList.contains('active')) {
            setMenu(false);
        }
    });

    function lightbox(src) {
        var overlay = document.createElement('div');
        overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.9);z-index:2000;display:flex;align-items:center;justify-content:center;cursor:pointer;padding:12px;box-sizing:border-box;';

        var fullImg = document.createElement('img');
        fullImg.src = src;
        fullImg.style.cssText = 'max-width:100%;max-height:90vh;width:auto;height:auto;border:3px solid #666;';

        var closeBtn = document.createElement('div');
        closeBtn.textContent = 'X';
        closeBtn.style.cssText = 'position:absolute;top:12px;right:16px;color:white;font-size:28px;font-weight:bold;cursor:pointer;min-width:44px;min-height:44px;display:flex;align-items:center;justify-content:center;';

        overlay.appendChild(fullImg);
        overlay.appendChild(closeBtn);
        document.body.appendChild(overlay);

        overlay.addEventListener('click', function() {
            if (overlay.parentNode) overlay.parentNode.removeChild(overlay);
        });
    }

    document.querySelectorAll('.gallery-item-image').forEach(function(img) {
        img.addEventListener('click', function() { lightbox(this.src); });
    });

    document.querySelectorAll('.screenshot-thumb').forEach(function(img) {
        img.addEventListener('click', function() { lightbox(this.src); });
    });

    document.querySelectorAll('a[href="#"]').forEach(function(link) {
        link.addEventListener('click', function(e) {
            if (this.textContent.includes('Back to Top')) {
                e.preventDefault();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    });
});
