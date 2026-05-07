// Load shared nav and footer into current page
// Language-aware: loads /en/nav.html for English pages, /nav.html for Chinese
// Injects GA4 on Chinese pages (English pages have it in <head>)

(function () {
  var base = document.querySelector('meta[name="base-path"]');
  var prefix = base ? base.content : '';
  var isEn = prefix === '/en';

  // Inject GA4 on Chinese pages (English pages have static GA4 in <head>)
  if (!isEn && !document.querySelector('script[src*="googletagmanager"]')) {
    var ga = document.createElement('script');
    ga.async = true;
    ga.src = 'https://www.googletagmanager.com/gtag/js?id=G-XGFYGQE9NS';
    document.head.appendChild(ga);
    var gtag = document.createElement('script');
    gtag.text = 'window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-XGFYGQE9NS");';
    document.head.appendChild(gtag);
  }

  function load(id, file) {
    var el = document.getElementById(id);
    if (!el) return;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', file, true);
    xhr.onload = function () {
      if (xhr.status >= 200 && xhr.status < 300) {
        el.innerHTML = xhr.responseText;
      }
    };
    xhr.send();
  }

  // Load language-specific nav
  if (isEn) {
    load('nav-placeholder', '/en/nav.html');
  } else {
    load('nav-placeholder', '/nav.html');
  }
  load('footer-placeholder', '/footer.html');
})();
