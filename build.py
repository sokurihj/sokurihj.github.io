#!/usr/bin/env python3
"""냥냥비트 사이트 전체를 한 틀에서 만든다 — 첫 화면 · 앱 페이지(앱마다 같은 틀) · 소개, 세 언어.
  한국어 /, /moanyang/, /nyangnyang/, /about/   일본어 /ja/...   영어 /en/...
문구·앱을 고치면 아래 APPS·UI를 고치고 `python3 build.py`를 다시 돌린다(손으로 HTML을 고치면 언어끼리 어긋난다).
모양은 style.css, 움직임(목록에서 빼꼼하는 고양이·폰 스크롤 발자국)은 main.js.
처리방침·약관은 예전 저장소(moanyang-site · nyangnyang-site)에 그대로 있다 — 앱스토어에 등록된 주소라 옮기지 않는다."""
import hashlib, os
from html import escape

LANGS = ('ko', 'ja', 'en')
PREFIX = {'ko': '/', 'ja': '/ja/', 'en': '/en/'}
EMAIL = 'sokurihj@gmail.com'
SNS = [('Threads', 'https://www.threads.com/@nyangnyangbit'), ('Instagram', 'https://www.instagram.com/nyangnyangbit/')]  # 주소를 채우면 소개 페이지에 링크가 생긴다

def ver(f):  # 파일이 바뀌면 주소가 바뀌게 — 브라우저가 옛 스타일을 붙들고 있지 않도록
    return hashlib.md5(open(f, 'rb').read()).hexdigest()[:8]

UI = {
 'ko': dict(studio='냥냥비트', apps='앱', about='소개',
            home_h='고양이랑 같이,<br>작은 앱을 만듭니다', home_p='매일 조금씩 손이 가는 앱을 하나씩 만들고 있어요.',
            how='이런 앱이에요', platforms='지원 기기', get='받기', soon='곧 출시', faq='자주 묻는 질문',
            others='다른 앱', privacy='개인정보 처리방침', terms='이용약관', contact='문의',
            about_h='냥냥비트는요', about_p=['혼자 앱을 만드는 작은 작업실이에요.', '책 읽기, 돈 모으기처럼 꾸준히 하기 어려운 일을 고양이와 함께라면 조금 더 오래 할 수 있다고 믿어요. 그래서 앱마다 고양이가 한 마리씩 살고 있어요.'],
            next_app=('다음 앱', '만드는 중'),
            about_kind='혼자 꾸리는 앱 작업실', about_say='메일은 내가 직접 읽는다냥', made='만든 앱', sns_h='SNS',
            about_big='꾸준히 하기 어려운 일을,<br>고양이랑 같이.',
            ways=[('혼자 다 해요', '기획, 그림, 개발, 문의 답장까지 한 사람이 해요. 메일을 보내면 만든 사람이 직접 읽고 답해요.'),
                  ('하루 잠깐이면 돼요', '오래 붙잡아 두는 앱보다, 하루에 한 번 잠깐 열고 닫는 앱을 만들어요.'),
                  ('고양이가 한 마리씩', '앱마다 고양이가 살아요. 혼자 하는 기록이 덜 심심하도록요.')]),
 'ja': dict(studio='ニャンニャンビット', apps='アプリ', about='紹介',
            home_h='ねこと一緒に、<br>小さなアプリを<br>つくっています', home_p='毎日ちょっとずつ使いたくなるアプリを、ひとつずつつくっています。',
            how='こんなアプリです', platforms='対応端末', get='ダウンロード', soon='近日公開', faq='よくある質問',
            others='ほかのアプリ', privacy='プライバシーポリシー', terms='利用規約', contact='お問い合わせ',
            about_h='ニャンニャンビットについて', about_p=['ひとりでアプリをつくっている小さな工房です。', '読書や貯金のように続けにくいことも、ねこと一緒なら少し長く続けられると思っています。だから、どのアプリにもねこが一匹ずつ住んでいます。'],
            next_app=('次のアプリ', 'つくっています'),
            about_kind='ひとりで営むアプリ工房', about_say='メールはわたしが直接読むにゃ', made='つくったアプリ', sns_h='SNS',
            about_big='続けにくいことを、<br>ねこと一緒に。',
            ways=[('ぜんぶひとりで', '企画、イラスト、開発、お問い合わせへの返信まで、ひとりで担当しています。メールはつくった本人が読んでお返事します。'),
                  ('一日ちょっとだけ', '長く引きとめるアプリより、一日に一度さっと開いて閉じるアプリをつくっています。'),
                  ('ねこが一匹ずつ', 'どのアプリにもねこが住んでいます。ひとりで続ける記録が、少しでも楽しくなるように。')]),
 'en': dict(studio='NyangNyangBit', apps='Apps', about='About',
            home_h='Small apps,<br>made with a cat', home_p='Little apps you’ll want to open a bit every day — made one at a time.',
            how='What it does', platforms='Platforms', get='Get the app', soon='Coming soon', faq='FAQ',
            others='Other apps', privacy='Privacy Policy', terms='Terms', contact='Contact',
            about_h='About NyangNyangBit', about_p=['A tiny one-person app studio.', 'Habits like reading and saving are hard to keep up — but with a cat by your side, you might stick with them a little longer. So every app has a cat living in it.'],
            next_app=('Next app', 'In the works'),
            about_kind='A one-person app studio', about_say='I read every email myself, meow', made='Apps', sns_h='Social',
            about_big='Hard-to-keep habits,<br>kept with a cat.',
            ways=[('One person, all of it', 'Planning, drawing, coding and answering your emails — all done by one person. Your message is read by the person who made the app.'),
                  ('A minute a day', 'Not apps that hold on to you, but apps you open for a moment once a day and close again.'),
                  ('A cat in every app', 'Every app has a cat living in it, so keeping a record on your own feels a little less lonely.')]),
}

# 앱 — 첫 화면 목록·앱 페이지·아래 "다른 앱" 목록이 모두 여기서 나온다. 순서가 곧 번호.
APPS = [
 dict(slug='nyangnyang', en_name='Nyangnyang Seoga', icon='assets/nyangnyang.png', poster='#efe0c2',
      shots=[f'assets/shots/nyangnyang-{i}.webp' for i in range(1, 7)],
      store=[('App Store', 'https://apps.apple.com/kr/app/id6806888734')],
      legal={'privacy': '/nyangnyang-site/privacy.html', 'terms': '/nyangnyang-site/terms.html'},
      faq={"ko": "<h3>로그인해야 쓸 수 있나요?</h3>\n<p>아니요. 책 등록, 구절·메모 기록, 단어장, 독서 시간, 고양이 모으기는 로그인 없이 바로 쓸 수 있어요. 로그인은 서버 백업과 피드를 쓰고 싶을 때만 하면 돼요.</p>\n<h3>폰을 바꾸면 기록은 어떻게 옮기나요?</h3>\n<p>기록은 기본적으로 내 기기에만 저장돼서, 앱을 지우면 함께 사라져요. <b>설정 → 기록 보관하기</b>로 파일을 만들어 두면 새 기기에서 \"보관해 둔 파일 불러오기\"로 모두 되살릴 수 있어요. 로그인해 두면 책·구절·메모·단어장은 서버에도 백업돼요.</p>\n<h3>찍은 사진은 어디로 보내지나요?</h3>\n<p>아이폰에서는 사진 속 글자를 기기 안에서 읽어서 사진이 밖으로 나가지 않아요. 자세한 내용은 <a href=\"/nyangnyang-site/privacy.html\">개인정보 처리방침</a>에 있어요.</p>\n<h3>무료인가요?</h3>\n<p>책 기록, 구절 촬영, 단어장, 독서 시간, 고양이, 백업, 피드는 모두 무료이고 횟수 제한도 없어요. 공유 카드 추가 템플릿, 인물 관계도 3명 이상, 태그 그래프 3개 이상만 유료이고, 한 번 사면 계속 쓸 수 있어요. 구독도 광고도 없어요.</p>\n<h3>폰을 바꾸면 산 기능은 어떻게 되나요?</h3>\n<p>같은 Apple 계정으로 로그인한 새 아이폰에서 <b>구매 복원</b>을 누르면 추가 결제 없이 다시 열려요.</p>\n<h3>환불은 어떻게 하나요?</h3>\n<p>결제는 Apple이 처리해서 환불도 Apple에 요청해야 해요. <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>에서 신청할 수 있어요. 결제했는데 기능이 열리지 않으면 메일로 알려 주세요.</p>", "ja": "<h3>ログインしないと使えませんか？</h3>\n<p>いいえ。本の登録、文章・メモの記録、単語帳、読書時間、ねこ集めはログインなしですぐに使えます。ログインが必要なのは、サーバーへのバックアップとフィードを使うときだけです。</p>\n<h3>機種変更のとき、記録はどう移しますか？</h3>\n<p>記録は基本的にこの端末にのみ保存されるため、アプリを削除すると一緒に消えます。<b>설정 → 기록 보관하기</b>（設定 → 記録を保管する）でファイルを作っておけば、新しい端末の「보관해 둔 파일 불러오기」（保管したファイルを読み込む）からすべて戻せます。ログインしていれば、本・文章・メモ・単語帳はサーバーにもバックアップされます。</p>\n<h3>撮った写真はどこに送られますか？</h3>\n<p>iPhoneでは写真の文字を端末内で読み取るため、写真が外部に送られることはありません。詳しくは<a href=\"/nyangnyang-site/privacy.html\">プライバシーポリシー</a>（韓国語）をご確認ください。</p>\n<h3>無料ですか？</h3>\n<p>本の記録、文章の撮影、単語帳、読書時間、ねこ、バックアップ、フィードはすべて無料で、回数の制限もありません。共有カードの追加テンプレート、人物相関図の3人以上、タググラフの3つ以上のみ有料で、一度購入すればずっと使えます。サブスクリプションも広告もありません。</p>\n<h3>機種変更すると購入した機能はどうなりますか？</h3>\n<p>同じApple アカウントでサインインした新しいiPhoneで<b>구매 복원</b>（購入を復元）すると、追加の支払いなしで再び使えます。</p>\n<h3>返金するには？</h3>\n<p>決済はAppleが行うため、返金もAppleにご請求ください。<a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>から申請できます。購入したのに機能が使えない場合はメールでお知らせください。</p>", "en": "<h3>Do I need to log in?</h3>\n<p>No. Adding books, saving quotes and notes, the word list, reading time and collecting cats all work without logging in. You only need to log in for server backup and the feed.</p>\n<h3>How do I move my records to a new phone?</h3>\n<p>Your records are stored only on your device by default, so deleting the app deletes them too. Make a file with <b>설정 → 기록 보관하기</b> (Settings → Keep my records), then use “보관해 둔 파일 불러오기” (Load a saved file) on your new device to bring everything back. If you’re logged in, your books, quotes, notes and word list are also backed up to the server.</p>\n<h3>Where do my photos go?</h3>\n<p>On iPhone, text in your photos is read on the device itself, so photos never leave it. See the <a href=\"/nyangnyang-site/privacy.html\">Privacy Policy</a> (in Korean) for details.</p>\n<h3>Is it free?</h3>\n<p>Book records, quote capture, the word list, reading time, cats, backup and the feed are all free with no limits. Only extra share-card templates, character maps with 3+ people and tag graphs with 3+ tags are paid — buy once and keep them forever. No subscriptions, no ads.</p>\n<h3>What happens to my purchases if I switch phones?</h3>\n<p>Tap <b>구매 복원</b> (Restore Purchases) on your new iPhone signed in with the same Apple Account, and they unlock again at no extra cost.</p>\n<h3>How do I get a refund?</h3>\n<p>Apple processes all payments, so refunds are requested from Apple at <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>. If a purchase didn’t unlock, please email us.</p>"},
      meta={'released': {'ko': '2026.09 출시', 'ja': '2026.09 リリース', 'en': 'Released 2026.09'}, 'platform': 'iOS', 'price': {'ko': '무료 · 일부 인앱 구매', 'ja': '無料 · 一部アプリ内課金', 'en': 'Free · optional in-app purchases'}},
      pills=['iPhone', 'iOS 16.4+'],
      ko=dict(name='냥냥서가', kind='책 구절 기록', lead='오늘 읽은 문장, 냥냥서가에 옮겨둘까요? 책 페이지를 사진으로 찍으면 문장이 그대로 기록돼요.',
              say='좋은 문장, 사진첩에 묻어 두지 말라냥',
              how='책을 펼치고 카메라로 찍으면 문장을 인식해 옮겨 적어요. 읽기 전·읽는 중·완독으로 서재를 나누고, 구절마다 메모와 단어장, 등장인물 관계도까지 남길 수 있어요. 책을 등록할 때마다 캣타워에 고양이가 한 마리씩 늘어나요.',
              note=''),
      ja=dict(name='Nyangnyang Seoga', kind='本の一節の記録（韓国語のみ）', lead='今日読んだ一文を、残しておきませんか。本のページを写真に撮ると、文章がそのまま記録されます。',
              say='いい一文、カメラロールに埋もれさせないでにゃ',
              how='本を開いてカメラで撮ると、文章を読み取って書き写します。読む前・読書中・読了で本棚を分け、一節ごとのメモや単語帳、登場人物の相関図も残せます。本を登録するたびに、キャットタワーのねこが一匹ずつ増えていきます。',
              note='現在、アプリは韓国語のみです。'),
      en=dict(name='Nyangnyang Seoga', kind='Book passage log (Korean only)', lead='Found a line worth keeping? Snap the page and the passage is saved as text.',
              say='Don’t let great lines get lost in your camera roll, meow',
              how='Open your book and take a photo — the passage is recognized and written out for you. Sort your shelf into to-read, reading and finished, and keep notes, a word list and even a character map for each book. Every book you add brings one more cat to your cat tower.',
              note='The app is currently available in Korean only.')),
 dict(slug='moanyang', en_name='MoaNyang', icon='assets/moanyang.png', poster='#ece8de',
      shots={l: [f'assets/shots/moanyang-{l}-{t}.webp' for t in ('entry', 'home', 'detail', 'history', 'shop')] for l in LANGS},
      store=[],
      legal={'privacy': {'ko': '/moanyang-site/privacy.html', 'ja': '/moanyang-site/ja/privacy.html', 'en': '/moanyang-site/en/privacy.html'}},
      # released: 출시 전이라 비움 — '곧 출시'는 받기 버튼에 이미 있다
      meta={'released': '', 'platform': 'iOS', 'price': {'ko': '무료 · 필름 팩 인앱 구매', 'ja': '無料 · フィルムパックはアプリ内課金', 'en': 'Free · film packs in-app'}},
      pills=['iPhone', 'iOS 16+', '한국어 · English · 日本語'],
      faq={"ko": "<h3>기록은 어디에 저장되나요?</h3>\n<p>모은 돈, 날짜별 기록, 물건 목록은 모두 내 기기에만 저장돼요. 서버에는 보내지 않아서 앱을 삭제하면 기록도 함께 사라져요. 앱을 지우거나 폰을 바꾸기 전에 <b>설정 → 백업 파일 만들기</b>로 파일을 저장해 두면, 그 파일로 언제든 되살릴 수 있어요.</p>\n<h3>필름이 뭔가요?</h3>\n<p>물건 사진을 픽셀 그림으로 바꿀 때 한 장씩 쓰여요. 처음 한 장은 무료이고, 그 뒤로는 필름 팩을 사서 쓸 수 있어요. 변환에 실패하면 필름은 돌아와요.</p>\n<h3>앱을 지웠다 다시 깔면 필름은 어떻게 되나요?</h3>\n<p>그대로 남아 있어요. 필름은 아이폰 키체인에 보관된 번호로 관리돼서 다시 설치해도 이어지고, iCloud 키체인을 켜 두면 같은 Apple 계정의 새 아이폰으로도 넘어가요. 결제했는데 필름이 들어오지 않았다면 결제한 날짜와 상품을 적어 메일로 알려 주세요.</p>\n<h3>사진은 어디로 보내지나요?</h3>\n<p>픽셀 그림으로 바꾸기 위해 외부 AI 서비스(fal.ai)로 보내지고, 저장되지 않아요. 자세한 내용은 <a href=\"/moanyang-site/privacy.html\">개인정보 처리방침</a>에 있어요.</p>\n<h3>환불은 어떻게 하나요?</h3>\n<p>결제는 Apple이 처리해서 환불도 Apple에 요청해야 해요. <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>에서 신청할 수 있어요.</p>", "ja": "<h3>記録はどこに保存されますか？</h3>\n<p>たまったお金、日ごとの記録、ほしいものリストはすべてこの端末にのみ保存されます。サーバーには送られないため、アプリを削除すると記録も消えます。アプリの削除や機種変更の前に<b>設定 → バックアップファイルを作る</b>でファイルを保存しておけば、そのファイルからいつでも戻せます。</p>\n<h3>フィルムとは何ですか？</h3>\n<p>写真をドット絵に変換するときに1枚ずつ使います。最初の1枚は無料で、その後はフィルムパックを購入して使えます。変換に失敗した場合、フィルムは戻ります。</p>\n<h3>アプリを入れ直すとフィルムはどうなりますか？</h3>\n<p>そのまま残ります。フィルムはiPhoneのキーチェーンに保管した番号で管理しているため、再インストールしても引き継がれ、iCloudキーチェーンをオンにしていれば同じApple アカウントの新しいiPhoneにも引き継がれます。購入後にフィルムが届かない場合は、購入日と商品を添えてメールでお問い合わせください。</p>\n<h3>写真はどこに送られますか？</h3>\n<p>ドット絵に変換するため外部のAIサービス（fal.ai）に送信され、保存されません。詳しくは<a href=\"/moanyang-site/ja/privacy.html\">プライバシーポリシー</a>をご確認ください。</p>\n<h3>返金するには？</h3>\n<p>決済はAppleが行うため、返金もAppleにご請求ください。<a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>から申請できます。</p>", "en": "<h3>Where are my records stored?</h3>\n<p>Your savings, daily log, and wish list are stored only on this device. They aren’t sent to a server, so deleting the app deletes them too. Before deleting the app or switching phones, save a file with <b>Settings → Make a backup file</b> — you can restore from it anytime.</p>\n<h3>What are films?</h3>\n<p>One film is used each time a photo is turned into pixel art. Your first film is free; after that you can buy film packs. If a conversion fails, the film is returned.</p>\n<h3>What happens to my films if I reinstall the app?</h3>\n<p>They stay. Films are tied to a number kept in your iPhone’s Keychain, so they carry over when you reinstall — and to a new iPhone on the same Apple Account if iCloud Keychain is on. If films didn’t arrive after a purchase, email us with the purchase date and product.</p>\n<h3>Where do my photos go?</h3>\n<p>They’re sent to an external AI service (fal.ai) to make the pixel art and aren’t stored. See the <a href=\"/moanyang-site/en/privacy.html\">Privacy Policy</a> for details.</p>\n<h3>How do I get a refund?</h3>\n<p>Apple processes all payments, so refunds are requested from Apple at <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>.</p>"},
      ko=dict(name='모아냥', kind='안 쓴 돈 저금', lead='커피 한 잔, 택시 한 번. 오늘 아낀 돈을 적으면 찍어 둔 물건 사진이 모은 만큼 색으로 차올라요.',
              say='아낀 돈이 숫자로만 남으면 금방 잊는다냥',
              how='하루 한 번 안 쓴 돈을 동전과 지폐로 적어요. 갖고 싶은 물건을 찍으면 AI가 픽셀 그림 폴라로이드로 바꿔 보드에 붙이고, 모은 만큼 아래에서부터 색이 차올라요. 물건을 사면 코인이 생겨 고양이에게 모자·목걸이·안경을 씌워 줄 수 있어요.',
              note=''),
      ja=dict(name='モアニャン', kind='使わなかったお金の貯金', lead='コーヒー1杯、タクシー1回。今日節約したお金を記録すると、撮っておいたほしいものの写真が、たまったぶんだけ色づきます。',
              say='節約したお金、数字だけだとすぐ忘れちゃうにゃ',
              how='使わなかったお金を、1日1回、硬貨とお札で記録します。ほしいものを撮るとAIがドット絵のインスタント写真にしてボードに貼り、たまったぶんだけ下から色づいていきます。買うとコインがもらえて、ねこに帽子・ネックレス・メガネをつけてあげられます。',
              note=''),
      en=dict(name='MoaNyang', kind='Save what you didn’t spend', lead='A coffee here, a cab ride there. Log what you saved today, and the photo of what you want fills with color as you go.',
              say='Saved money is easy to forget when it’s just a number, meow',
              how='Once a day, tap coins and bills to log what you didn’t spend. Snap something you want and AI turns it into a pixel-art snapshot pinned to your board — and it fills with color from the bottom as you save. Buy it and you earn coins to dress your cat in hats, necklaces and glasses.',
              note='')),
]

def head(lang, title, desc, depth):
    up = '../' * depth
    hand = {'ko': 'Gowun+Batang:wght@700', 'ja': 'Zen+Old+Mincho:wght@700', 'en': 'Gowun+Batang:wght@700'}[lang]
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family={hand}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="/style.css?v={ver('style.css')}">
</head>
<body>
"""

def header(lang, path):
    u = UI[lang]; p = PREFIX[lang]
    langs = ''.join(f'<a class="lang" href="{PREFIX[l]}{path}"{" aria-current=\"page\"" if l == lang else ""}>{l.upper()}</a>' for l in LANGS)
    return f"""<header class="nav">
  <a class="brand" href="{p}"><img src="/assets/cat.png" alt="" width="28" height="28"><b>{UI['en']['studio']}</b></a>
  <nav><a href="{p}#apps">{u['apps']}</a><a href="{p}about/">{u['about']}</a><span class="langs">{langs}</span></nav>
</header>
"""

def cards(lang, current=None, small=False):
    """앱 폴라로이드 — 첫 화면과 앱 페이지 아래 "다른 앱"에 같이 쓴다. 고양이가 고른 카드 윗변 뒤에서 빼꼼한다(main.js)."""
    p = PREFIX[lang]; out = []
    for i, a in enumerate(APPS):
        t = a[lang]
        if a['slug'] == current: continue
        out.append(f"""    <a class="card" href="{p}{a['slug']}/" style="--rot:{('-2deg', '1.6deg', '-1deg')[i % 3]}; --poster:{a['poster']}">
      <span class="tape"></span>
      <span class="win"><img src="/{a['icon']}" alt="" width="200" height="200"></span>
      <span class="lab"><b>{escape(t['name'])}</b>{escape(t['kind'])}</span>
    </a>""")
    n, k = UI[lang]['next_app']
    out.append(f"""    <span class="card soon" style="--rot:1.2deg; --poster:#f3f1ec"><span class="tape"></span><span class="win"><span class="q">?</span></span><span class="lab"><b>{n}</b>{k}</span></span>""")
    return f'<div class="cards{" small" if small else ""}">\n' + '\n'.join(out) + '\n<img class="sitter" src="/assets/cat.png" alt=""></div>'

def footer(lang):
    u = UI[lang]
    return f"""<footer class="foot"><span>© 2026 {u['studio']}</span><a href="mailto:{EMAIL}">{EMAIL}</a></footer>
<script src="/main.js?v={ver('main.js')}"></script>
</body>
</html>
"""

def pick(v, lang):
    return v[lang] if isinstance(v, dict) else v

def write(path, html):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    open(path, 'w').write(html)
    print('wrote', path)

for lang in LANGS:
    u = UI[lang]; base = '' if lang == 'ko' else f'{lang}/'
    # ── 첫 화면 ──
    write(f'{base}index.html', head(lang, f"{u['studio']} — {u['home_h'].replace('<br>', ' ')}", u['home_p'], 0) + header(lang, '') + f"""<main class="home">
  <h1 class="hero">{u['home_h']}</h1>
  <p class="hero-p">{u['home_p']}</p>
  <section id="apps" aria-label="{u['apps']}">
{cards(lang)}
  </section>
</main>
""" + footer(lang))

    # ── 앱 페이지 ──
    for a in APPS:
        t = a[lang]; m = a['meta']
        shots = a['shots'][lang] if isinstance(a['shots'], dict) else a['shots']
        store = ''.join(f'<a class="pill solid" href="{h}">{escape(n)}</a>' for n, h in a['store']) or f'<span class="pill">App Store · {u["soon"]}</span>'
        legal = ''.join(f'<a href="{pick(h, lang)}">{u[k]}</a>' for k, h in a['legal'].items())
        faq = ''
        if 'faq' in a:
            faq = f'<section class="faq"><h2>{u["faq"]}</h2>\n' + a['faq'][lang] + '\n</section>'
        note = f'<p class="note">{escape(t["note"])}</p>' if t['note'] else ''
        write(f'{base}{a["slug"]}/index.html', head(lang, f"{t['name']} — {t['kind']} · {u['studio']}", t['lead'], 1) + header(lang, f"{a['slug']}/") + f"""<main class="proj" style="--poster:{a['poster']}">
  <aside class="side">
    <h1 class="title">{escape(t['name'])}</h1>
    <p class="kind">{escape(t['kind'])}</p>
    <p class="lead">{escape(t['lead'])}</p>
    {note}
    <p class="say"><img src="/assets/cat.png" alt="" width="40" height="40"><span>{escape(t['say'])}</span></p>
    <h2>{u['how']}</h2>
    <p>{escape(t['how'])}</p>
    <h2>{u['platforms']}</h2>
    <div class="pills">{''.join(f'<span class="pill">{escape(x)}</span>' for x in a['pills'] + [pick(m['released'], lang), pick(m['price'], lang)] if x)}</div>
    <h2>{u['get']}</h2>
    <div class="pills">{store}</div>
    <p class="legal">{legal}<a href="mailto:{EMAIL}">{u['contact']}</a></p>
  </aside>
  <div class="main">
    <figure class="hero-pol"><span class="tape"></span><span class="win"><img src="/{a['icon']}" alt="{escape(t['name'])}" width="200" height="200"></span><figcaption>{escape(t['name'])}</figcaption></figure>
    <div class="shots">{''.join(f'<figure class="shot" style="--rot:{("-1.5deg", "1.2deg", "-0.8deg", "1.6deg", "-1.2deg")[i % 5]}"><span class="tape"></span><img src="/{s}" alt="{escape(t["name"])}" loading="lazy"></figure>' for i, s in enumerate(shots))}</div>
    {faq}
    <section class="others" aria-label="{u['others']}"><h2>{u['others']}</h2>
{cards(lang, a['slug'], small=True)}
    </section>
  </div>
</main>
""" + footer(lang))

    # ── 소개: 왼쪽에 연락처·앱 목록, 오른쪽에 큰 한마디·만드는 방식·앱 폴라로이드 ──
    sns = ''.join(f'<a href="{h}">{n}</a>' for n, h in SNS if h)
    sns = f'<h2>{u["sns_h"]}</h2><p class="links">{sns}</p>' if sns else ''
    app_pills = ''.join(f'<a class="pill" href="{PREFIX[lang]}{a["slug"]}/">{escape(a[lang]["name"])}</a>' for a in APPS)
    privacy = ''.join(f'<a href="{pick(a["legal"]["privacy"], lang)}">{escape(a[lang]["name"])}</a>' for a in APPS if 'privacy' in a['legal'])
    ways = ''.join(f'<li><b>{escape(h)}</b><p>{escape(t)}</p></li>' for h, t in u['ways'])
    write(f'{base}about/index.html', head(lang, f"{u['about_h']} · {u['studio']}", u['about_p'][0], 1) + header(lang, 'about/') + f"""<main class="proj about">
  <aside class="side">
    <h1 class="title">{u['studio']}</h1>
    <p class="kind">{u['about_kind']}</p>
    <p class="say"><img src="/assets/cat.png" alt="" width="40" height="40"><span>{escape(u['about_say'])}</span></p>
    <h2>{u['contact']}</h2>
    <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    {sns}
    <h2>{u['apps']}</h2>
    <div class="pills">{app_pills}</div>
    <h2>{u['privacy']}</h2>
    <p class="legal">{privacy}</p>
  </aside>
  <div class="main">
    <p class="big">{u['about_big']}</p>
    {''.join(f'<p class="intro">{escape(x)}</p>' for x in u['about_p'])}
    <ol class="ways">{ways}</ol>
    <section aria-label="{u['made']}"><h2 class="sub">{u['made']}</h2>
{cards(lang)}
    </section>
  </div>
</main>
""" + footer(lang))
