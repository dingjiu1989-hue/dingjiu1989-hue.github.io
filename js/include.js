// Load shared nav and footer into current page
// Usage: add <div id="nav-placeholder"></div> and <div id="footer-placeholder"></div> to pages

(function () {
  var base = document.querySelector('meta[name="base-path"]');
  var prefix = base ? base.content : '';

  function load(id, file) {
    var el = document.getElementById(id);
    if (!el) return;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', prefix + file, true);
    xhr.onload = function () {
      if (xhr.status >= 200 && xhr.status < 300) {
        el.innerHTML = xhr.responseText;
      }
    };
    xhr.send();
  }

  load('nav-placeholder', '/nav.html');
  load('footer-placeholder', '/footer.html');
})();
