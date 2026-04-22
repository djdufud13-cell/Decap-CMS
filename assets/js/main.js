/* ============================================================
   刘的博客 · main.js
   功能：语言切换 / 产品弹窗 / 订阅表单 / 移动菜单
   ============================================================ */

(function () {
  'use strict';

  /* ── 0. 语言代码检测 ─────────────────────────────── */
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

  /* ── 1. 语言菜单定义 ─────────────────────────────── */
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

  /* ── 2. 语言路由 ───────────────────────────────── */
  var navLinks = {
    zh: ['index.html', 'pages/zh/blog.html', '#products', '#contact'],
    en: ['index_en.html', 'pages/en/blog.html', '#products', '#contact'],
    ja: ['pages/ja/index.html', 'pages/ja/blog.html', '#products', '#contact'],
    ko: ['pages/ko/index.html', 'pages/ko/blog.html', '#products', '#contact'],
    ru: ['pages/ru/index.html', 'pages/ru/blog.html', '#products', '#contact'],
    es: ['pages/es/index.html', 'pages/es/blog.html', '#products', '#contact'],
    fr: ['pages/fr/index.html', 'pages/fr/blog.html', '#products', '#contact'],
    it: ['pages/it/index.html', 'pages/it/blog.html', '#products', '#contact'],
    th: ['pages/th/index.html', 'pages/th/blog.html', '#products', '#contact'],
    vi: ['pages/vi/index.html', 'pages/vi/blog.html', '#products', '#contact'],
  };

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

  /* ── 3. 语言切换下拉菜单 ────────────────────────── */
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

  /* ── 4. 移动端汉堡菜单 ─────────────────────────── */
  function initMobileNav() {
    var hamburger = document.querySelector('.hamburger');
    var mobileNav = document.querySelector('.mobile-nav');
    if (!hamburger || !mobileNav) return;

    hamburger.addEventListener('click', function () {
      var expanded = hamburger.getAttribute('aria-expanded') === 'true';
      hamburger.setAttribute('aria-expanded', String(!expanded));
      mobileNav.classList.toggle('open');
      hamburger.classList.toggle('open');
    });

    mobileNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        mobileNav.classList.remove('open');
        hamburger.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ── 5. 平滑滚动 ───────────────────────────────── */
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
      anchor.addEventListener('click', function (e) {
        var targetId = this.getAttribute('href');
        if (targetId === '#' || targetId.length <= 1) return;
        var target = document.querySelector(targetId);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  /* ── 6. 产品弹窗 ───────────────────────────────── */
  var PRODUCTS = {
    handwheel: {
      title: '胶木手轮',
      titleEn: 'Bakelite Handwheel',
      specs: [
        ['标准', 'DIN 950 / DIN 1804'],
        ['材质', '酚醛树脂 PF（电木/Bakelite）'],
        ['规格', 'φ40mm ~ φ320mm'],
        ['最大孔径', 'Φ38mm（标准）'],
        ['耐温', '-30°C ~ +130°C'],
        ['颜色', '黑色（标准）/ 棕色'],
        ['认证', 'RoHS / REACH（可选）'],
      ],
      features: ['标准DIN 950规格，规格齐全互换性强', '优异的耐热性，连续耐温可达130°C', '良好的电绝缘性能，介电强度 > 10kV/mm', '化学耐腐蚀，耐大多数油脂和溶剂', '摩擦系数低，手感舒适，操作噪音小', '支持定制孔径、键槽宽度、颜色'],
      applications: ['机床设备 / 食品机械 / 包装设备', '阀门与管道系统 / 仪器仪表', '纺织机械 / 印刷设备', '电工电气设备 / 实验室仪器'],
      images: ['products/product_1.png', 'products/product_1.png'],
      icon: '01',
    },
    handle: {
      title: '胶木把手',
      titleEn: 'Bakelite Handle',
      specs: [
        ['类型', '圆头把手 / 锥头把手 / 星型把手 AK型'],
        ['材质', '酚醛树脂 PF（电木）'],
        ['螺纹规格', 'M3 ~ M24（全系列）'],
        ['耐温', '-30°C ~ +130°C'],
        ['绝缘', 'E级绝缘，耐压 > 10kV'],
        ['颜色', '黑色 / 棕色'],
      ],
      features: ['全系列螺纹规格，覆盖M3~M24', '酚醛材质，绝缘性能优越，适合电气设备', '表面光滑，耐油脂，耐大多数化学品', '多种头部形状可选（圆头/锥头/星型）', '可按非标尺寸定制'],
      applications: ['电气开关柜 / 配电箱', '机械设备操作面板', '仪器仪表调节', '家用电器的操作把手'],
      images: ['products/product_2.png', 'products/product_2.png', 'products/product_2.png'],
      icon: '02',
    },
    lever: {
      title: '胶木手柄',
      titleEn: 'Bakelite Lever Handle',
      specs: [
        ['类型', '十字手柄 / 一字手柄 / T型手柄'],
        ['材质', '酚醛树脂 PF'],
        ['螺纹规格', 'M4 ~ M20'],
        ['耐温', '-30°C ~ +130°C'],
        ['表面', '光洁，耐磨'],
        ['认证', 'RoHS'],
      ],
      features: ['多种操作形式：十字、一字、T型', '酚醛树脂，耐磨、耐油，尺寸稳定', '机械强度高，长期使用不变形', '长期供货，批次一致性好'],
      applications: ['机床操作面板', '阀门手轮', '测试设备', '木工机械'],
      images: ['products/page_11_img_1.jpeg', 'products/page_11_img_1.jpeg'],
      icon: '03',
    },
    oilsight: {
      title: '油镜 / 油标',
      titleEn: 'Oil Sight Glass',
      specs: [
        ['玻璃', '钢化硼硅玻璃，耐压0.5~1.6MPa'],
        ['耐温', '-20°C ~ +120°C（玻璃部分）'],
        ['框架材质', '黄铜 / 不锈钢304/316'],
        ['密封', 'NBR / 氟橡胶（耐油型）'],
        ['接口螺纹', 'G1/4 ~ G2（多种规格）'],
        ['标准', 'DIN 11851 / ISO 2084（可定制）'],
      ],
      features: ['钢化硼硅玻璃，透视清晰，强度高', '金属框架防撞设计，使用安全', '多种密封材料可选，耐油型配置', '可承受正压和一定负压'],
      applications: ['减速机 / 齿轮箱 / 变速箱', '液压站 / 润滑油路', '石化储罐液位观察', '食品机械润滑系统'],
      images: ['products/product_4.png', 'products/product_4.png', 'products/product_4.png'],
      icon: '04',
    },
    knob: {
      title: '胶木旋钮 / 刻度盘',
      titleEn: 'Bakelite Knob & Dial',
      specs: [
        ['材质', '酚醛树脂 PF'],
        ['规格', 'φ15mm ~ φ100mm'],
        ['绝缘等级', 'E级（耐温130°C）'],
        ['表面字符', 'UV印字，清晰耐磨'],
        ['螺纹', 'M4 ~ M12（可定制）'],
        ['刻度', '0~270° 多种刻度盘可选'],
      ],
      features: ['表面字符UV印刷，清晰耐磨不掉色', '酚醛材质，绝缘性能优越', '多种刻度盘可选（数字/字母/符号）', '手感舒适，定位准确'],
      applications: ['电器开关旋钮', '仪表仪器刻度盘', '音频设备旋钮', '实验室调节旋钮'],
      images: ['products/product_6.png', 'products/page_16_img_1.jpeg', 'products/page_17_img_1.jpeg'],
      icon: '05',
    },
  };

  function openProductModal(productId) {
    var product = PRODUCTS[productId];
    if (!product) return;

    var modal = document.getElementById('product-modal');
    if (!modal) return;

    // Set modal title
    var titleEl = modal.querySelector('.modal-product-title');
    if (titleEl) titleEl.textContent = product.title;

    // Build specs table
    var specsBody = modal.querySelector('#modal-specs-body');
    if (specsBody) {
      specsBody.innerHTML = product.specs.map(function (row) {
        return '<tr><td style="color:var(--text-muted);font-size:0.88em;">' + row[0] + '</td><td style="font-weight:500;">' + row[1] + '</td></tr>';
      }).join('');
    }

    // Build features
    var featuresEl = modal.querySelector('#modal-features');
    if (featuresEl) {
      featuresEl.innerHTML = '<ul style="margin:0;padding-left:18px;">' +
        product.features.map(function (f) { return '<li style="margin-bottom:6px;color:var(--text);">' + f + '</li>'; }).join('') +
        '</ul>';
    }

    // Build applications
    var appsEl = modal.querySelector('#modal-applications');
    if (appsEl) {
      appsEl.innerHTML = product.applications.map(function (a) {
        return '<span class="tag" style="margin:3px;">' + a + '</span>';
      }).join('');
    }

    // Set icon
    var iconEl = modal.querySelector('.modal-product-icon');
    if (iconEl) iconEl.textContent = product.icon;

    // Images
    var mainImg = modal.querySelector('.product-modal-image img');
    var thumbsContainer = modal.querySelector('.product-thumbs');
    if (mainImg && product.images && product.images.length > 0) {
      mainImg.src = 'assets/images/' + product.images[0];
      mainImg.alt = product.title;
    }
    // Only show first image, hide thumbs container
    if (thumbsContainer) {
      thumbsContainer.style.display = 'none';
    }

    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeProductModal() {
    var modal = document.getElementById('product-modal');
    if (!modal) return;
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  function initProductModals() {
    // 详情链接 → 弹窗
    document.querySelectorAll('[data-product]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        openProductModal(this.dataset.product);
      });
    });

    // 关闭按钮
    var closeBtn = document.querySelector('.product-modal-close');
    if (closeBtn) closeBtn.addEventListener('click', closeProductModal);

    // 点击遮罩关闭
    var modal = document.getElementById('product-modal');
    if (modal) {
      modal.addEventListener('click', function (e) {
        if (e.target === modal) closeProductModal();
      });
    }

    // ESC 关闭
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeProductModal();
    });
  }

  /* ── 7. 订阅表单 ───────────────────────────────── */
  function initSubscribeForm() {
    var forms = document.querySelectorAll('.subscribe-form');
    forms.forEach(function (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var emailInput = form.querySelector('input[type="email"]');
        var btn = form.querySelector('button[type="submit"]');
        if (!emailInput || !emailInput.value || !emailInput.value.includes('@')) {
          alert('请输入有效的邮箱地址');
          return;
        }
        var originalText = btn.textContent;
        btn.textContent = '订阅成功 ✓';
        btn.style.background = 'var(--brand)';
        btn.disabled = true;
        emailInput.value = '';
        setTimeout(function () {
          btn.textContent = originalText;
          btn.style.background = '';
          btn.disabled = false;
        }, 3000);
      });
    });
  }

  /* ── 8. 高德地图加载 ───────────────────────────── */
  function loadMap() {
    var mapContainer = document.getElementById('amap-container');
    if (!mapContainer) return;
    var script = document.createElement('script');
    script.src = 'https://webapi.amap.com/maps?v=2.0&key=YOUR_MAP_KEY&callback=initAMap';
    script.async = true;
    document.head.appendChild(script);
  }

  /* ── 9. 初始化 ─────────────────────────────────── */
  function init() {
    // Clear stale language preference - each page has its own content
    localStorage.removeItem("liu_blog_lang");
    // applyI18n removed: each page has its own language content
    // 语言切换器
    var langSwitcherEl = document.querySelector('.lang-switcher');
    if (langSwitcherEl) buildLangSwitcher(langSwitcherEl);

    // 移动菜单
    initMobileNav();

    // 平滑滚动
    initSmoothScroll();

    // 产品弹窗
    initProductModals();

    // 订阅表单
    initSubscribeForm();

    // 地图
    loadMap();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  /* ── 11. I18N 多语言翻译数据 ─────────────────────────────────────── */
  var I18N = {
    nav: {
      zh: ['首页', '博客', '产品', '联系'],
      en: ['Home', 'Blog', 'Products', 'Contact'],
      ja: ['ホーム', 'ブログ', '製品', 'お問い合わせ'],
      ko: ['홈', '블로그', '제품', '문의'],
      ru: ['Главная', 'Блог', 'Продукция', 'Контакты'],
      es: ['Inicio', 'Blog', 'Productos', 'Contacto'],
      fr: ['Accueil', 'Blog', 'Produits', 'Contact'],
      it: ['Home', 'Blog', 'Prodotti', 'Contatti'],
      th: ['หน้าแรก', 'บล็อก', 'สินค้า', 'ติดต่อ'],
      vi: ['Trang chu', 'Blog', 'San pham', 'Lien he'],
    },
    hero: {
      zh: { label: '酚醛树脂配件专家', title: '专注胶木工艺\n15年匠心制造', subtitle: '从原材料到成品的全流程管控，为机械、电气、石化等领域提供可靠的酚醛树脂配件解决方案。', stats1: '年出口量', stats1val: '200万+', stats2: '出口国家', stats2val: '30+', stats3: '行业经验', stats3val: '15年', cta1: '查看产品', cta2: '了解更多' },
      en: { label: 'Bakelite Parts Expert', title: '15 Years of Precision\nBakelite Manufacturing', subtitle: 'Full-process control from raw materials to finished products, providing reliable phenolic resin component solutions for machinery, electrical, petrochemical and other fields.', stats1: 'Annual Export', stats1val: '2M+', stats2: 'Countries', stats2val: '30+', stats3: 'Years Experience', stats3val: '15 yrs', cta1: 'View Products', cta2: 'Learn More' },
      ja: { label: 'ベークライト部品の専門家', title: '15年を振り返る\nベークライト製造の匠', subtitle: '原材料から完成品までの全工程を管理し、機械・電気・石油化学などの分野に信頼できるフェノール樹脂部品ソリューションを提供します。', stats1: '年間輸出量', stats1val: '200万+', stats2: '輸出国', stats2val: '30+', stats3: '業界経験', stats3val: '15年', cta1: '製品を見る', cta2: '詳しく見る' },
      ko: { label: '베이클라이트 부품 전문가', title: '15년 장인\n베이클라이트 제조', subtitle: '원자재부터 완제품까지 전 공정을 관리하여 기계, 전기, 석유화학 등의 분야에 신뢰할 수 있는 페놀 수지 부품 솔루션을 제공합니다.', stats1: '연간 수출량', stats1val: '200만+', stats2: '수출 국가', stats2val: '30+', stats3: '업계 경력', stats3val: '15년', cta1: '제품 보기', cta2: '자세히 보기' },
      ru: { label: 'Эксперт по бакелитовым деталям', title: '15 лет мастерства\nпроизводства бакелита', subtitle: 'Полный контроль производственного цикла от сырья до готовой продукции для машиностроения, электротехники, нефтехимии и других отраслей.', stats1: 'Годовой экспорт', stats1val: '2M+', stats2: 'Стран', stats2val: '30+', stats3: 'Лет опыта', stats3val: '15 лет', cta1: 'Смотреть продукцию', cta2: 'Узнать больше' },
      es: { label: 'Experto en piezas de baquelita', title: '15 anos de experiencia\nen fabricacion de baquelita', subtitle: 'Control integral del proceso productivo desde la materia prima hasta el producto terminado, ofreciendo soluciones confiables de piezas de resina fenolica para maquinaria, electricidad, petroquimica y mas.', stats1: 'Exportacion anual', stats1val: '2M+', stats2: 'Paises', stats2val: '30+', stats3: 'Anos de experiencia', stats3val: '15 anos', cta1: 'Ver productos', cta2: 'Saber mas' },
      fr: { label: 'Expert en pieces en bakelite', title: '15 ans de savoir-faire\nen fabrication de bakelite', subtitle: 'Controle complet du processus de production, de la matiere premiere au produit fini, offrant des solutions fiables en pieces en resine phenolique pour la machinerie, l\'electricite, la petrochimie et autres.', stats1: 'Exportations annuelles', stats1val: '2M+', stats2: 'Pays', stats2val: '30+', stats3: 'Annees d\'experience', stats3val: '15 ans', cta1: 'Voir les produits', cta2: 'En savoir plus' },
      it: { label: 'Esperto di componenti in bachelite', title: '15 anni di artigianato\nnella produzione di bachelite', subtitle: 'Controllo dell\'intero processo produttivo, dalla materia prima al prodotto finito, per offrire soluzioni affidabili in resine fenoliche per macchinari, elettrico, petrolchimico e altro.', stats1: 'Esportazione annuale', stats1val: '2M+', stats2: 'Paesi', stats2val: '30+', stats3: 'Anni di esperienza', stats3val: '15 anni', cta1: 'Vedi prodotti', cta2: 'Scopri di piu' },
      th: { label: 'ผู้เชี่ยวชาญชิ้นส่วนเบคคาไลต์', title: 'ช่างผู้ผลิตเบคคาไลต์\n15 ปีแห่งความเชี่ยวชาญ', subtitle: 'ควบคุมกระบวนการผลิตทั้งหมดตั้งแต่วัตถุดิบจนถึงผลิตภัณฑ์สำเร็จ นำเสนอโซลูชันชิ้นส่วนเรซิ่นฟีนอลที่เชื่อถือได้สำหรับอุตสาหกรรมเครื่องจักร อิเล็กทริก เพทรอคมีคอลและอื่นๆ', stats1: 'ส่งออกต่อปี', stats1val: '2M+', stats2: 'ประเทศ', stats2val: '30+', stats3: 'ประสบการณ์', stats3val: '15 ปี', cta1: 'ดูสินค้า', cta2: 'เรียนรู้เพิ่มเติม' },
      vi: { label: 'Chuyen gia linh kien bakelit', title: '15 nam kinh nghiem\nsan xuat bakelit', subtitle: 'Kiem soat toan bo quy trinh tu nguyen lieu den thanh pham, cung cap giai phap linh kien nhua fenol dang tin cay cho may moc, dien, hoa chat va cac linh vuc khac.', stats1: 'Xuat khau hang nam', stats1val: '2M+', stats2: 'Quoc gia', stats2val: '30+', stats3: 'Nam kinh nghiem', stats3val: '15 nam', cta1: 'Xem san pham', cta2: 'Tìm hieu them' },
    },
    about: {
      zh: { label: '关于刘工', title: '15年专注酚醛树脂配件制造', p1: '我叫刘工，来自河北衡水，专业从事酚醛树脂（胶木/Bakelite）机械配件的设计与制造。', p2: '酚醛树脂是世界上最早实现工业化生产的合成高分子材料，拥有优异的耐热性、电气绝缘性和机械强度，广泛应用于电工电气、机械设备、汽车配件、石油化工、轨道交通等领域。', p3: '我的产品覆盖标准件和定制件两大类，标准件常备库存最快当天发货，定制件从图纸确认到交付通常15-30天。' },
      en: { label: 'About Liu', title: '15 Years Dedicated to Phenolic Resin Manufacturing', p1: 'My name is Liu, based in Hengshui, Hebei. I specialize in the design and manufacture of phenolic resin (Bakelite) mechanical components.', p2: 'Phenolic resin is the world\'s earliest industrialized synthetic polymer material, with excellent heat resistance, electrical insulation, and mechanical strength, widely used in electrical equipment, machinery, automotive, petrochemical, rail transit and other fields.', p3: 'My products cover both standard and custom parts. Standard parts are kept in stock and can ship the same day; custom parts typically take 15-30 days from drawing confirmation to delivery.' },
      ja: { label: '劉さんについて', title: '15年続けるフェノール樹脂部品製造', p1: '河北省衡水在住の劉です。フェノール树脂（ベークライト）機械部品の設計・製造を専門としています。', p2: 'フェノール树脂は世界で初めて工業化された合成高分子材料で、優れた耐熱性、電気絶縁性、機械強度を持ち、電工機器、機械設備自動車部品、石油化学、鉄道交通などに広く使われています。', p3: '標準部品とカスタム部品の両方を扱っています。標準部品は在庫があり、最短当日に発送可能。カスタム部品は図面確認から納品まで通常15~30日です。' },
      ko: { label: 'Liu에 대하여', title: '15년 페놀 수지 부품 제조 전문', p1: '호베이성 헝수이에서 온 리우입니다. 페놀 수지（베이클라이트）기계 부품의 설계 및 제조를 전문으로 합니다.', p2: '페놀 수지는 세계에서 가장 먼저 산업화된 합성 고분자 소재로, 우수한 내열성, 전기 절연성, 기계적 강도를 갖추고 있습니다.', p3: '표준 부품과 맞춤 부품을 모두 생산합니다. 표준 부품은 재고 있어 당일 출고 가능, 맞춤 부품은 도면 확인 후 15~30일 이내에 출고합니다.' },
      ru: { label: 'О Лю', title: '15 лет производства фенольных смол', p1: 'Меня зовут Лю, из Хэншуэй, провинция Хэбэй. Специализируюсь на проектировании и производстве механических деталей из фенольной смолы (бакелита).', p2: 'Фенольная смола — первый в мире промышленный синтетический полимер с превосходной термостойкостью, электроизоляцией и механической прочностью.', p3: 'Произвожу как стандартные, так и нестандартные детали. Стандартные детали в наличии, отгрузка в день заказа; нестандартные — 15-30 дней.' },
      es: { label: 'Acerca de Liu', title: '15 anos en fabricacion de resinas fenolicas', p1: 'Me llamo Liu, de Hengshui, Hebei. Me especializo en el diseno y fabricacion de componentes mecanicos de resina fenolica (baquelita).', p2: 'La resina fenolica es el primer polimero sintetico industrializado del mundo, con excelente resistencia al calor, aislamiento electrico y resistencia mecanica.', p3: 'Produzco piezas estandar y personalizadas. Las estandar se envian el mismo dia; las personalizadas tardan 15-30 dias desde la confirmacion del diseno.' },
      fr: { label: 'A propos de Liu', title: '15 ans de fabrication de resines phenoliques', p1: 'Je m\'appelle Liu, de Hengshui, Hebei. Je me specialise dans la conception et la fabrication de composants mecaniques en resine phenolique (bakelite).', p2: 'La resine phenolique est le premier polymere synthétique industrielle au monde, avec une excellente resistance a la chaleur, isolation electrique et resistance mecanique.', p3: 'Je produis des pieces standard et sur mesure. Les standard sont en stock, expedition le jour meme; les sur mesure prennent 15-30 jours.' },
      it: { label: 'Chi e Liu', title: '15 anni di produzione di resine fenoliche', p1: 'Mi chiamo Liu, di Hengshui, Hebei. Mi occupo di progettazione e produzione di componenti meccanici in resina fenolica (bachelite).', p2: 'La resina fenolica e il primo polimero sintetico industrializzato al mondo, con eccellente resistenza termica, isolamento elettrico e resistenza meccanica.', p3: 'Produco componenti standard e personalizzati. Gli standard sono a magazzino, spedizione in giornata; i personalizzati richiedono 15-30 giorni.' },
      th: { label: 'เกี่ยวกับลิว', title: '15 ปีในการผลิตชิ้นส่วนเรซิ่นฟีนอล', p1: 'ผมชื่อลิว จากเหอซุย มณฑลเหอเปย์ ผมเชี่ยวชาญด้านการออกแบบและผลิตชิ้นส่วนเครื่องจักรจากเรซิ่นฟีนอล（เบคคาไลต์）', p2: 'เรซิ่นฟีนอลคือวัสดุพอลิเมอร์สังเคราะห์ที่ผลิตในอุตสาหกรรมเป็นรายแรกของโลก มีความต้านทานความร้อน ฉนวนไฟฟ้า และความแข็งแรงที่ยอดเยี่ยม', p3: 'ผลิตภัณฑ์ครอบคลุมทั้งชิ้นส่วนมาตรฐานและชิ้นส่วนกำหนดเอง ชิ้นส่วนมาตรฐานส่งได้วันเดียว ชิ้นส่วนกำหนดเองใช้เวลา 15-30 วัน' },
      vi: { label: 'Ve Liu', title: '15 nam san xuat linh kien nhua fenol', p1: 'Toi ten Liu, den tu Hengshui, Hebei. Toi chuyen ve thiet ke va san xuat cac linh kien co khi tu nhua fenol (bakelit).', p2: 'Nhua fenol la loai polime toong hop duoc cong nghiep hoa dau tien tren the gioi, co tinh chiu nhiet, cach dien va cuong do co hoc xuat sac.', p3: 'San pham cua toi bao gom chi tiet tieu chuan va chi tiet tuy chinh. Chi tiet tieu chuan co san trong kho, gui hang cung ngay; chi tiet tuy chinh mat 15-30 ngay.' },
    },
    products: {
      zh: { title: '主营产品', desc: '广泛应用于机床、电气设备、石油化工、轨道交通等领域的酚醛树脂配件', items: [{n:'胶木手轮',d:'标准DIN 950，φ40~320mm，耐温130°C'}, {n:'胶木把手',d:'圆头/锥头/星型，M3~M24全系列'}, {n:'胶木手柄',d:'十字/一字/T型，耐磨耐油'}, {n:'油镜/油标',d:'钢化玻璃，耐压1.6MPa'}, {n:'胶木旋钮',d:'刻度盘，φ15~100mm，绝缘E级'}, {n:'非标定制',d:'按图定制，最快15天交付'}] },
      en: { title: 'Main Products', desc: 'Phenolic resin components widely used in machine tools, electrical equipment, petrochemical, rail transit and more', items: [{n:'Bakelite Handwheel',d:'DIN 950 standard, φ40~320mm, 130°C rated'}, {n:'Bakelite Handle',d:'Round/Tapered/Star types, M3~M24 full range'}, {n:'Bakelite Lever Handle',d:'Cross/Flat bar/T-shape, wear and oil resistant'}, {n:'Oil Sight Glass',d:'Tempered glass, 1.6MPa rated'}, {n:'Bakelite Knob & Dial',d:'Dial plates, φ15~100mm, Class E insulation'}, {n:'Custom Parts',d:'Made to drawing, fastest 15-day delivery'}] },
      ja: { title: '主力製品', desc: '工作機械・電気機器・石油化学・鉄道交通などに広く使われるフェノール树脂部品', items: [{n:'ベークライトハンドホイール',d:'DIN 950基準 φ40~320mm 耐温130°C'}, {n:'ベークライトハンドル',d:'丸頭/テーパ/SType M3~M24全種'}, {n:'ベークライトレバー',d:'十字/一字/T型 耐磨耗・耐油性'}, {n:'油量計ガラス',d:'強化ガラス 耐圧1.6MPa'}, {n:'ベークライトノブ',d:'ダイヤル板 φ15~100mm クラスE絶縁'}, {n:'カスタム部品',d:'図面대로製作 最速15日納品'}] },
      ko: { title: '주력 제품', desc: '머신툴, 전기장비, 석유화학, 철도운송 등에 널리 사용되는 베이클라이트 부품', items: [{n:'베이클라이트 핸드휠',d:'DIN 950 기준 φ40~320mm 내열130°C'}, {n:'베이클라이트 핸들',d:'둥근/SType/테이퍼 M3~M24 전 규격'}, {n:'베이클라이트 레버',d:'십자/일자/T형 내마모·내유성'}, {n:'오일_site_glass',d:'강화유리 내압 1.6MPa'}, {n:'베이클라이트 노브',d:'다이얼판 φ15~100mm 클래스E 절연'}, {n:'맞춤 부품',d:'도면 제작 최단 15일 납기'}] },
      ru: { title: 'Основная продукция', desc: 'Бакелитовые детали для станков, электрооборудования, нефтехимии и транспорта', items: [{n:'Бакелитовый маховик',d:'DIN 950, φ40~320мм, до 130°C'}, {n:'Бакелитовая ручка',d:'Круглая/Коническая/Звездочка M3~M24'}, {n:'Бакелитовый рычаг',d:'Крестообразный/Плоский/T-образный'}, {n:'Смотровое стекло',d:'Закаленное стекло, 1.6MPa'}, {n:'Бакелитовый маховик',d:'Шкалы, φ15~100мм, класс E изоляции'}, {n:'Нестандартные детали',d:'По чертежам, 15-30 дней'}] },
      es: { title: 'Productos principales', desc: 'Componentes de baquelita para maquinas herramienta, equipos electricos, petroquimica y transporte', items: [{n:'Volante de baquelita',d:'DIN 950, φ40~320mm, hasta 130°C'}, {n:'Asa de baquelita',d:'Redonda/Conica/Estrella M3~M24'}, {n:'Palanca de baquelita',d:'Cruz/Plana/T-shape, resistente al desgaste'}, {n:'Visor de nivel de aceite',d:'Vidrio templado, 1.6MPa'}, {n:'Pomo de baquelita',d:'Discos de medicion, φ15~100mm, Clase E'}, {n:'Piezas personalizadas',d:'Segun plano, 15-30 dias'}] },
      fr: { title: 'Produits principaux', desc: 'Composants en bakelite pour machines-outils, equipement electrique, petrochimie et transport', items: [{n:'Volant en bakelite',d:'DIN 950, φ40~320mm, jusqu\'a 130°C'}, {n:'Poignee en bakelite',d:'Ronde/Conique/Etoile M3~M24'}, {n:'Levier en bakelite',d:'Croix/Platine/T-shape, resistant'}, {n:'Voyants de niveau d\'huile',d:'Verre trempe, 1.6MPa'}, {n:'Bouton en bakelite',d:'Cadrans, φ15~100mm, Classe E isolation'}, {n:'Pieces personnalisees',d:'Sur plan, 15-30 jours'}] },
      it: { title: 'Prodotti principali', desc: 'Componenti in bachelite per macchinari, apparecchiature elettriche, petrolchimica e trasporti', items: [{n:'Volantino in bachelite',d:'DIN 950, φ40~320mm, fino a 130°C'}, {n:'Impugnatura in bachelite',d:'Rotonda/Conica/Stella M3~M24'}, {n:'Leva in bachelite',d:'Croce/Piatta/T-forma, resistente'}, {n:'Spia livello olio',d:'Vetro temperato, 1.6MPa'}, {n:'Manopola in bachelite',d:'Quadranti, φ15~100mm, Classe E isolamento'}, {n:'Componenti personalizzati',d:'Su disegno, 15-30 giorni'}] },
      th: { title: 'สินค้าหลัก', desc: 'ชิ้นส่วนเบคคาไลต์สำหรับเครื่องจักรกล อุปกรณ์ไฟฟ้า ปิโตรเคมี และระบบขนส่ง', items: [{n:'ล้อมือเบคคาไลต์',d:'DIN 950 φ40~320mm ทนความร้อน 130°C'}, {n:'มือจับเบคคาไลต์',d:'กลม/SType/ทาเปอร์ M3~M24 ทุกขนาด'}, {n:'คันโยกเบคคาไลต์',d:'กากบาท/แบน/T-shape ทนสึก ทนน้ำมัน'}, {n:'กระจกส่องน้ำมัน',d:'กระจกเทมเปอร์ ทนความดัน 1.6MPa'}, {n:'ปุ่มเบคคาไลต์',d:'แผงมาตรวัด φ15~100mm ระดับฉนวน E'}, {n:'ชิ้นส่วนกำหนดเอง',d:'ตามแบบ ส่งเร็วสุด 15 วัน'}] },
      vi: { title: 'San pham chinh', desc: 'Linh kien bakelit cho may cong cu, thiet bi dien, hoa dau va van tai', items: [{n:'Ban sang bakelit',d:'DIN 950 φ40~320mm cho nhiet 130°C'}, {n:'Tay cam bakelit',d:'Tron/SType/Mai M3~M24 day du'}, {n:'Can yo bakelit',d:'Chu thap/Dung phang/T-shape  ben cao'}, {n:'Kinh do muc dau',d:'Kinh temper ben ap luc 1.6MPa'}, {n:'Nut xoay bakelit',d:'Ban quay φ15~100mm cach dien E'}, {n:'Chi tiet tuy chinh',d:'Theo yeu cau, nhanh nhat 15 ngay'}] },
    },
    news: {
      zh: { title: '行业资讯', desc: '技术文章与行业洞察，持续更新' },
      en: { title: 'Industry News', desc: 'Technical articles and industry insights, regularly updated' },
      ja: { title: '業界ニュース', desc: '技術記事と業界動向、 regularly updated' },
      ko: { title: '업계 뉴스', desc: '기술 기사와 업계 동향, 정기 업데이트' },
      ru: { title: 'Новости отрасли', desc: 'Технические статьи и обзоры, регулярное обновление' },
      es: { title: 'Noticias del sector', desc: 'Articulos tecnicos y perspectiva de la industria, actualizacion regular' },
      fr: { title: 'Actualites du secteur', desc: 'Articles techniques et perspectives industrielles, mise a jour reguliere' },
      it: { title: 'Notizie del settore', desc: 'Articoli tecnici e prospettive del settore, aggiornamento regolare' },
      th: { title: 'ข่าวอุตสาหกรรม', desc: 'บทความเทคนิคและข้อมูลเชิงลึกอุตสาหกรรม อัปเดตสม่ำเสมอ' },
      vi: { title: 'Tin nganh', desc: 'Bai viet ky thuat va phan tich nganh, cap nhat deu de' },
    },
    footer: {
      zh: { copyright: '刘的博客 · 分享酚醛树脂配件专业知识和行业经验', addr: '河北省衡水市' },
      en: { copyright: "Liu's Blog · Sharing phenolic resin expertise and industry experience", addr: 'Hengshui, Hebei, China' },
      ja: { copyright: '劉のブログ · フェノール树脂の專業知識と業界経験の共有', addr: '中国河北省衡水市' },
      ko: { copyright: '류의 블로그 · 베이클라이트 전문 지식과 업계 경험 공유', addr: '중국 허베이성 헝수이' },
      ru: { copyright: 'Блог Лю · Обмен опытом по бакелитовым деталям', addr: 'Хэншуэй, Хэбэй, Китай' },
      es: { copyright: 'Blog de Liu · Compartiendo experiencia en piezas de baquelita', addr: 'Hengshui, Hebei, China' },
      fr: { copyright: 'Blog de Liu · Partager l\'expertise en pieces en bakelite', addr: 'Hengshui, Hebei, Chine' },
      it: { copyright: 'Blog di Liu · Condivisione di expertise su componenti in bachelite', addr: 'Hengshui, Hebei, Cina' },
      th: { copyright: 'บล็อกของลิว · แบ่งปันความเชี่ยวชาญด้านเบคคาไลต์', addr: 'เหอซุย มณฑลเหอเปย์ จีน' },
      vi: { copyright: 'Blog cua Liu · Chia se kien thuc ve linh kien bakelit', addr: 'Hengshui, Hebei, Trung Quoc' },
    },
    contact: {
      zh: { label: '联系我们', title: '有任何需求，欢迎随时联系', phone: '电话 / WeChat', email: '邮箱', address: '地址', btn: '发送消息', name: '您的姓名', msg: '请描述您的需求（产品名称、数量、图纸等）' },
      en: { label: 'Contact Us', title: 'Get in touch for any inquiry', phone: 'Phone / WeChat', email: 'Email', address: 'Address', btn: 'Send Message', name: 'Your Name', msg: 'Please describe your requirements (product name, quantity, drawings, etc.)' },
      ja: { label: 'お問い合わせ', title: 'お問い合わせお待ちしています', phone: '電話/WeChat', email: 'メール', address: '住所', btn: '送信', name: 'お名前', msg: '必要事項を記入してください（製品名、数量図面等）' },
      ko: { label: '문의하기', title: '어떤 수요든 편하게 문의주세요', phone: '전화 / WeChat', email: '이메일', address: '주소', btn: '메시지 보내기', name: '성함', msg: '요구를 설명해주세요（제품명, 수량, 도면 등）' },
      ru: { label: 'Свяжитесь с нами', title: 'Напишите нам по любому вопросу', phone: 'Телефон / WeChat', email: 'Email', address: 'Адрес', btn: 'Отправить', name: 'Ваше имя', msg: 'Опишите ваши требования (название товара, количество, чертежи и т.д.)' },
      es: { label: 'Contactenos', title: 'Estamos a su disposicion para cualquier consulta', phone: 'Telefono / WeChat', email: 'Correo', address: 'Direccion', btn: 'Enviar mensaje', name: 'Su nombre', msg: 'Describa sus necesidades (nombre del producto, cantidad, planos, etc.)' },
      fr: { label: 'Contactez-nous', title: 'Nous sommes a votre disposition pour toute demande', phone: 'Telephone / WeChat', email: 'Email', address: 'Adresse', btn: 'Envoyer', name: 'Votre nom', msg: 'Decrivez votre besoin (nom du produit, quantite, plans, etc.)' },
      it: { label: 'Contattaci', title: 'Per qualsiasi esigenza, non esitate a contattarci', phone: 'Telefono / WeChat', email: 'Email', address: 'Indirizzo', btn: 'Invia messaggio', name: 'Il tuo nome', msg: 'Descrivi la tua richiesta (nome prodotto, quantita, disegni, ecc.)' },
      th: { label: 'ติดต่อเรา', title: 'ยินดีตอบทุกคำถาม', phone: 'โทร / WeChat', email: 'อีเมล', address: 'ที่อยู่', btn: 'ส่งข้อความ', name: 'ชื่อของคุณ', msg: 'อธิบายความต้องการของคุณ（ชื่อสินค้า จำนวน แบบ ฯลฯ）' },
      vi: { label: 'Lien he chung toi', title: 'Moi nhu cau deu duoc hoan tra loi', phone: 'Dien thoai / WeChat', email: 'Email', address: 'Dia chi', btn: 'Gui tin nhan', name: 'Ten cua ban', msg: 'Mieu ta yeu cau cua ban（ten san pham, so luong, ban ve, v.v.）' },
    },
    articles: {
      zh: [
        {title: '酚醛树脂配件入门：材料特性、优势与应用场景', category: '入门手册', date: '2026-04-10', readtime: '10min', cta: '阅读 →'},
        {title: '如何为你的应用选择合适的酚醛树脂型号', category: '选型指南', date: '2026-04-12', readtime: '8min', cta: '阅读 →'},
        {title: '酚醛树脂注塑模具设计要点：浇口、流道与冷却系统', category: '技术深潜', date: '2026-04-14', readtime: '12min', cta: '阅读 →'},
        {title: '酚醛树脂配件质检方法：尺寸、外观、功能三维度检验', category: '技术深潜', date: '2026-04-16', readtime: '8min', cta: '阅读 →'},
        {title: '酚醛树脂配件行业应用案例：从石油钻井到轨道交通', category: '行业观察', date: '2026-04-16', readtime: '9min', cta: '阅读 →'},
        {title: '非标定制酚醛树脂配件：如何与工厂高效沟通需求', category: '行业观察', date: '2026-04-16', readtime: '7min', cta: '阅读 →'},
      ],
      en: [
        {title: 'Getting Started with Phenolic Resin Components: Material Properties and Applications', category: 'Getting Started', date: '2026-04-10', readtime: '10min', cta: 'Read →'},
        {title: 'How to Choose the Right Phenolic Resin Grade for Your Application', category: 'Selection Guide', date: '2026-04-12', readtime: '8min', cta: 'Read →'},
        {title: 'Phenolic Resin Injection Mold Design: Gates, Runners and Cooling Systems', category: 'Technical Deep-Dive', date: '2026-04-14', readtime: '12min', cta: 'Read →'},
        {title: 'Quality Control Methods for Phenolic Resin Parts: Three-Dimension Inspection', category: 'Technical Deep-Dive', date: '2026-04-16', readtime: '8min', cta: 'Read →'},
        {title: 'Industry Application Cases: From Oil Drilling to Rail Transit', category: 'Industry Insights', date: '2026-04-16', readtime: '9min', cta: 'Read →'},
        {title: 'Custom Phenolic Resin Parts: How to Communicate Requirements Efficiently with Factories', category: 'Industry Insights', date: '2026-04-16', readtime: '7min', cta: 'Read →'},
      ],
      ja: [
        {title: 'フェノール树脂部品の入门：材料特性、メリットと応用シーン', category: '入门ガイド', date: '2026-04-10', readtime: '10分', cta: '読む →'},
        {title: '用途に合ったフェノール树脂の型の選び方', category: '選定ガイド', date: '2026-04-12', readtime: '8分', cta: '読む →'},
        {title: 'フェノール树脂射出成形：金口、流路、冷却システムの設計ポイント', category: '技術深掘り', date: '2026-04-14', readtime: '12分', cta: '読む →'},
        {title: 'フェノール树脂部品の品質管理：寸法·外観·機能三維度の検査', category: '技術深掘り', date: '2026-04-16', readtime: '8分', cta: '読む →'},
        {title: '業界応用事例：石油掘削から軌道交通まで', category: '業界動向', date: '2026-04-16', readtime: '9分', cta: '読む →'},
        {title: '非標定制フェノール树脂部品：工場との高效なコミュニケーション方法', category: '業界動向', date: '2026-04-16', readtime: '7分', cta: '読む →'},
      ],
      ko: [
        {title: '페놀 수지 부품 입문：재료 특성, 장점 및 응용シーン', category: '입문 가이드', date: '2026-04-10', readtime: '10분', cta: '읽기 →'},
        {title: '용도에 맞는 페놀 수지 등급 선택 방법', category: '선택 가이드', date: '2026-04-12', readtime: '8분', cta: '읽기 →'},
        {title: '페놀 수지 사출 금형 설계：게이트, 러너 및 냉각 시스템', category: '기술 심층', date: '2026-04-14', readtime: '12분', cta: '읽기 →'},
        {title: '페놀 수지 부품 품질 관리：치수·외관·기능 3차원 검사', category: '기술 심층', date: '2026-04-16', readtime: '8분', cta: '읽기 →'},
        {title: '업계 적용 사례：석유 시추에서 궤도 교통까지', category: '업계 동향', date: '2026-04-16', readtime: '9분', cta: '읽기 →'},
        {title: '맞춤 페놀 수지 부품：공장과 효율적으로 소통하는 방법', category: '업계 동향', date: '2026-04-16', readtime: '7분', cta: '읽기 →'},
      ],
      ru: [
        {title: 'Начало работы с деталями из фенольной смолы: свойства и применение', category: 'Введение', date: '2026-04-10', readtime: '10мин', cta: 'Читать →'},
        {title: 'Как выбрать подходящую марку фенольной смолы для вашего применения', category: 'Руководство по выбору', date: '2026-04-12', readtime: '8мин', cta: 'Читать →'},
        {title: 'Проектирование литьевых форм для фенольных смол: литники, каналы и охлаждение', category: 'Технические детали', date: '2026-04-14', readtime: '12мин', cta: 'Читать →'},
        {title: 'Контроль качества деталей из фенольной смолы: трехмерный контроль', category: 'Технические детали', date: '2026-04-16', readtime: '8мин', cta: 'Читать →'},
        {title: 'Примеры применения в промышленности: от бурения до железных дорог', category: 'Отраслевые обзоры', date: '2026-04-16', readtime: '9мин', cta: 'Читать →'},
        {title: 'Нестандартные детали из фенольной смолы: как общаться с заводом', category: 'Отраслевые обзоры', date: '2026-04-16', readtime: '7мин', cta: 'Читать →'},
      ],
      es: [
        {title: 'Introduccion a las piezas de resina fenolica: propiedades y aplicaciones', category: 'Guia de inicio', date: '2026-04-10', readtime: '10min', cta: 'Leer →'},
        {title: 'Como elegir el grado correcto de resina fenolica para su aplicacion', category: 'Guia de seleccion', date: '2026-04-12', readtime: '8min', cta: 'Leer →'},
        {title: 'Diseno de moldes de inyeccion para resinas fenolicas: compuertas, canales y enfriamiento', category: 'Detalles tecnicos', date: '2026-04-14', readtime: '12min', cta: 'Leer →'},
        {title: 'Control de calidad de piezas de resina fenolica: inspeccion tridimensional', category: 'Detalles tecnicos', date: '2026-04-16', readtime: '8min', cta: 'Leer →'},
        {title: 'Casos de aplicacion industrial: desde perforacion de petroleo hasta transporte rail', category: 'Perspectivas del sector', date: '2026-04-16', readtime: '9min', cta: 'Leer →'},
        {title: 'Piezas de resina fenolica no estandar: como comunicarse eficientemente con la fabrica', category: 'Perspectivas del sector', date: '2026-04-16', readtime: '7min', cta: 'Leer →'},
      ],
      fr: [
        {title: 'Decouvrir les pieces en resine phenolique: proprietes et applications', category: 'Guide de demarrage', date: '2026-04-10', readtime: '10min', cta: 'Lire →'},
        {title: 'Comment choisir le grade de resine phenolique adapte a votre application', category: 'Guide de selection', date: '2026-04-12', readtime: '8min', cta: 'Lire →'},
        {title: 'Conception de moules d\'injection pour resines phenoliques: attaques, canaux et refroidissement', category: 'Details techniques', date: '2026-04-14', readtime: '12min', cta: 'Lire →'},
        {title: 'Controle qualite des pieces en resine phenolique: inspection tridimensionnelle', category: 'Details techniques', date: '2026-04-16', readtime: '8min', cta: 'Lire →'},
        {title: 'Cas d\'application industrielle: du forage petrolier au transport ferre', category: 'Perspectives sectorielles', date: '2026-04-16', readtime: '9min', cta: 'Lire →'},
        {title: 'Pieces en resine phenolique non standard: comment communiquer efficacement avec l\'usine', category: 'Perspectives sectorielles', date: '2026-04-16', readtime: '7min', cta: 'Lire →'},
      ],
      it: [
        {title: 'Introduzione ai componenti in resina fenolica: proprieta e applicazioni', category: 'Guida introduttiva', date: '2026-04-10', readtime: '10min', cta: 'Leggi →'},
        {title: 'Come scegliere il grado di resina fenolica giusto per la vostra applicazione', category: 'Guida alla selezione', date: '2026-04-12', readtime: '8min', cta: 'Leggi →'},
        {title: 'Progettazione di stampi a iniezione per resine fenoliche: punti di iniezione, canali e raffreddamento', category: 'Dettagli tecnici', date: '2026-04-14', readtime: '12min', cta: 'Leggi →'},
        {title: 'Controllo qualita dei componenti in resina fenolica: ispezione tridimensionale', category: 'Dettagli tecnici', date: '2026-04-16', readtime: '8min', cta: 'Leggi →'},
        {title: 'Casi di applicazione industriale: dalla perforazione petrolifera al trasporto su rotaia', category: 'Prospettive del settore', date: '2026-04-16', readtime: '9min', cta: 'Leggi →'},
        {title: 'Componenti in resina fenolica non standard: come comunicare efficientemente con la fabbrica', category: 'Prospettive del settore', date: '2026-04-16', readtime: '7min', cta: 'Leggi →'},
      ],
      th: [
        {title: 'เริ่มต้นกับชิ้นส่วนเรซิ่นฟีนอล：คุณสมบัติ ข้อดี และการใช้งาน', category: 'คู่มือเริ่มต้น', date: '2026-04-10', readtime: '10นาที', cta: 'อ่าน →'},
        {title: 'วิธีเลือกเกรดเรซิ่นฟีนอลที่เหมาะสมสำหรับการใช้งานของคุณ', category: 'คู่มือการเลือก', date: '2026-04-12', readtime: '8นาที', cta: 'อ่าน →'},
        {title: 'การออกแบบแม่พิมพ์ฉีดเรซิ่นฟีนอล： 게이트, ช่องนำ ระบบระบายความร้อน', category: 'รายละเอียดทางเทคนิค', date: '2026-04-14', readtime: '12นาที', cta: 'อ่าน →'},
        {title: 'การควบคุมคุณภาพชิ้นส่วนเรซิ่นฟีนอล：การตรวจสอบสามมิติ', category: 'รายละเอียดทางเทคนิค', date: '2026-04-16', readtime: '8นาที', cta: 'อ่าน →'},
        {title: 'กรณีศึกษาการใช้งานในอุตสาหกรรม：จากการเจาะน้ำมันถึงระบบขนส่งทางราง', category: 'ข้อมูลเชิงลึกอุตสาหกรรม', date: '2026-04-16', readtime: '9นาที', cta: 'อ่าน →'},
        {title: 'ชิ้นส่วนเรซิ่นฟีนอลที่กำหนดเอง：วิธีสื่อสารกับโรงงานอย่างมีประสิทธิภาพ', category: 'ข้อมูลเชิงลึกอุตสาหกรรม', date: '2026-04-16', readtime: '7นาที', cta: 'อ่าน →'},
      ],
      vi: [
        {title: 'Gioi thieu ve linh kien nhua fenol：Tinh chat, uu diem va ung dung', category: 'Huong dan bat dau', date: '2026-04-10', readtime: '10phut', cta: 'Doc →'},
        {title: 'Cach chon loai nhua fenol phu hop cho ung dung cua ban', category: 'Huong dan chon', date: '2026-04-12', readtime: '8phut', cta: 'Doc →'},
        {title: 'Thiet ke khuon ep nhua fenol：Cua vao, kenh chay va he thong lam nguoi', category: 'Chi tiet ky thuat', date: '2026-04-14', readtime: '12phut', cta: 'Doc →'},
        {title: 'Kiem soat chat luong linh kien nhua fenol：Kiem tra ba chieu', category: 'Chi tiet ky thuat', date: '2026-04-16', readtime: '8phut', cta: 'Doc →'},
        {title: 'Truong hop ung dung nganh：从 khoan dau den van tai rail', category: 'Phan tich nganh', date: '2026-04-16', readtime: '9phut', cta: 'Doc →'},
        {title: 'Linh kien nhua fenol tuy chinh：Cach giao tiep hieu qua voi nha may', category: 'Phan tich nganh', date: '2026-04-16', readtime: '7phut', cta: 'Doc →'},
      ],
    },
  };

  /* ── 12. applyI18n — 页面翻译 ────────────────────────────────────── */
  function applyI18n(lang) {
    lang = lang || getLang();
    var t = I18N;
    if (!t) return;

    // Hero section
    var heroLabel = document.querySelector('.hero-badge-label');
    if (heroLabel && t.hero && t.hero[lang]) {
      var hero = t.hero[lang];
      heroLabel.textContent = hero.label;
      var heroTitle = document.querySelector('.hero-title');
      if (heroTitle) heroTitle.innerHTML = (hero.title || '').replace(/\n/g, '<br>');
      var heroSub = document.querySelector('.hero-subtitle');
      if (heroSub) heroSub.textContent = hero.subtitle || '';
      var statsEls = document.querySelectorAll('.hero-stat-value');
      if (statsEls[0]) statsEls[0].textContent = hero.stats1val || '';
      if (statsEls[1]) statsEls[1].textContent = hero.stats2val || '';
      if (statsEls[2]) statsEls[2].textContent = hero.stats3val || '';
      var ctaEls = document.querySelectorAll('.hero-cta .btn');
      if (ctaEls[0]) ctaEls[0].textContent = hero.cta1 || '';
      if (ctaEls[1]) ctaEls[1].textContent = hero.cta2 || '';
    }

    // About section
    if (t.about && t.about[lang]) {
      var about = t.about[lang];
      var aboutLabel = document.querySelector('.about-label');
      if (aboutLabel) aboutLabel.textContent = about.label;
      var aboutTitle = document.querySelector('.about-title');
      if (aboutTitle) aboutTitle.textContent = about.title;
      var aboutPs = document.querySelectorAll('.about-text');
      if (aboutPs[0]) aboutPs[0].textContent = about.p1 || '';
      if (aboutPs[1]) aboutPs[1].textContent = about.p2 || '';
      if (aboutPs[2]) aboutPs[2].textContent = about.p3 || '';
    }

    // Products section
    if (t.products && t.products[lang]) {
      var prods = t.products[lang];
      var pTitle = document.querySelector('.products-section .section-title');
      if (pTitle) pTitle.textContent = prods.title;
      var pDesc = document.querySelector('.products-section .section-desc');
      if (pDesc) pDesc.textContent = prods.desc;
      var cards = document.querySelectorAll('.product-card');
      if (cards.length && prods.items) {
        cards.forEach(function(card, i) {
          var nameEl = card.querySelector('.product-name');
          var descEl = card.querySelector('.product-desc');
          if (nameEl && prods.items[i]) nameEl.textContent = prods.items[i].n;
          if (descEl && prods.items[i]) descEl.textContent = prods.items[i].d;
        });
      }
    }

    // News section
    if (t.news && t.news[lang]) {
      var news = t.news[lang];
      var nLabel = document.querySelector('#news .section-label');
      if (nLabel) nLabel.textContent = '博客文章';
      var nTitle = document.querySelector('#news .section-title');
      if (nTitle) nTitle.textContent = news.title;
      var nDesc = document.querySelector('#news .section-desc');
      if (nDesc) nDesc.textContent = news.desc;
    }

    // News cards
    if (t.articles && t.articles[lang]) {
      var articles = t.articles[lang];
      var cards = document.querySelectorAll('.news-card');
      cards.forEach(function(card, i) {
        if (!articles[i]) return;
        var a = articles[i];
        var cat = card.querySelector('.news-card-category');
        var title = card.querySelector('.news-card-title');
        var date = card.querySelector('.news-card-date');
        var cta = card.querySelector('.news-card-cta');
        if (cat) cat.textContent = a.category;
        if (title) title.textContent = a.title;
        if (date) date.textContent = a.date;
        if (cta) cta.textContent = a.cta;
      });
    }

    // Footer
    if (t.footer && t.footer[lang]) {
      var footer = t.footer[lang];
      var copyEl = document.querySelector('.footer-copy');
      if (copyEl) copyEl.textContent = footer.copyright;
      var addrEl = document.querySelector('.footer-addr');
      if (addrEl) addrEl.textContent = footer.addr;
    }

    // Contact section
    if (t.contact && t.contact[lang]) {
      var ctc = t.contact[lang];
      var cLabel = document.querySelector('#contact .section-label');
      if (cLabel) cLabel.textContent = ctc.label;
      var cTitle = document.querySelector('#contact .section-title');
      if (cTitle) cTitle.textContent = ctc.title;
    }

    // Update document title
    if (t.hero && t.hero[lang]) {
      document.title = t.hero[lang].label + ' | 刘的博客';
    }
  }


  init();

  /* ── 12. Hero背景图懒加载 ─────────────────────────────────────── */
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