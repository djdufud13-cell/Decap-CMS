/* ============================================================
   Liu's Blog — main_en.js (English Homepage)
   功能：移动端导航 / 返回顶部 / 平滑滚动 / 导航高亮 / 订阅 / 产品弹窗
   ============================================================ */
(function () {
  'use strict';

  /* ── 汉堡菜单 ─────────────────────────────────────────── */
  function initHamburger() {
    const hamburger = document.querySelector('.hamburger');
    const mobileNav = document.querySelector('.mobile-nav');
    if (!hamburger || !mobileNav) return;
    hamburger.addEventListener('click', () => {
      const isOpen = mobileNav.classList.toggle('open');
      hamburger.setAttribute('aria-expanded', isOpen);
    });
    mobileNav.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => { mobileNav.classList.remove('open'); });
    });
  }

  /* ── 返回顶部 ─────────────────────────────────────────── */
  function initBackToTop() {
    const btn = document.querySelector('.back-to-top');
    if (!btn) return;
    window.addEventListener('scroll', () => {
      btn.classList.toggle('visible', window.scrollY > 400);
    }, { passive: true });
    btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  /* ── 平滑滚动 ─────────────────────────────────────────── */
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          e.preventDefault();
          window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - 72, behavior: 'smooth' });
        }
      });
    });
  }

  /* ── 导航高亮 ─────────────────────────────────────────── */
  function initActiveNav() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.navbar-nav a');
    window.addEventListener('scroll', () => {
      let current = '';
      sections.forEach(sec => { if (window.scrollY >= sec.offsetTop - 80) current = sec.id; });
      navLinks.forEach(a => {
        a.classList.toggle('active', a.getAttribute('href') === '#' + current);
      });
    }, { passive: true });
  }

  /* ── 订阅表单 ─────────────────────────────────────────── */
  function initSubscribe() {
    const form = document.querySelector('.subscribe-form');
    if (!form) return;
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = form.querySelector('input');
      const btn = form.querySelector('button');
      if (input && input.value && input.value.includes('@')) {
        const orig = btn.textContent;
        btn.textContent = 'Subscribed OK';
        btn.style.background = '#C8882B';
        btn.disabled = true;
        input.value = '';
        setTimeout(() => { btn.textContent = orig; btn.style.background = ''; btn.disabled = false; }, 3000);
      } else if (input) {
        input.style.borderColor = '#e53';
        setTimeout(() => { input.style.borderColor = ''; }, 1500);
      }
    });
  }

  /* ── 产品详情弹窗 ─────────────────────────────────────── */
  const productData = {
    'handwheel': {
      icon: '01',
      title: 'Bakelite Handwheels',
      subtitle: 'DIN 950 Standard · Full Size Range',
      images: ['page_02_img_1.jpeg', 'page_03_img_1.jpeg', 'page_04_img_1.jpeg'],
      desc: 'Standard DIN 950 handwheels, full size range (40-320mm), customizable bore and keyway. Heat resistant, corrosion resistant, excellent insulation. Stable in food machinery, machine tools, and industrial equipment.',
      specs: [
        { label: 'Size Range', value: 'φ40 ~ φ320mm' },
        { label: 'Bore', value: 'φ6 ~ φ50mm (custom)' },
        { label: 'Material', value: 'PF2 / PF5 Phenolic' },
        { label: 'Temp Range', value: '-20°C ~ +150°C' },
        { label: 'Finish', value: 'Polished / Matte' },
        { label: 'MOQ', value: '100 pcs' },
      ],
      features: ['Heat Resistant', 'Corrosion Resistant', 'Insulating', 'Dimensional Stability', 'Comfortable Grip', 'Oil Resistant'],
      applications: ['Machine Tools', 'Food Machinery', 'Packaging', 'Printing', 'Textile'],
    },
    'handle': {
      icon: '02',
      title: 'Bakelite Handles',
      subtitle: 'Round / Cone / Star Types',
      images: ['product_2.png'],
      desc: 'Round handles, tapered handles, star handles (AK type) — full range. M3-M24 thread specs, non-standard sizes available. Excellent insulation for electrical equipment operating parts.',
      specs: [
        { label: 'Thread', value: 'M3 ~ M24' },
        { label: 'Head Dia.', value: 'φ10 ~ φ60mm' },
        { label: 'Material', value: 'PF2 Phenolic' },
        { label: 'Temp Range', value: '-20°C ~ +120°C' },
        { label: 'Types', value: 'Round/Cone/Star' },
        { label: 'MOQ', value: '200 pcs' },
      ],
      features: ['Standard Threads', 'Insulating', 'Comfortable Grip', 'Refined Finish', 'Non-slip'],
      applications: ['Electrical Cabinets', 'Control Panels', 'Instruments', 'Enclosures', 'Valve Operation'],
    },
    'lever': {
      icon: '03',
      title: 'Bakelite Levers',
      subtitle: 'Cross / Straight / T-Shape',
      images: ['product_3.png'],
      desc: 'Cross levers, flat levers, T-handle levers. Multiple specs, wear-resistant, oil-resistant, dimensionally stable. Batch consistency guaranteed for export quality.',
      specs: [
        { label: 'Length', value: '50 ~ 300mm' },
        { label: 'Handle Dia.', value: 'φ12 ~ φ30mm' },
        { label: 'Material', value: 'PF2 / PF5 Phenolic' },
        { label: 'Temp Range', value: '-20°C ~ +150°C' },
        { label: 'Types', value: 'Cross/Straight/T-Shape' },
        { label: 'MOQ', value: '100 pcs' },
      ],
      features: ['High Strength', 'Wear Resistant', 'Oil Resistant', 'Stable', 'Easy Install'],
      applications: ['Machine Operation', 'Valve Handles', 'Adjustment', 'Fixtures', 'Transmission'],
    },
    'oilsight': {
      icon: '04',
      title: 'Oil Sight Gauges',
      subtitle: 'Tempered Glass · Pressure Rated',
      images: ['product_4.png'],
      desc: 'Tempered glass oil windows, pressure rated 0.5-1.6MPa, temp range -20°C to +120°C. Metal frames in brass or stainless steel. For reducers, gearboxes, hydraulic systems.',
      specs: [
        { label: 'Pressure', value: '0.5 ~ 1.6 MPa' },
        { label: 'Temp Range', value: '-20°C ~ +120°C' },
        { label: 'Glass', value: 'Tempered' },
        { label: 'Frame', value: 'Brass / Stainless' },
        { label: 'Size', value: 'φ20 ~ φ100mm' },
        { label: 'MOQ', value: '50 pcs' },
      ],
      features: ['Pressure Rated', 'Sealed', 'Clear View', 'Corrosion Resistant', 'Easy Install'],
      applications: ['Reducers', 'Gearboxes', 'Hydraulic Stations', 'Lubrication', 'Transformers'],
    },
    'knob': {
      icon: '06',
      title: 'Bakelite Knobs & Dials',
      subtitle: 'UV Printed · Insulating',
      images: ['product_6.png'],
      desc: 'Electrical switch knobs, instrument dials. UV-printed characters, wear-resistant and clearly legible. Insulation grade E or above. Specs 15-100mm dia., custom available.',
      specs: [
        { label: 'Diameter', value: 'φ15 ~ φ100mm' },
        { label: 'Bore', value: 'φ3 ~ φ20mm' },
        { label: 'Material', value: 'PF2 Phenolic' },
        { label: 'Insulation', value: 'Class E or above' },
        { label: 'Printing', value: 'UV / Laser' },
        { label: 'MOQ', value: '200 pcs' },
      ],
      features: ['Insulating', 'Clear Print', 'Wear Resistant', 'Good Feel', 'Refined'],
      applications: ['Switches', 'Instrument Panels', 'Control Panels', 'Adjustment Knobs', 'Measurement'],
    },
  };

  function createProductModal() {
    const modal = document.createElement('div');
    modal.className = 'product-modal';
    modal.id = 'product-modal';
    modal.innerHTML = `
      <div class="product-modal-overlay"></div>
      <div class="product-modal-content">
        <button class="product-modal-close">×</button>
        <div class="product-modal-header">
          <div class="product-modal-image" id="modalImage"></div>
          <div class="product-modal-header-inner">
            <div class="product-modal-icon" id="modalIcon"></div>
            <div>
              <h2 class="product-modal-title" id="modalTitle"></h2>
              <div class="product-modal-subtitle" id="modalSubtitle"></div>
            </div>
          </div>
        </div>
        <div class="product-modal-body">
          <div class="product-modal-section">
            <div class="product-modal-section-title">Description</div>
            <p class="product-modal-text" id="modalDesc"></p>
          </div>
          <div class="product-modal-section">
            <div class="product-modal-section-title">Specifications</div>
            <div class="product-specs" id="modalSpecs"></div>
          </div>
          <div class="product-modal-section">
            <div class="product-modal-section-title">Features</div>
            <div class="product-features" id="modalFeatures"></div>
          </div>
          <div class="product-modal-section">
            <div class="product-modal-section-title">Applications</div>
            <div class="product-applications" id="modalApplications"></div>
          </div>
        </div>
        <div class="product-modal-cta">
          <a href="#contact" class="btn-primary" onclick="closeProductModal()">Request Quote</a>
          <a href="mailto:15503295692@163.com" class="btn-secondary">Send Drawings</a>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
    modal.querySelector('.product-modal-overlay').addEventListener('click', closeProductModal);
    modal.querySelector('.product-modal-close').addEventListener('click', closeProductModal);
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeProductModal(); });
  }

  function openProductModal(productKey) {
    const data = productData[productKey];
    if (!data) return;
    document.getElementById('modalIcon').textContent = data.icon;
    document.getElementById('modalTitle').textContent = data.title;
    document.getElementById('modalSubtitle').textContent = data.subtitle;
    document.getElementById('modalDesc').textContent = data.desc;

    // Product image
    const imageEl = document.getElementById('modalImage');
    if (data.images && data.images.length > 0) {
      imageEl.innerHTML = `<img src="assets/images/products/${data.images[0]}" alt="${data.title}">`;
    } else {
      imageEl.innerHTML = '';
    }

    document.getElementById('modalSpecs').innerHTML = data.specs.map(s => `
      <div class="product-spec-item">
        <div class="product-spec-label">${s.label}</div>
        <div class="product-spec-value">${s.value}</div>
      </div>
    `).join('');
    document.getElementById('modalFeatures').innerHTML = data.features.map(f => `<span class="product-feature">${f}</span>`).join('');
    document.getElementById('modalApplications').innerHTML = data.applications.map(a => `<span class="product-application">${a}</span>`).join('');
    document.getElementById('product-modal').classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  window.closeProductModal = function() {
    const modal = document.getElementById('product-modal');
    if (modal) { modal.classList.remove('open'); document.body.style.overflow = ''; }
  };

  function initProductModal() {
    createProductModal();
    document.querySelectorAll('[data-product]').forEach(el => {
      el.addEventListener('click', (e) => { e.preventDefault(); openProductModal(el.dataset.product); });
    });
  }

  /* ── 语言切换 ─────────────────────────────────────────── */
var langMenu = [
    { code: 'zh', label: '中文' },
    { code: 'en', label: 'English' },
    { code: 'ja', label: '日本語' },
    { code: 'ko', label: '한국어' },
    { code: 'ru', label: 'Русский' },
    { code: 'es', label: 'Español' },
    { code: 'fr', label: 'Français' },
    { code: 'it', label: 'Italiano' },
    { code: 'th', label: 'ภาษาไทย' },
    { code: 'vi', label: 'Tiếng Việt' },
  ];

function getLang() {
    var path = window.location.pathname;
    if (path.indexOf('/pages/ja') >= 0 || path === '/pages/ja/index.html') return 'ja';
    if (path.indexOf('/pages/ko') >= 0) return 'ko';
    if (path.indexOf('/pages/ru') >= 0) return 'ru';
    if (path.indexOf('/pages/es') >= 0) return 'es';
    if (path.indexOf('/pages/fr') >= 0) return 'fr';
    if (path.indexOf('/pages/it') >= 0) return 'it';
    if (path.indexOf('/pages/th') >= 0) return 'th';
    if (path.indexOf('/pages/vi') >= 0) return 'vi';
    if (path.indexOf('/pages/en') >= 0 || path === '/index_en.html') return 'en';
    return 'zh';
  }

function switchLang(lang) {
    var path = window.location.pathname;
    var onPages = /\/pages\/[a-z]{2}\//.test(path);

    // 在 /pages/xx/ 目录下
    if (onPages) {
      if (lang === 'zh') {
        // 回到根目录的 index.html
        window.location.href = '../../index.html';
      } else if (lang === 'en') {
        window.location.href = '../en/index.html';
      } else {
        // 切到其他语言
        window.location.href = '../' + lang + '/index.html';
        
        
      }
      return;
    }

    // 根目录文件（index.html 或 index_en.html）
    if (lang === 'zh') {
      window.location.href = 'index.html';
    } else if (lang === 'en') {
      window.location.href = 'index_en.html';
    } else {
      window.location.href = 'pages/' + lang + '/index.html';
    }
  }

function buildLangSwitcher(container) {
    var currentLang = getLang();
    var current = langMenu.find(function (l) { return l.code === currentLang; }) || langMenu[0];

    container.innerHTML = '\
      <button class="lang-btn" aria-haspopup="true" aria-expanded="false" aria-label="切换语言">\
        <span class="lang-icon">🌐</span>\
        <span class="lang-label">' + current.label + '</span>\
        <span style="font-size:0.6em;opacity:0.6;margin-left:2px;">▾</span>\
      </button>\
      <div class="lang-dropdown" role="menu">\
        ' + langMenu.map(function (l) {
          return '<a href="javascript:void(0)" data-lang="' + l.code + '" role="menuitem"' +
            (l.code === currentLang ? ' style="color:var(--brand);font-weight:600;"' : '') + '>\
            ' + l.label + '\
          </a>';
        }).join('') + '\
      </div>';

    // Toggle dropdown
    var btn = container.querySelector('.lang-btn');
    var dropdown = container.querySelector('.lang-dropdown');
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var expanded = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!expanded));
      dropdown.style.display = expanded ? 'none' : 'block';
    });
    document.addEventListener('click', function () {
      btn.setAttribute('aria-expanded', 'false');
      dropdown.style.display = 'none';
    });

    // Click to switch
    container.querySelectorAll('[data-lang]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        switchLang(link.dataset.lang);
      });
    });
  }

/* ── 初始化 ─────────────────────────────────────────── */

  function init() {
    initHamburger();
    initBackToTop();
    initSmoothScroll();
    initActiveNav();
    initSubscribe();
    initProductModal();
    // Language switcher
    var langSwitcherEl = document.querySelector('.lang-switcher');
    if (langSwitcherEl) buildLangSwitcher(langSwitcherEl);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  /* ── Hero背景图懒加载 ─────────────────────────────────────── */
  (function() {
    var hero = document.querySelector('[data-bg="hero"]');
    if (hero && 'IntersectionObserver' in window) {
      var obs = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            hero.classList.add('hero-loaded');
            obs.unobserve(hero);
          }
        });
      }, {rootMargin: '100px'});
      obs.observe(hero);
    } else if (hero) {
      hero.classList.add('hero-loaded');
    }
  })();
})();