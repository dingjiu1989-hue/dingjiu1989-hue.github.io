(function () {
  'use strict';

  var input = document.getElementById('search-input');
  if (!input) return;

  var results = document.getElementById('search-results');
  var articles = [];
  var boards = {};
  var selectedIndex = -1;

  // Board name mapping (mirrors BOARD_NAMES_EN)
  var boardNames = {
    'daily': 'AI Daily Digest',
    'tech': 'Tech Tutorials',
    'sidehustle': 'Side Hustle Guides',
    'tools': 'Tool Recommendations',
    'ai': 'AI & LLM Tutorials',
    'compare': 'Tool Comparisons',
    'security': 'Security Guides',
    'database': 'Database Tutorials',
    'architecture': 'Architecture Patterns'
  };

  function loadData() {
    var req = new XMLHttpRequest();
    req.open('GET', '/en/articles.json?' + Date.now());
    req.onload = function () {
      try {
        var data = JSON.parse(req.responseText);
        for (var i = 0; i < data.boards.length; i++) {
          var b = data.boards[i];
          var boardName = boardNames[b.id] || b.name || b.id;
          for (var j = 0; j < b.posts.length; j++) {
            var a = b.posts[j];
            articles.push({
              title: a.title,
              description: a.description || '',
              tags: (a.tags || []).join(', '),
              slug: a.slug,
              board: b.id,
              boardName: boardName,
              date: a.date,
              replies: a.replies || 0
            });
          }
        }
      } catch (e) {
        console.error('Search data parse error:', e);
      }
    };
    req.send();
  }
  loadData();

  function matchText(text, query) {
    if (!text) return false;
    return text.toLowerCase().indexOf(query) > -1;
  }

  function doSearch(query) {
    if (!query || query.length < 2) return [];
    var q = query.toLowerCase();
    var results = [];
    for (var i = 0; i < articles.length; i++) {
      var a = articles[i];
      if (matchText(a.title, q) ||
          matchText(a.description, q) ||
          matchText(a.tags, q) ||
          matchText(a.boardName, q)) {
        results.push(a);
        if (results.length >= 20) break;
      }
    }
    return results;
  }

  function renderResults(items) {
    selectedIndex = -1;
    if (items.length === 0) {
      results.innerHTML = '<div class="search-no-results">No articles found</div>';
      results.classList.add('active');
      return;
    }
    var html = '';
    for (var i = 0; i < items.length; i++) {
      var a = items[i];
      var icon = a.board === 'daily' ? '📰' : a.board === 'sidehustle' ? '💼' : '📄';
      html += '<div class="search-result-item" data-index="' + i + '" data-slug="' + a.slug + '" data-board="' + a.board + '">' +
        '<div class="search-result-title">' + esc(a.title) + '</div>' +
        '<div class="search-result-meta">' + icon + ' ' + esc(a.boardName) + ' · ' + a.date + ' · ' + a.replies + ' replies</div>' +
        (a.description ? '<div class="search-result-desc">' + esc(a.description.substring(0, 120)) + '</div>' : '') +
        '</div>';
    }
    results.innerHTML = html;
    results.classList.add('active');

    // Click handler
    var resultEls = results.querySelectorAll('.search-result-item');
    for (var k = 0; k < resultEls.length; k++) {
      resultEls[k].addEventListener('click', function () {
        goToArticle(this.getAttribute('data-slug'), this.getAttribute('data-board'));
      });
    }
  }

  function esc(s) {
    if (!s) return '';
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function goToArticle(slug, board) {
    window.location.href = '/en/' + board + '/' + slug + '.html';
  }

  function highlightNext() {
    var items = results.querySelectorAll('.search-result-item');
    if (items.length === 0) return;
    if (selectedIndex >= 0) items[selectedIndex].classList.remove('highlighted');
    selectedIndex = Math.min(selectedIndex + 1, items.length - 1);
    items[selectedIndex].classList.add('highlighted');
    items[selectedIndex].scrollIntoView({ block: 'nearest' });
  }

  function highlightPrev() {
    var items = results.querySelectorAll('.search-result-item');
    if (items.length === 0) return;
    if (selectedIndex >= 0) items[selectedIndex].classList.remove('highlighted');
    selectedIndex = Math.max(selectedIndex - 1, 0);
    items[selectedIndex].classList.add('highlighted');
    items[selectedIndex].scrollIntoView({ block: 'nearest' });
  }

  function selectHighlighted() {
    var items = results.querySelectorAll('.search-result-item');
    if (selectedIndex >= 0 && selectedIndex < items.length) {
      var el = items[selectedIndex];
      goToArticle(el.getAttribute('data-slug'), el.getAttribute('data-board'));
    }
  }

  // Event listeners
  var debounceTimer;
  input.addEventListener('input', function () {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(function () {
      var query = input.value.trim();
      if (query.length < 2) {
        results.classList.remove('active');
        return;
      }
      var matches = doSearch(query);
      renderResults(matches);
    }, 200);
  });

  input.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      highlightNext();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      highlightPrev();
    } else if (e.key === 'Enter') {
      e.preventDefault();
      selectHighlighted();
    } else if (e.key === 'Escape') {
      results.classList.remove('active');
      input.blur();
    }
  });

  // Close on outside click
  document.addEventListener('click', function (e) {
    if (!input.contains(e.target) && !results.contains(e.target)) {
      results.classList.remove('active');
    }
  });
})();
