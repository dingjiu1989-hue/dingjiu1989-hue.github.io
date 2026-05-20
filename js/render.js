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
      var views = (p.replies || 0) * 120;
      html +=
        '<a href="' + esc(url) + '" class="post-row">' +
        '<span class="post-pin' + pinClass + '">' + pinIcon + '</span>' +
        '<span class="post-title">' + esc(p.title) + '</span>' +
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
    var views = (p.replies || 0) * 120;
    html +=
      '<a href="' + esc(url) + '" class="post-row">' +
      '<span class="col-pin"' + pinStyle + '>' + pinMark + '</span>' +
      '<span class="col-title"' + titleStyle + '>' + esc(p.title) + '</span>' +
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
})();
