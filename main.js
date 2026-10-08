// 냥냥비트 사이트의 움직임 — ① 고정 머리말 밑줄 ② 고른 앱 폴라로이드 뒤로 빼꼼하는 고양이 ③ 발자국(PC 마우스·폰 스크롤).
// 내용은 HTML에 이미 있고(build.py가 언어별로 만든다), 여기서는 동작만 붙인다.

const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

// ── 머리말: 내용 위로 스크롤되면 아래 선을 그어 경계를 보인다 ──
const nav = document.querySelector('.nav');
const onScrollNav = () => nav.classList.toggle('scrolled', scrollY > 8);
addEventListener('scroll', onScrollNav, { passive: true });
onScrollNav();

// ── 빼꼼: 앞 카드 뒤로 쏙 숨었다가, 고른 폴라로이드 윗변 뒤에서 얼굴과 손만 내민다 ──
// 그림 한 장(모아냥 고양이)으로 하려고 아래 절반은 카드에 가려지게 둔다 — 점프는 포즈가 하나라 스티커가 나는 것처럼 어색했다.
document.querySelectorAll('.cards').forEach((wrap) => {
  const sitter = wrap.querySelector('.sitter');
  const cards = [...wrap.querySelectorAll('.card')];
  let seat = null;
  function spotFor(card) {
    const box = wrap.getBoundingClientRect();
    const r = card.getBoundingClientRect();
    const w = sitter.offsetWidth, h = sitter.offsetHeight;
    return { x: r.left - box.left + r.width * 0.68 - w / 2, y: r.top - box.top - h * 0.5, hide: h * 0.6 };
  }
  const at = (p, dy = 0) => `translate(${p.x}px, ${p.y + dy}px)`;
  function peekAt(card, first = false) {
    if (!card || (seat === card && !first)) return;
    const from = seat && !first ? spotFor(seat) : null;
    seat = card;
    const to = spotFor(card);
    sitter.getAnimations().forEach((a) => a.cancel());
    sitter.style.transform = at(to);
    if (reduced) return;
    const frames = from ? [{ transform: at(from) }, { transform: at(from, from.hide), offset: 0.3 }] : [];
    frames.push({ transform: at(to, to.hide), offset: from ? 0.31 : 0 }, { transform: at(to, -5), offset: 0.85 }, { transform: at(to) });
    sitter.animate(frames, { duration: from ? 640 : 520, easing: 'ease-out' });
  }
  cards.forEach((card) => {
    card.addEventListener('pointerenter', (e) => { if (e.pointerType === 'mouse') peekAt(card); });
    card.addEventListener('focus', () => peekAt(card));
  });
  addEventListener('resize', () => { if (seat) sitter.style.transform = at(spotFor(seat)); });
  // 그림 크기를 알아야 자리를 계산할 수 있다.
  const start = () => peekAt(cards[0], true);
  sitter.complete ? start() : sitter.addEventListener('load', start, { once: true });
});

// ── 발자국 ──
const PAW = '<svg viewBox="0 0 24 24"><ellipse cx="12" cy="15.5" rx="5.6" ry="4.8"/><circle cx="5.2" cy="9.6" r="2.3"/><circle cx="9.4" cy="5.6" r="2.4"/><circle cx="14.6" cy="5.6" r="2.4"/><circle cx="18.8" cy="9.6" r="2.3"/></svg>';
function paw(x, y, deg) {
  const el = document.createElement('span');
  el.className = 'paw';
  el.innerHTML = PAW;
  el.style.left = x - 10 + 'px';
  el.style.top = y - 10 + 'px';
  el.style.setProperty('--t', `rotate(${deg}deg)`);
  document.body.appendChild(el);
  el.addEventListener('animationend', () => el.remove());
}

// PC: 빈 바탕을 지나간 마우스 자리에 왼발·오른발 번갈아 찍는다(카드·글자·그림 위에서는 안 찍는다).
let last = null, side = 1;
addEventListener('pointermove', (e) => {
  if (e.pointerType !== 'mouse' || reduced) return;
  if (e.target.closest('.card, .shot, .hero-pol, .ways li, .say, a, button, h1, h2, h3, p, li, table, .nav, .big')) { last = null; return; }
  const x = e.pageX, y = e.pageY;
  if (!last) { last = { x, y }; return; }
  const dx = x - last.x, dy = y - last.y;
  if (Math.hypot(dx, dy) < 44) return;
  const ang = Math.atan2(dy, dx);
  side = -side;
  paw(x - Math.sin(ang) * 8 * side, y + Math.cos(ang) * 8 * side, ang * 180 / Math.PI + 90);
  last = { x, y };
});

// 폰: 손가락을 따라가면 안 된다 — 쓸어내리면 페이지도 같이 움직여 페이지 기준 손가락 위치가 거의 그대로고,
// 손을 뗀 뒤 미끄러지는 스크롤 동안엔 터치 신호가 아예 안 온다(실기기에서 1개만 찍히거나 들쭉날쭉했다).
// 대신 스크롤한 거리만큼 고양이가 화면 오른쪽(스크롤 막대 쪽) 여백을 따라 걸어간 것처럼 찍는다.
const STEP = 70;
let walked = scrollY, foot = 1;
addEventListener('scroll', () => {
  if (reduced || !matchMedia('(hover: none)').matches) { walked = scrollY; return; }
  while (Math.abs(scrollY - walked) >= STEP) {
    const down = scrollY > walked;
    walked += down ? STEP : -STEP;
    foot = -foot;
    const y = walked + innerHeight * 0.62; // 화면 아래쪽 2/3 지점 — 엄지에 안 가리는 높이
    paw(document.documentElement.clientWidth - 22 + Math.sin(y / 260) * 5 + foot * 6, y, down ? 180 : 0);
  }
}, { passive: true });
