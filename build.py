#!/usr/bin/env python3
"""냥냥비트 사이트 세 언어(index.html · ja/index.html · en/index.html)를 한 틀에서 만든다.
문구·앱을 고치면 아래 APPS·STR·SNS를 고치고 `python3 build.py`를 다시 돌린다 — 세 파일을 손으로 고치면 언어끼리 어긋난다.
모양은 style.css, 움직임(카드 뒤집기·빼꼼 고양이·발자국)은 main.js."""
from html import escape
from string import Template

# 새 소식을 올리는 계정. 주소를 채우면 소개 쪽지에 링크가 생긴다(비어 있으면 안 보인다).
SNS = [('Threads', ''), ('Instagram', '')]

# 앱 목록 — 보드에 붙는 순서. 링크가 하나도 없으면 뒷면에 "준비 중"이 뜬다.
APPS = [
  dict(icon='assets/nyangnyang.png', links=[('page', {'ko': '/nyangnyang-site/', 'ja': '/nyangnyang-site/', 'en': '/nyangnyang-site/'}),
                                             ('App Store', 'https://apps.apple.com/kr/app/id6806888734')],
       ko=('냥냥서가', '마음에 든 책 구절을 찍어 모으는 서재', '책 속 문장을 사진으로 찍으면 글자로 바꿔 기록해 줘요. 읽은 책과 구절이 차곡차곡 쌓여요.'),
       # 한국어 전용 앱이라 공식 일본어·영어 이름이 없다 — 이름을 지어내지 않고 로마자 표기 + "한국어 전용"을 밝힌다
       ja=('Nyangnyang Seoga', 'お気に入りの一節を撮って集める本棚（韓国語のみ）', '本の一節を写真に撮ると文字にして記録してくれます。読んだ本と言葉が少しずつたまっていきます。'),
       en=('Nyangnyang Seoga', 'Snap and keep your favorite book passages (Korean only)', 'Take a photo of a passage and it turns into text you can keep. Your books and favorite lines pile up, page by page.')),
  dict(icon='assets/moanyang.png', links=[('page', {'ko': '/moanyang-site/', 'ja': '/moanyang-site/ja/', 'en': '/moanyang-site/en/'})],
       ko=('모아냥', '안 쓴 돈으로 갖고 싶은 걸 물들이는 저금 앱', '아낀 돈을 하루 한 번 적으면, 찍어 둔 물건 사진이 모은 만큼 색으로 차올라요.'),
       ja=('モアニャン', '使わなかったお金で、ほしいものに色をつける貯金アプリ', '節約したお金を1日1回記録すると、撮っておいたほしいものの写真が、たまったぶんだけ色づきます。'),
       en=('MoaNyang', 'Color in what you want with money you didn’t spend', 'Log what you saved once a day, and the photo of what you want fills with color as you go.')),
  dict(icon=None, links=[],
       ko=('다음 앱', '고양이가 또 뭔가 준비하고 있어요', '아직 비밀이에요. 나오면 여기에 제일 먼저 붙일게요.'),
       ja=('次のアプリ', 'ねこがまた何か準備しています', 'まだ秘密です。できたら、いちばんにここに貼ります。'),
       en=('Next app', 'The cat is cooking up something new', 'Still a secret. It’ll be pinned here first when it’s ready.')),
]

STR = {
 'ko': dict(title='냥냥비트 — 고양이랑 같이, 작은 앱을 만듭니다', desc='냥냥서가·모아냥을 만든 1인 앱 작업실 냥냥비트예요.',
            brand='냥냥비트', nav_apps='앱', nav_about='소개', h1='고양이랑 같이,<br>작은 앱을 만듭니다',
            sub='매일 조금씩 손이 가는 앱을 하나씩 만들고 있어요.', flip='뒤집기', page='소개 페이지', soon='준비 중',
            about_h='냥냥비트는요', about_p='혼자 앱을 만드는 작은 작업실이에요. 책 읽기, 돈 모으기처럼 꾸준히 하기 어려운 일을 고양이와 함께라면 조금 더 오래 할 수 있다고 믿어요.',
            about_hand='새 앱 소식은 SNS에서!', contact='문의'),
 'ja': dict(title='ニャンニャンビット — ねこと一緒に、小さなアプリをつくっています', desc='Nyangnyang Seoga・モアニャンをつくった、ひとりのアプリ工房です。',
            brand='ニャンニャンビット', nav_apps='アプリ', nav_about='紹介', h1='ねこと一緒に、<br>小さなアプリを<br>つくっています',
            sub='毎日ちょっとずつ使いたくなるアプリを、ひとつずつつくっています。', flip='めくる', page='紹介ページ', soon='準備中',
            about_h='ニャンニャンビットについて', about_p='ひとりでアプリをつくっている小さな工房です。読書や貯金のように続けにくいことも、ねこと一緒なら少し長く続けられると思っています。',
            about_hand='新しいアプリのお知らせはSNSで!', contact='お問い合わせ'),
 'en': dict(title='NyangNyangBit — Small apps, made with a cat', desc='NyangNyangBit is a one-person app studio behind Nyangnyang Seoga and MoaNyang.',
            brand='NyangNyangBit', nav_apps='Apps', nav_about='About', h1='Small apps,<br>made with a cat',
            sub='Little apps you’ll want to open a bit every day — made one at a time.', flip='flip', page='Learn more', soon='Coming soon',
            about_h='About NyangNyangBit', about_p='A tiny one-person app studio. Habits like reading and saving are hard to keep up — but with a cat by your side, you might just stick with them a little longer.',
            about_hand='new apps are announced on social!', contact='Contact'),
}

HAND = {'ko': 'Nanum+Pen+Script', 'ja': 'Yomogi', 'en': 'Caveat:wght@600'}
NAV = {'ko': ('./', 'ja/', 'en/'), 'ja': ('../', './', '../en/'), 'en': ('../', '../ja/', './')}

PAGE = Template("""<!doctype html>
<html lang="$lang">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title</title>
<meta name="description" content="$desc">
<link rel="icon" type="image/png" href="${up}assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=$hand_font&display=swap" rel="stylesheet">
<link rel="stylesheet" href="${up}style.css">
</head>
<body>
<div class="wrap">
  <header class="top">
    <a class="logo" href="$home"><img src="${up}assets/cat.png" alt="" width="34" height="34">$brand</a>
    <nav><a href="#apps">$nav_apps</a><a href="#about">$nav_about</a>$langs</nav>
  </header>

  <section class="intro">
    <h1>$h1</h1>
    <p>$sub</p>
  </section>

  <!-- 앱 보드: 폴라로이드를 누르면 뒤집힌다. 고양이는 고른 카드 뒤에서 빼꼼한다(main.js) -->
  <section class="apps" id="apps">
    <div class="board-grid">
$cards
    </div>
    <img class="sitter" id="sitter" src="${up}assets/cat.png" alt="">
  </section>

  <section class="about" id="about">
    <div class="note">
      <span class="tape"></span>
      <h2>$about_h</h2>
      <p>$about_p</p>
      <span class="hand">$about_hand</span>
      <div class="links">$sns<a href="mailto:sokurihj@gmail.com">$contact sokurihj@gmail.com</a></div>
    </div>
  </section>

  <footer>$brand · sokurihj@gmail.com</footer>
</div>
<script src="${up}main.js"></script>
</body>
</html>
""")

CARD = Template("""      <div class="card" style="--rot:$rot" tabindex="0" role="button" aria-pressed="false" aria-label="$name $flip">
        <div class="card-in">
          <div class="face front">
            <span class="tape" style="--tape-rot:$tape"></span>
            <div class="win">$win</div>
            <div class="lab"><b>$name</b><span>$line</span></div>
          </div>
          <div class="face back">
            <div><h3>$name</h3><p>$back</p></div>
            <div class="links">$links</div>
          </div>
        </div>
      </div>""")

for lang, s in STR.items():
    up = '' if lang == 'ko' else '../'
    links = NAV[lang]
    langs = ''.join(f'<a class="lang" href="{h}"{" aria-current=\"page\"" if l == lang else ""}>{n}</a>'
                    for h, l, n in zip(links, ('ko', 'ja', 'en'), ('한국어', '日本語', 'English')))
    cards = []
    for i, app in enumerate(APPS):
        name, line, back = (escape(t) for t in app[lang])
        win = f'<img src="{up}{app["icon"]}" alt="">' if app['icon'] else '<span class="soon">?</span>'
        ls = ''.join(f'<a href="{href[lang] if isinstance(href, dict) else href}">{s["page"] if label == "page" else label}</a>'
                     for label, href in app['links']) or f'<span>{s["soon"]}</span>'
        cards.append(CARD.substitute(rot=('-2deg', '1.5deg', '-1deg')[i % 3], tape=f'{3 if i % 2 else -2}deg',
                                     name=name, line=line, back=back, win=win, links=ls, flip=s['flip']))
    sns = ''.join(f'<a href="{url}">{label}</a>' for label, url in SNS if url)
    html = PAGE.substitute(s, lang=lang, up=up, home=links[('ko', 'ja', 'en').index(lang)], langs=langs,
                           cards='\n'.join(cards), sns=sns, hand_font=HAND[lang])
    open('index.html' if lang == 'ko' else f'{lang}/index.html', 'w').write(html)
    print('wrote', lang)
