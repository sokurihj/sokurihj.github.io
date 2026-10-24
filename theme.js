// 낮·밤 모드 — 머리말에서 먼저 읽어 <html data-theme>을 정하고(그려지기 전이라 깜빡이지 않는다),
// 문서가 다 읽히면 머리말에 전환 버튼을 붙인다. 처음 온 사람은 기기 설정을 따르고, 버튼을 누르면 그 선택을 기억한다.
// 약관·처리방침 같은 옛 정적 페이지는 이 파일 한 줄만 넣으면 버튼까지 같이 생긴다.
(function () {
  var KEY = 'theme';
  var root = document.documentElement;
  var LABEL = { ko: '다크 모드', en: 'Dark mode', ja: 'ダークモード' };

  function saved() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  var theme = saved() || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  root.setAttribute('data-theme', theme);

  document.addEventListener('DOMContentLoaded', function () {
    var nav = document.querySelector('.nav nav');
    if (!nav) return;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'theme-btn';
    btn.setAttribute('role', 'switch');
    btn.setAttribute('aria-label', LABEL[root.lang] || LABEL.en);
    btn.innerHTML =
      '<span class="knob">' +
      '<svg class="moon" viewBox="0 0 24 24"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>' +
      '<svg class="sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>' +
      '</span>';
    function paint() { btn.setAttribute('aria-checked', root.getAttribute('data-theme') === 'dark'); }
    btn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem(KEY, next); } catch (e) { /* 저장이 막혀도 이번 방문에는 바뀐다 */ }
      paint();
    });
    paint();
    nav.insertBefore(btn, nav.querySelector('.langs')); // 언어 줄이 없는 약관 페이지에서는 null이라 맨 뒤에 붙는다
  });
})();
