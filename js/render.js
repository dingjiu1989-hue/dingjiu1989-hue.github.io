// Consistent view calculation matching the server-side formula
function calcViews(replies, slug) {
  var seed = 0;
  for (var i = 0; i < slug.length; i++) { seed += slug.charCodeAt(i); }
  return 50 + (seed % 200) + ((replies || 0) * 120);
}

// Render homepage stats bar and hero stats
function renderStats(data) {
  var boards = data.boards || [];
  var totalBoards = boards.length;
  var totalPosts = 0;
  boards.forEach(function (b) { totalPosts += (b.posts || []).length; });

  var heroStats = document.getElementById('hero-stats');
  if (heroStats) {
    heroStats.innerHTML =
      '<span class="hero-stat">📂 ' + totalBoards + ' boards</span>' +
      '<span class="hero-stat">📝 ' + totalPosts + ' articles</span>';
  }

  var statsBar = document.getElementById('stats-bar');
  if (statsBar) {
    var s = data.site && data.site.stats;
    if (s) {
      statsBar.innerHTML =
        '<span>🔥 Today: ' + s.today + '</span>' +
        '<span>📅 Yesterday: ' + s.yesterday + '</span>' +
        '<span>📊 Total: ' + s.total + '</span>';
    } else {
      statsBar.innerHTML = '<span>📊 Total: ' + totalPosts + '</span>';
    }
  }

  // Also update post-count spans on category pages
  var allBoardsTotal = 0;
  boards.forEach(function (b) { allBoardsTotal += (b.posts || []).length; });
  var postCounts = document.querySelectorAll('.post-count');
  for (var i = 0; i < postCounts.length; i++) {
    var text = postCounts[i].textContent;
    if (text && text.indexOf('articles') >= 0) {
      postCounts[i].textContent = text.replace(/\d+ articles/, allBoardsTotal + ' articles');
    }
  }
}

function renderHomepage(data) {
  var container = document.getElementById('homepage-boards');
  if (!container) return;
  var boards = data.boards || [];
  var html = '';
  boards.forEach(function (b) {
    html +=
      '<div class="board">' +
      '<div class="board-header">' +
      '<span class="board-icon">' + esc(b.icon) + '</span>' +
      '<span class="board-name">' + esc(b.name) + '</span>' +
      '<span class="board-desc">' + esc(b.desc) + '</span>' +
      '<span class="board-count">' + (b.posts ? b.posts.length : 0) + ' posts</span>' +
      '</div>';
    var posts = b.posts || [];
    posts.forEach(function (p) {
      var url = '/' + b.id + '/' + p.slug + '.html';
      var pinClass = '';
      var pinIcon = '';
      if (p.pinned) { pinClass = ' pinned'; pinIcon = '📌'; }
      else if (p.hot || (p.replies || 0) >= 20) { pinClass = ' hot'; pinIcon = '🔥'; }
      var views = calcViews(p.replies, p.slug);
      var badge = (p.replies || 0) > 0 ? '<span class="reply-badge">' + (p.replies || 0) + '</span>' : '';
      html +=
        '<a href="' + esc(url) + '" class="post-row">' +
        '<span class="post-pin' + pinClass + '">' + pinIcon + '</span>' +
        '<span class="post-title">' + esc(p.title) + badge + '</span>' +
        '<span class="post-replies">' + views + ' views</span>' +
        '<span class="post-date">' + esc(p.date.substring(5)) + '</span>' +
        '</a>';
    });
    html += '</div>';
  });
  container.innerHTML = html;
}

// Render category page post table
function renderCategory(data, boardId) {
  var container = document.getElementById('category-posts');
  if (!container) return;
  var board;
  var boards = data.boards || [];
  for (var i = 0; i < boards.length; i++) {
    if (boards[i].id === boardId) { board = boards[i]; break; }
  }
  if (!board) return;
  var posts = board.posts || [];
  var html =
    '<div class="post-table">' +
    '<div class="post-table-header">' +
    '<span class="col-pin"></span>' +
    '<span class="col-title">Title</span>' +
    '<span class="col-replies">Views</span>' +
    '<span class="col-date">Date</span>' +
    '</div>';
  posts.forEach(function (p) {
    var url = '/' + boardId + '/' + p.slug + '.html';
    var pinStyle = '';
    var pinMark = '';
    if (p.pinned) { pinMark = '📌'; pinStyle = ' style="color:#d73a49;"'; }
    else if (p.hot || (p.replies || 0) >= 20) { pinMark = '🔥'; pinStyle = ' style="color:#d73a49;"'; }
    var titleStyle = p.pinned ? ' style="font-weight:600;"' : '';
    var views = calcViews(p.replies, p.slug);
    var badge = (p.replies || 0) > 0 ? '<span class="reply-badge">' + (p.replies || 0) + '</span>' : '';
    html +=
      '<a href="' + esc(url) + '" class="post-row">' +
      '<span class="col-pin"' + pinStyle + '>' + pinMark + '</span>' +
      '<span class="col-title"' + titleStyle + '>' + esc(p.title) + badge + '</span>' +
      '<span class="col-replies">' + views + '</span>' +
      '<span class="col-date">' + esc(p.date.substring(5)) + '</span>' +
      '</a>';
  });
  html += '</div>';
  container.innerHTML = html;
}

// Render related posts on article pages
function renderRelated(data, boardId, excludeSlug) {
  var grid = document.querySelector('.related-grid');
  if (grid && grid.children.length > 0) return;
  var container = document.getElementById('related-posts');
  if (!container) { container = document.createElement('div'); }
  else { container.style.display = ''; }
  var posts = [];
  var boards = data.boards || [];
  for (var i = 0; i < boards.length; i++) {
    var bp = boards[i].posts || [];
    for (var j = 0; j < bp.length; j++) {
      if (bp[j].slug !== excludeSlug) {
        posts.push({ post: bp[j], boardId: boards[i].id });
      }
    }
  }
  var same = [];
  var other = [];
  for (var k = 0; k < posts.length; k++) {
    if (posts[k].boardId === boardId) same.push(posts[k]);
    else other.push(posts[k]);
  }
  var picked = same.concat(other).slice(0, 4);
  if (picked.length === 0) return;
  var html = '<h3>Related Articles</h3><div class="related-grid">';
  picked.forEach(function (item) {
    var url = '/' + item.boardId + '/' + item.post.slug + '.html';
    html += '<a href="' + esc(url) + '" class="related-card">' + esc(item.post.title) + '</a>';
  });
  html += '</div>';
  container.innerHTML = html;
}

function esc(s) {
  if (!s) return '';
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// Reading progress bar
function initProgressBar() {
  var bar = document.getElementById('reading-progress-bar');
  if (!bar) return;
  function update() {
    var scrollTop = window.scrollY || document.documentElement.scrollTop;
    var docHeight = document.documentElement.scrollHeight - window.innerHeight;
    if (docHeight > 0) {
      bar.style.width = Math.min(100, (scrollTop / docHeight) * 100) + '%';
    }
  }
  window.addEventListener('scroll', update, { passive: true });
  update();
}

// Back-to-top button
function initBackToTop() {
  var btn = document.getElementById('back-to-top');
  if (!btn) return;
  window.addEventListener('scroll', function () {
    if (window.scrollY > 400) { btn.classList.add('visible'); }
    else { btn.classList.remove('visible'); }
  }, { passive: true });
  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// Copy link button
function initCopyLink() {
  document.querySelectorAll('.copy-link-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var url = btn.getAttribute('data-url');
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(function () {
          btn.textContent = 'Copied!';
          btn.classList.add('copied');
          setTimeout(function () {
            btn.textContent = 'Copy';
            btn.classList.remove('copied');
          }, 2000);
        });
      }
    });
  });
}

// Lazy-load Giscus via IntersectionObserver
function initGiscus() {
  var section = document.getElementById('giscus-section');
  if (!section) return;
  if (section.getAttribute('data-giscus-loaded') === 'true') return;
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      observer.disconnect();
      section.setAttribute('data-giscus-loaded', 'true');
      var script = document.createElement('script');
      script.src = 'https://giscus.app/client.js';
      script.setAttribute('data-repo', 'dingjiu1989-hue/dingjiu1989-hue.github.io');
      script.setAttribute('data-repo-id', 'R_kgDOSWcDOw');
      script.setAttribute('data-category', 'Announcements');
      script.setAttribute('data-category-id', 'DIC_kwDOSWcDO84C9bsh');
      script.setAttribute('data-mapping', 'pathname');
      script.setAttribute('data-strict', '1');
      script.setAttribute('data-reactions-enabled', '1');
      script.setAttribute('data-emit-metadata', '0');
      script.setAttribute('data-input-position', 'top');
      script.setAttribute('data-theme', 'light');
      script.setAttribute('data-lang', 'en');
      script.crossOrigin = 'anonymous';
      script.async = true;
      section.appendChild(script);
    });
  }, { rootMargin: '200px' });
  observer.observe(section);
}

// Load articles.json and auto-detect rendering type
(function () {
  var type = document.documentElement.getAttribute('data-render');
  if (!type) return;
  var base = document.querySelector('meta[name="base-path"]');
  var prefix = base ? base.content : '';
  var xhr = new XMLHttpRequest();
  xhr.open('GET', prefix + '/articles.json', true);
  xhr.onload = function () {
    if (xhr.status < 200 || xhr.status >= 300) return;
    var data = JSON.parse(xhr.responseText);
    if (type === 'homepage')      { renderStats(data); renderHomepage(data); }
    if (type === 'category')      renderCategory(data, document.documentElement.getAttribute('data-board'));
    if (type === 'related')       renderRelated(data, document.documentElement.getAttribute('data-board'), document.documentElement.getAttribute('data-exclude'));
  };
  xhr.send();

  // Engagement features (only on article pages)
  if (type === 'related') {
    // Run after a small delay to avoid competing with articles.json load
    setTimeout(function () {
      initProgressBar();
      initBackToTop();
      initCopyLink();
      initGiscus();
    }, 100);
  }
})();
