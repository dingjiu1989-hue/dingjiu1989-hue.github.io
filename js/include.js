// Load shared nav and footer into current page
// Language-aware: loads /en/nav.html for English pages, /nav.html for Chinese

(function () {
  var base = document.querySelector('meta[name="base-path"]');
  var prefix = base ? base.content : '';
  var isEn = prefix === '/en';

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
