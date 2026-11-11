#!/usr/bin/env python3
"""냥냥비트 사이트 전체를 한 틀에서 만든다 — 첫 화면 · 앱 페이지(앱마다 같은 틀) · 소개, 세 언어.
  한국어 /, /moanyang/, /nyangnyang/, /about/   일본어 /ja/...   영어 /en/...
문구·앱을 고치면 아래 APPS·UI를 고치고 `python3 build.py`를 다시 돌린다(손으로 HTML을 고치면 언어끼리 어긋난다).
모양은 style.css, 움직임(목록에서 빼꼼하는 고양이·폰 스크롤 발자국)은 main.js.
처리방침·약관은 예전 저장소(moanyang-site · nyangnyang-site)에 그대로 있다 — 앱스토어에 등록된 주소라 옮기지 않는다."""
import hashlib, os, re
from html import escape

LANGS = ('ko', 'ja', 'en')
# App Store 링크는 나라 표시가 없으면 보는 사람의 나라로 가서 사이트 언어와 어긋난다 — 언어별로 스토어 나라를 못 박는다
STORE_CC = {'ko': 'kr', 'en': 'us', 'ja': 'jp'}
PREFIX = {'ko': '/', 'ja': '/ja/', 'en': '/en/'}
EMAIL = 'sokurihj@gmail.com'
SNS = [('Threads', 'https://www.threads.com/@nyangnyangbit'), ('Instagram', 'https://www.instagram.com/nyangnyangbit/')]  # 주소를 채우면 소개 페이지에 링크가 생긴다

def ver(f):  # 파일이 바뀌면 주소가 바뀌게 — 브라우저가 옛 스타일을 붙들고 있지 않도록
    return hashlib.md5(open(f, 'rb').read()).hexdigest()[:8]

UI = {
 'ko': dict(studio='냥냥비트', apps='앱', about='소개',
            home_h='고양이랑 같이,<br>작은 앱을 만듭니다', home_p='매일 조금씩 손이 가는 앱을 하나씩 만들고 있어요.',
            how='이런 앱이에요', platforms='지원 기기', get='받기', prev='이전 화면', next='다음 화면', soon='곧 출시', faq='자주 묻는 질문',
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
            how='こんなアプリです', platforms='対応端末', get='ダウンロード', prev='前の画面', next='次の画面', soon='近日公開', faq='よくある質問',
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
            how='What it does', platforms='Platforms', get='Get the app', prev='Previous screenshot', next='Next screenshot', soon='Coming soon', faq='FAQ',
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
      # 순서: 사진 → 문장(OCR)이 첫 장 — 이 앱의 가장 큰 매력을 첫 화면에서 보이려고. 번호는 파일 이름이고, 대체 글(alts)도 이 순서를 따른다
      shots={l: [f'assets/shots/nyangnyang-{l}-{i}.webp' for i in (2, 4, 1, 3, 5, 6)] for l in LANGS},
      og='assets/og/nyangnyang-{lang}.jpg',
      promise={
        'ko': [('로그인 없이 바로 써요', '책 등록부터 구절 기록, 고양이 모으기까지 가입 없이 다 돼요.'), ('기록은 내 폰에 저장돼요', '로그인하기 전에는 책과 구절이 서버에 올라가지 않아요.'), ('광고도 구독도 없어요', '기본 기능은 모두 무료예요. 일부 기능만 한 번 결제하면 계속 써요.')],
        'ja': [('ログインなしですぐ使えます', '本の登録から文章の記録、ねこ集めまで、会員登録は不要です。'), ('記録はこの端末に保存されます', 'ログインするまで、本や文章がサーバーに送られることはありません。'), ('広告もサブスクもありません', '基本の機能はすべて無料。一部の機能だけ、一度の購入でずっと使えます。')],
        'en': [('Use it without logging in', 'From adding books to saving quotes and collecting cats, no account needed.'), ('Your records stay on your phone', 'Nothing is uploaded to our server until you log in.'), ('No ads, no subscriptions', 'The core is free. A few extras unlock with a one-time purchase.')],
      },
      free={'ko': '무료로 시작 · 광고 없음 · 로그인 필요 없음', 'ja': '無料で始められます · 広告なし · ログイン不要', 'en': 'Free to start · No ads · No sign-in needed'},
      alts={'ko': ['찍으면 끝, 문장을 옮겨 적어요. 사진 속 글자를 자동으로 읽어줘요', '마음에 든 문장은 예쁜 카드로 공유. 배경과 글꼴을 골라 SNS에 바로', '고양이들이 지키는 나만의 서재. 읽은 책과 문장을 모으는 곳', '읽은 책과 문장이 차곡차곡 쌓여요. 읽는 중인 책도, 다 읽은 책도 한눈에', '책을 담을 때마다 새 냥냥이를 만나요. 하나씩 채워가는 냥냥이 도감', '읽는 시간은 냥냥이가 재줘요. 잠금화면에서 바로 보는 독서 타이머'], 'ja': ['撮ったらおしまい、一節を書き写します。写真の中の文字を自動で読み取ります', 'お気に入りの一節はカードでシェア。背景と書体を選んでSNSにすぐ投稿', '猫たちが守るわたしの本棚。読んだ本と一節をまとめて置ける場所', '読んだ本と一節がどんどん貯まります。読書中も読了もひと目で', '本を登録するたびににゃんこに会える! ひとつずつ集めるにゃんこ図鑑', '読む時間はにゃんこが計ります。ロック画面ですぐ見られる読書タイマー'], 'en': ['Snap it and the quote is saved! Reads the text in your photo for you', 'Turn a quote into a pretty card! Pick a background and font, then share', 'Cats guard your own library! Where your books and quotes live', 'Your books and quotes pile up! Reading or finished, all at a glance', 'Meet a new cat with every book! Fill your cat collection one by one', 'Your cat times your reading! A reading timer on your Lock Screen']},
      store=[('App Store', 'https://apps.apple.com/{cc}/app/id6806888734'), ('Google Play', 'https://play.google.com/store/apps/details?id=com.nyangnyangseoga.app&amp;hl={hl}')],
      legal={'privacy': {'ko': '/nyangnyang-site/privacy.html', 'ja': '/nyangnyang-site/ja/privacy.html', 'en': '/nyangnyang-site/en/privacy.html'},
             'terms': {'ko': '/nyangnyang-site/terms.html', 'ja': '/nyangnyang-site/ja/terms.html', 'en': '/nyangnyang-site/en/terms.html'}},
      faq={"ko": "<h3>로그인해야 쓸 수 있나요?</h3>\n<p>아니요. 책 등록, 구절·메모 기록, 단어장, 독서 시간, 고양이 모으기는 로그인 없이 바로 쓸 수 있어요. 로그인은 서버 백업과 피드를 쓰고 싶을 때만 하면 돼요.</p>\n<h3>폰을 바꾸면 기록은 어떻게 옮기나요?</h3>\n<p>기록은 기본적으로 내 기기에만 저장돼서, 앱을 지우면 함께 사라져요. <b>설정 → 기록 보관하기</b>로 파일을 만들어 두면 새 기기에서 \"보관해 둔 파일 불러오기\"로 모두 되살릴 수 있어요. 로그인해 두면 책·구절·메모·단어장은 서버에도 백업돼요.</p>\n<h3>찍은 사진은 어디로 보내지나요?</h3>\n<p>아이폰에서는 사진 속 글자를 기기 안에서 읽어서 사진이 밖으로 나가지 않아요. 안드로이드에서는 글자를 더 정확하게 읽으려고 사진을 서버를 거쳐 Google Cloud Vision으로 보내요. 사진은 저장하지 않고 읽어 낸 글자만 돌려받으며, 인터넷에 연결되어 있지 않으면 기기 안에서 읽어요. 자세한 내용은 <a href=\"/nyangnyang-site/privacy.html\">개인정보 처리방침</a>에 있어요.</p>\n<h3>무료인가요?</h3>\n<p>책 기록, 구절 촬영, 단어장, 독서 시간, 고양이 모으기, 백업, 피드는 모두 무료이고 횟수 제한도 없어요. 공유 카드 추가 템플릿, 인물 관계도 3명 이상, 태그 그래프 3개 이상, 프리미엄 고양이(캣타워에 상주하는 특별한 고양이)만 유료이고, 한 번 사면 계속 쓸 수 있어요. 구독도 광고도 없어요.</p>\n<h3>폰을 바꾸면 산 기능은 어떻게 되나요?</h3>\n<p>같은 Apple 계정으로 로그인한 새 아이폰에서 <b>구매 복원</b>을 누르면 추가 결제 없이 다시 열려요. 안드로이드는 같은 Google 계정으로 로그인한 새 폰에서 똑같이 하면 돼요. 다만 아이폰과 안드로이드 사이에서는 구매 내역이 옮겨지지 않아요.</p>\n<h3>환불은 어떻게 하나요?</h3>\n<p>결제는 Apple이 처리해서 환불도 Apple에 요청해야 해요. <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>에서 신청할 수 있어요. 안드로이드는 Google Play가 결제를 처리해서 환불도 Google Play에 요청해야 해요. <a href=\"https://play.google.com/store/account/orderhistory\">Google Play 주문 내역</a>에서 신청할 수 있어요. 결제했는데 기능이 열리지 않으면 메일로 알려 주세요.</p>", "ja": "<h3>ログインしないと使えませんか？</h3>\n<p>いいえ。本の登録、文章・メモの記録、読書時間、ねこ集めはログインなしですぐに使えます。ログインが必要なのは、サーバーへのバックアップとフィードを使うときだけです。</p>\n<h3>機種変更のとき、記録はどう移しますか？</h3>\n<p>記録は基本的にこの端末にのみ保存されるため、アプリを削除すると一緒に消えます。<b>設定 → 記録を保管する</b>でファイルを作っておけば、新しい端末の「保管したファイルを読み込む」からすべて戻せます。ログインしていれば、本・文章・メモはサーバーにもバックアップされます。</p>\n<h3>撮った写真はどこに送られますか？</h3>\n<p>iPhoneでは写真の文字を端末内で読み取るため、写真が外部に送られることはありません。Androidでは、文字をより正確に読み取るために写真をサーバー経由でGoogle Cloud Visionに送信します。写真は保存されず、認識された文字だけが戻ってきます。インターネットに接続できないときは端末内で読み取ります。詳しくは<a href=\"/nyangnyang-site/ja/privacy.html\">プライバシーポリシー</a>をご確認ください。</p>\n<h3>無料ですか？</h3>\n<p>本の記録、文章の撮影、読書時間、ねこ集め、バックアップ、フィードはすべて無料で、回数の制限もありません。共有カードの追加テンプレート、人物相関図の3人以上、タググラフの3つ以上、プレミアムにゃんこ（キャットタワーに居続ける特別なにゃんこ）のみ有料で、一度購入すればずっと使えます。サブスクリプションも広告もありません。</p>\n<h3>機種変更すると購入した機能はどうなりますか？</h3>\n<p>同じApple アカウントでサインインした新しいiPhoneで<b>購入の復元</b>すると、追加の支払いなしで再び使えます。Androidでは、同じGoogleアカウントでサインインした新しい端末で同様に操作してください。iPhoneとAndroidの間では購入は引き継がれません。</p>\n<h3>返金するには？</h3>\n<p>決済はAppleが行うため、返金もAppleにご請求ください。<a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>から申請できます。AndroidではGoogle Playが決済を行うため、返金もGoogle Playにご請求ください。<a href=\"https://play.google.com/store/account/orderhistory\">Google Playの注文履歴</a>から申請できます。購入したのに機能が使えない場合はメールでお知らせください。</p>", "en": "<h3>Do I need to log in?</h3>\n<p>No. Adding books, saving quotes and notes, reading time and collecting cats all work without logging in. You only need to log in for server backup and the feed.</p>\n<h3>How do I move my records to a new phone?</h3>\n<p>Your records are stored only on your device by default, so deleting the app deletes them too. Make a file with <b>Settings → Back up your records</b>, then use “Import a saved file” on your new device to bring everything back. If you’re logged in, your books, quotes and notes are also backed up to the server.</p>\n<h3>Where do my photos go?</h3>\n<p>On iPhone, text in your photos is read on the device itself, so photos never leave it. On Android, photos are sent through our server to Google Cloud Vision to read the text more accurately. They are not stored, and only the recognized text comes back. Without an internet connection, Android reads the text on the device instead. See the <a href=\"/nyangnyang-site/en/privacy.html\">Privacy Policy</a> for details.</p>\n<h3>Is it free?</h3>\n<p>Book records, quote capture, reading time, collecting cats, backup and the feed are all free with no limits. Only extra share-card templates, character maps with 3+ people, tag graphs with 3+ tags and the Premium cat (a special cat that stays in your cat tower) are paid — buy once and keep them forever. No subscriptions, no ads.</p>\n<h3>What happens to my purchases if I switch phones?</h3>\n<p>Tap <b>Restore purchase</b> on your new iPhone signed in with the same Apple Account, and they unlock again at no extra cost. On Android, do the same on a new phone signed in with the same Google account. Purchases don’t carry over between iPhone and Android.</p>\n<h3>How do I get a refund?</h3>\n<p>Apple processes all payments, so refunds are requested from Apple at <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>. On Android, Google Play processes payments, so refunds are requested from Google Play in your <a href=\"https://play.google.com/store/account/orderhistory\">Google Play order history</a>. If a purchase didn’t unlock, please email us.</p>"},
      meta={'released': '', 'platform': 'iOS', 'price': {'ko': '무료 · 일부 인앱 구매', 'ja': '無料 · 一部アプリ内課金', 'en': 'Free · optional in-app purchases'}},
      pills=['iPhone · iOS 16.4+', 'Android 7.0+', '한국어 · English · 日本語'],
      ko=dict(name='냥냥서가', kind='책 구절 기록', lead='오늘 읽은 문장, 냥냥서가에 옮겨둘까요? 책 페이지를 사진으로 찍으면 문장이 그대로 기록돼요.',
              say='좋은 문장, 사진첩에 묻어 두지 말라냥',
              how='책을 펼치고 카메라로 찍으면 문장을 인식해 옮겨 적어요. 읽기 전·읽는 중·완독으로 서재를 나누고, 구절마다 메모와 단어장, 등장인물 관계도까지 남길 수 있어요. 책을 등록할 때마다 캣타워에 고양이가 한 마리씩 늘어나요.',
              note=''),
      ja=dict(name='Nyangnyang Seoga', kind='本の一節の記録', lead='今日読んだ一文を、残しておきませんか。本のページを写真に撮ると、文章がそのまま記録されます。',
              say='いい一文、カメラロールに埋もれさせないでにゃ',
              how='本を開いてカメラで撮ると、文章を読み取って書き写します。読む前・読書中・読了で本棚を分け、一節ごとのメモや登場人物の相関図も残せます。本を登録するたびに、キャットタワーのねこが一匹ずつ増えていきます。',
              note='アプリは韓国語・英語・日本語に対応しています。'),
      en=dict(name='Nyangnyang Seoga', kind='Book passage log', lead='Found a line worth keeping? Snap the page and the passage is saved as text.',
              say='Don’t let great lines get lost in your camera roll, meow',
              how='Open your book and take a photo — the passage is recognized and written out for you. Sort your shelf into to-read, reading and finished, and keep notes and even a character map for each book. Every book you add brings one more cat to your cat tower.',
              note='The app is available in Korean, English and Japanese.')),
 dict(slug='moanyang', en_name='MoaNyang', icon='assets/moanyang.png', poster='#ece8de',
      shots={l: [f'assets/shots/moanyang-{l}-{t}.webp' for t in ('entry', 'home', 'detail', 'history', 'glasses', 'cats', 'outfit')] for l in LANGS},
      promise={
        'ko': [('로그인 없이 바로 써요', '가입도 로그인도 없이 시작해요. 처음 한 장은 무료로 변환해 볼 수 있어요.'), ('기록은 내 폰에만 저장돼요', '모은 돈, 날짜별 기록, 물건 목록은 서버로 보내지 않아요. 사진은 픽셀 그림으로 바꿀 때만 AI에 보내고 저장하지 않아요.'), ('광고도 구독도 없어요', '필름 팩은 필요할 때 한 번만 사는 방식이에요. 정기 결제는 없어요.')],
        'ja': [('ログインなしですぐ使えます', '会員登録もログインも不要です。最初の1枚は無料で変換できます。'), ('記録はこの端末にだけ保存されます', 'たまったお金・日ごとの記録・ほしいものリストはサーバーに送りません。写真はドット絵に変換するときだけAIに送り、保存しません。'), ('広告もサブスクもありません', 'フィルムパックは必要なときに1回だけ購入する方式です。定期課金はありません。')],
        'en': [('Use it without logging in', 'No sign-up, no login. Your first conversion is free.'), ('Your records stay on your phone', 'Your savings, daily log and wish list are never sent to a server. A photo goes to AI only while it’s turned into pixel art, and isn’t stored.'), ('No ads, no subscriptions', 'Buy a film pack once, only when you need it. No recurring charges.')],
      },
      store=[('App Store', 'https://apps.apple.com/{cc}/app/id6819154609'), ('Google Play', 'https://play.google.com/store/apps/details?id=io.github.sokurihj.moanyang&amp;hl={hl}')],
      legal={'privacy': {'ko': '/moanyang-site/privacy.html', 'ja': '/moanyang-site/ja/privacy.html', 'en': '/moanyang-site/en/privacy.html'}},
      meta={'released': '', 'platform': 'iOS', 'price': {'ko': '무료 · 필름 팩 인앱 구매', 'ja': '無料 · フィルムパックはアプリ内課金', 'en': 'Free · film packs in-app'}},
      pills=['iPhone · iOS 16+', 'Android 7.0+', '한국어 · English · 日本語'],
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

 # 출시 전: hidden이면 앱 페이지(/mureonyang/)만 만들고 검색에서 빼며, 첫 화면·소개·다른 앱 목록에는 나오지 않는다.
 # 출시하면 hidden 줄을 지우고 store에 앱스토어 주소를 넣은 뒤 처리방침 세 곳의 noindex도 지운다
 dict(slug='mureonyang', en_name='Fetch Cat', icon='assets/mureonyang.png', poster='#ede7e3', hidden=True,
      shots={l: [f'assets/shots/mureonyang-{l}-{i}.webp' for i in (1, 2, 3, 4)] for l in LANGS},
      promise={
        'ko': [('로그인 없이 바로 써요', '가입도 계정도 없어요. 설치하면 바로 시작해요.'), ('링크는 내 기기와 내 iCloud에만 저장돼요', '우리 서버로 보내지 않아요. 클립보드는 저장하려고 누를 때만 읽어요.'), ('광고도 추적도 없어요', '모든 기능이 무료예요. 후원은 선택이에요.')],
        'ja': [('ログインなしですぐ使えます', '会員登録もアカウントも不要です。インストールしたらすぐ始められます。'), ('リンクは端末と自分のiCloudだけに保存されます', '運営者のサーバーには送りません。クリップボードは、保存のために操作したときだけ読み取ります。'), ('広告もトラッキングもありません', 'すべての機能が無料です。応援は任意です。')],
        'en': [('Use it without logging in', 'No sign-up, no account. Just install and go.'), ('Links stay on your devices and in your iCloud', 'Nothing goes to our servers. The clipboard is read only when you choose to save.'), ('No ads, no tracking', 'Everything is free. Tips are optional.')],
      },
      free={'ko': '무료 · 광고 없음 · 로그인 필요 없음', 'ja': '無料 · 広告なし · ログイン不要', 'en': 'Free · No ads · No sign-in needed'},
      alts={'ko': ['복사한 링크를 폴더에 차곡차곡 모아요', '공유 버튼으로 바로 저장해요. 사파리·크롬 어디서든 폴더만 고르면 끝', '저장하면 고양이가 알려줘요. 생선을 물고 와서 넣었다고 말해 줘요', '왜 저장했는지 메모로 남겨요'],
            'ja': ['コピーしたリンクを、フォルダできれいに', '共有ボタンからすぐ保存。SafariやChromeなど、どこからでもフォルダを選ぶだけ', '保存すると、ねこが教えてくれます', '保存した理由も、メモに残せます'],
            'en': ['Copied links, neatly sorted into folders', 'Save from the Share button in Safari, Chrome or any app. Just pick a folder', 'The cat tells you when a link is saved', 'Add a note to remember why you saved it']},
      store=[],
      legal={'privacy': {'ko': '/mureonyang/privacy.html', 'ja': '/ja/mureonyang/privacy.html', 'en': '/en/mureonyang/privacy.html'}},
      faq={"ko": "<h3>복사한 내용을 읽나요?</h3>\n<p>복사할 때는 웹 주소처럼 보이는지만 확인하고 내용은 읽지 않아요. 저장하려고 폴더를 고르거나 발바닥 버튼을 누를 때만 내용을 읽고, 웹 주소만 저장해요.</p>\n<h3>링크는 어디에 저장되나요?</h3>\n<p>내 기기와 내 iCloud에 저장돼요. Mac과 iPhone이 같은 Apple 계정의 iCloud로 이어지고, 우리 서버로는 보내지 않아서 개발자도 볼 수 없어요.</p>\n<h3>iPhone에서는 어떻게 저장하나요?</h3>\n<p>복사한 링크는 발바닥 버튼을 눌러 붙여넣고, Safari나 크롬 같은 앱에서는 공유 버튼으로 바로 저장해요.</p>\n<h3>후원을 해야 쓸 수 있나요?</h3>\n<p>아니요. 모든 기능이 무료예요. 고양이에게 간식을 선물하는 후원은 선택이에요.</p>",
           "ja": "<h3>コピーした内容を読み取りますか？</h3>\n<p>コピーしたときは、URLかどうかだけを確認し、内容は読み取りません。保存のためにフォルダを選んだり肉球ボタンを押したりしたときだけ内容を読み取り、保存するのはURLだけです。</p>\n<h3>リンクはどこに保存されますか？</h3>\n<p>端末と自分のiCloudに保存されます。MacとiPhoneが同じApple AccountのiCloudでつながり、運営者のサーバーには送らないので、開発者にも見えません。</p>\n<h3>iPhoneではどうやって保存しますか？</h3>\n<p>コピーしたリンクは肉球ボタンでペーストし、Safariなど他のアプリでは共有ボタンからそのまま保存できます。</p>\n<h3>応援しないと使えませんか？</h3>\n<p>いいえ。すべての機能が無料です。ねこにおやつをプレゼントする応援は任意です。</p>",
           "en": "<h3>Does it read what I copy?</h3>\n<p>When you copy, the app only checks whether it looks like a web address; it doesn’t read what you copied. It reads the content only when you pick a folder or tap the paw button to save, and it saves only the web address.</p>\n<h3>Where are my links stored?</h3>\n<p>On your devices and in your own iCloud. Mac and iPhone sync through the iCloud of your Apple Account. Nothing goes to our servers, so even the developer can’t see them.</p>\n<h3>How do I save on iPhone?</h3>\n<p>Tap the paw button to paste a copied link, or use the Share button in Safari, Chrome and other apps.</p>\n<h3>Do I need to tip to use it?</h3>\n<p>No. Everything is free. Giving the cat a treat is optional.</p>"},
      meta={'released': '', 'platform': 'iOS · macOS', 'price': {'ko': '무료 · 후원은 선택', 'ja': '無料 · 応援は任意', 'en': 'Free · optional tips'}},
      pills=['iPhone · iOS 26+', 'Mac · macOS 26+', '한국어 · English · 日本語'],
      ko=dict(name='물어냥', kind='링크 저장·정리', lead='링크를 복사하면 고양이가 물어다 줘요. 폴더만 고르면 저장 끝이에요.',
              say='복사한 링크, 잃어버리지 말라냥',
              how='Mac에서는 바탕화면에 고양이가 살아요. 웹 주소를 복사하면 말풍선이 뜨고, 폴더를 고르면 저장돼요. iPhone에서는 발바닥 버튼으로 붙여넣거나 공유 버튼으로 바로 저장해요. 제목·아이콘·소개글이 자동으로 채워지고, 메모와 고정, 검색까지 되고, Mac과 iPhone이 내 iCloud로 이어져요.',
              note=''),
      ja=dict(name='くわえにゃん', kind='リンクの保存・整理', lead='コピーしたリンクを、ねこがくわえてきます。',
              say='コピーしたリンク、なくさないでにゃ',
              how='Macではデスクトップにねこが住んでいます。リンクをコピーすると吹き出しが出て、フォルダを選ぶだけで保存。iPhoneでは肉球ボタンでペーストしたり、ほかのアプリの共有ボタンからそのまま保存したりできます。タイトル・アイコン・説明文は自動で入ります。メモや固定、検索もでき、MacとiPhoneは自分のiCloudで同期されます。',
              note='アプリは韓国語・英語・日本語に対応しています。'),
      en=dict(name='Fetch Cat', kind='Save and sort links', lead='Copy a link and the cat fetches it. Pick a folder, and it’s saved.',
              say='Don’t lose the links you copy, meow',
              how='On Mac, a cat lives on your desktop. Copy a web address and a speech bubble pops up; pick a folder and the link is saved. On iPhone, tap the paw button to paste, or save straight from the Share button in other apps. Titles, icons and descriptions fill in on their own, and you can add notes, pin favorites and search. Mac and iPhone stay in sync through your own iCloud.',
              note='The app is available in Korean, English and Japanese.')),

 dict(slug='nyancorder', en_name='Nyancorder', icon='assets/nyancorder.png', poster='#f6dfe0',
      store=[('App Store', 'https://apps.apple.com/{cc}/app/id6825653409')],
      soon_store=['Google Play'],  # 안드로이드는 비공개 테스트 중 — 공개되면 이 줄을 지우고 store에 구글 플레이 주소를 넣는다
      shots={l: [f'assets/shots/nyancorder-{l}-{i}.webp' for i in range(1, 9)] for l in LANGS},
      promise={
        'ko': [('로그인 없이 바로 써요', '가입도 계정도 없어요. 열자마자 바로 찍어요.'), ('사진과 영상은 내 폰에서만 처리돼요', '필터는 기기 안에서 입혀지고, 찍은 건 사진 앱에 저장돼요. 서버로 보내지 않아요.'), ('광고도 구독도 없어요', '홈비디오·흑백은 무료예요. 나머지 필터는 한 번만 사면 계속 써요.')],
        'ja': [('ログインなしですぐ使えます', '会員登録もアカウントも不要です。開いたらすぐ撮れます。'), ('写真と動画は端末の中だけで処理されます', 'フィルターは端末内でかけられ、撮ったものは写真アプリに保存されます。サーバーには送りません。'), ('広告もサブスクもありません', 'ホームビデオとモノクロは無料。ほかのフィルターは一度の購入でずっと使えます。')],
        'en': [('Use it without logging in', 'No sign-up, no account. Open it and start shooting.'), ('Photos and videos stay on your phone', 'Filters are applied on your device, and your shots are saved to the Photos app. Nothing goes to a server.'), ('No ads, no subscriptions', 'Home Video and B&W are free. The other filters unlock with a one-time purchase.')],
      },
      free={'ko': '무료로 시작 · 광고 없음 · 로그인 필요 없음', 'ja': '無料で始められます · 広告なし · ログイン不要', 'en': 'Free to start · No ads · No sign-in needed'},
      alts={'ko': ['화질은 옛날 캠코더, 화면은 고양이. 찍으면 추억이 되는 카메라', '톡은 사진, 꾹은 영상. 셔터 하나로 끝', '필터 7종, 옆으로 쓱 넘겨요. 홈비디오·흑백은 무료', '초록빛 나이트샷도 있어요. 찍은 건 Instagram 스토리로 바로 공유', '일회용 카메라 감성. 플래시 터진 듯 밝고 따뜻하게', '디카 느낌 그대로. 선명하고 쨍한 색감', '필름 느낌 그대로. 빛바랜 색과 필름 스크래치', '지지직 글리치도 있어요. 색이 갈라지는 글리치 화면'], 'en': ['Old-camcorder look, cat-themed screen! Shots that feel like memories', 'Tap for photos, hold for videos! One shutter does it all', '7 filters, just swipe! Home Video and B&W are free', 'Even a green Night Shot! Share straight to Instagram Stories', 'Disposable camera vibes! Bright, warm, flash-lit look', 'That classic digicam look! Crisp, punchy colors', 'Film look, just like that! Faded color and film scratches', 'Glitch filter, too! A glitchy, color-splitting picture'], 'ja': ['昔のビデオカメラ画質、画面はねこデザイン。撮るだけで思い出になるカメラ', 'タップで写真、長押しで動画。シャッターひとつでOK', 'フィルター7種類、スワイプで切り替え。ホームビデオとモノクロは無料', '緑色のナイトショットもあります。Instagramストーリーにすぐ共有', '使い捨てカメラ風に撮れます。フラッシュを焚いたような明るさ', 'デジカメ風に撮れます。くっきり鮮やかな色合い', 'フィルム写真のような仕上がり。色あせた風合いとフィルムの傷', 'グリッチ加工もあります。色がずれるグリッチ画面']},
      legal={'privacy': {'ko': '/nyancorder/privacy.html', 'ja': '/ja/nyancorder/privacy.html', 'en': '/en/nyancorder/privacy.html'}},
      faq={"ko": "<h3>무료로 쓸 수 있나요?</h3>\n<p>홈비디오·흑백 필터는 무료예요. 나머지 5종도 써 볼 수 있지만, 구매하기 전까지는 사진과 영상에 로고가 붙어요. 한 번 구매하면 7종 모두 로고 없이 계속 쓸 수 있어요.</p>\n<h3>사진과 영상은 어떻게 찍나요?</h3>\n<p>셔터를 톡 누르면 사진, 꾹 누르고 있으면 영상이 찍혀요. 폰을 가로로 들면 가로로 찍혀요.</p>\n<h3>찍은 건 어디에 저장되나요?</h3>\n<p>아이폰의 사진 앱에 저장돼요. 필터는 기기 안에서 입혀지고, 서버로는 보내지 않아요.</p>\n<h3>인스타그램 스토리에 바로 올릴 수 있나요?</h3>\n<p>네. 찍은 뒤 Instagram 스토리 버튼을 누르면 인스타그램으로 바로 넘어가요.</p>",
           "ja": "<h3>無料で使えますか？</h3>\n<p>ホームビデオとモノクロのフィルターは無料です。ほかの5種類も試せますが、購入するまでは写真と動画にロゴが入ります。一度購入すれば、7種類すべてをロゴなしでずっと使えます。</p>\n<h3>写真と動画はどうやって撮りますか？</h3>\n<p>シャッターをタップすると写真、長押しすると動画が撮れます。スマホを横にすると横向きで撮れます。</p>\n<h3>撮ったものはどこに保存されますか？</h3>\n<p>iPhoneの写真アプリに保存されます。フィルターは端末の中でかけられ、サーバーには送りません。</p>\n<h3>Instagramのストーリーズにすぐ投稿できますか？</h3>\n<p>はい。撮影後にInstagramストーリーのボタンを押すと、Instagramにそのまま移動します。</p>",
           "en": "<h3>Is it free?</h3>\n<p>The Home Video and B&amp;W filters are free. You can try the other five too, but a logo is added to your photos and videos until you buy them. One purchase unlocks all seven without the logo, for good.</p>\n<h3>How do I take photos and videos?</h3>\n<p>Tap the shutter for a photo, or hold it to record a video. Turn your phone sideways to shoot in landscape.</p>\n<h3>Where are my shots saved?</h3>\n<p>In the Photos app on your iPhone. Filters are applied on your device, and nothing is sent to a server.</p>\n<h3>Can I post straight to Instagram Stories?</h3>\n<p>Yes. After you shoot, tap the Instagram Story button and it opens right in Instagram.</p>"},
      meta={'released': '', 'platform': 'iOS', 'price': {'ko': '무료 · 전체 필터 한 번 구매', 'ja': '無料 · 全フィルターは買い切り', 'en': 'Free · all filters with a one-time purchase'}},
      pills=['iPhone · iOS 17+', '한국어 · English · 日本語'],
      ko=dict(name='냥코더', kind='레트로 캠코더 카메라', lead='옛날 캠코더로 찍은 듯한 사진과 영상을 찍어요. 필터 7종을 옆으로 넘기며 골라요.',
              say='찍기만 해도 추억 느낌이다냥',
              how='셔터를 톡 누르면 사진, 꾹 누르면 영상이 찍혀요. 홈비디오·흑백·일회용·디카·필름·나이트샷·지지직, 필터 7종을 옆으로 넘기며 고를 수 있어요. 찍은 사진과 영상은 사진 앱에 저장되고, Instagram 스토리로 바로 공유할 수 있어요. 폰을 가로로 들면 가로로 찍혀요.',
              note=''),
      ja=dict(name='ニャンコーダー', title_size='38px', kind='レトロなビデオカメラ', lead='昔のビデオカメラで撮ったような写真と動画が撮れます。',
              say='撮るだけで思い出っぽくなるにゃ',
              how='シャッターをタップすると写真、長押しすると動画。ホームビデオ・モノクロ・使い捨て・デジカメ・フィルム・ナイトショット・グリッチの7種類のフィルターを、横にスワイプして選べます。撮った写真と動画は写真アプリに保存され、Instagramのストーリーズにもすぐ共有できます。スマホを横にすると横向きで撮れます。',
              note='アプリは韓国語・英語・日本語に対応しています。'),
      en=dict(name='Nyancorder', kind='Retro camcorder camera', lead='Take photos and videos that look like they came from an old camcorder. Swipe through 7 filters.',
              say='Every shot feels like an old memory, meow',
              how='Tap the shutter for a photo, hold it for a video. Swipe through 7 filters: Home Video, B&W, Disposable, Digicam, Film, Night Shot and Glitch. Your shots are saved to the Photos app and can go straight to Instagram Stories. Turn your phone sideways to shoot in landscape.',
              note='The app is available in Korean, English and Japanese.')),
]

SITE = 'https://nyangnyangbit.com'
OG_LOCALE = {'ko': 'ko_KR', 'ja': 'ja_JP', 'en': 'en_US'}

def head(lang, title, desc, depth, path='', image=None, noindex=False):
    up = '../' * depth
    # 같은 페이지의 다른 언어판(hreflang)과 대표 주소(canonical) — 검색이 언어판을 한 묶음으로 보고, 공유 링크의 주소가 하나로 모인다
    url = f'{SITE}{PREFIX[lang]}{path}'
    alts = ''.join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{PREFIX[l]}{path}">\n' for l in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{SITE}/{path}">\n'
    # 카카오톡·인스타·X에 링크를 올릴 때 뜨는 카드. 앱 페이지는 1200x630 이미지(assets/og), 앱 아이콘만 있으면 작은 카드
    share = (f'<meta property="og:image" content="{SITE}/{image}">\n<meta name="twitter:card" content="{"summary_large_image" if image.startswith("assets/og/") else "summary"}">\n' if image else '<meta name="twitter:card" content="summary">\n')
    share += ('<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n' if image and image.startswith('assets/og/') else '')
    hand = {'ko': 'Gowun+Batang:wght@700', 'ja': 'Zen+Old+Mincho:wght@700', 'en': 'Gowun+Batang:wght@700'}[lang]
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
{'<meta name="robots" content="noindex">\n' if noindex else ''}<link rel="canonical" href="{url}">
{alts}<meta property="og:type" content="website">
<meta property="og:site_name" content="{UI[lang]['studio']}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{OG_LOCALE[lang]}">
{share}<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family={hand}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="/style.css?v={ver('style.css')}">
<script src="/theme.js?v={ver('theme.js')}"></script>
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
        if a['slug'] == current or a.get('hidden'): continue
        out.append(f"""    <a class="card" href="{p}{a['slug']}/" style="--rot:{('-2deg', '1.6deg', '-1deg')[i % 3]}; --poster:{a['poster']}">
      <span class="tape"></span>
      <span class="win"><img src="/{a['icon']}" alt="" width="200" height="200"></span>
      <span class="lab"><b>{escape(t['name'])}</b>{escape(t['kind'])}{' · ' + UI[lang]['soon'] if a.get('teaser') else ''}</span>
    </a>""")
    n, k = UI[lang]['next_app']
    out.append(f"""    <span class="card soon" style="--rot:1.2deg; --poster:#f3f1ec"><span class="tape"></span><span class="win"><span class="q">?</span></span><span class="lab"><b>{n}</b>{k}</span></span>""")
    return f'<div class="cards{" small" if small else ""}">\n' + '\n'.join(out) + '\n<img class="sitter" src="/assets/cat.png" alt=""></div>'

def footer(lang):
    return f"""<footer class="foot"><span>© 2026 NyangNyangBit</span><a href="mailto:{EMAIL}">{EMAIL}</a></footer>
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
        store = ''.join(f'<a class="btn" href="{h.replace('{cc}', STORE_CC[lang]).replace('{hl}', lang)}">{escape(n)}</a>' for n, h in a['store']) or f'<span class="pill">App Store · {u["soon"]}</span>'
        store += ''.join(f'<span class="pill">{escape(n)} · {u["soon"]}</span>' for n in a.get('soon_store', []))
        legal = ''.join(f'<a href="{pick(h, lang)}">{u[k]}</a>' for k, h in a['legal'].items())
        faq = ''
        if 'faq' in a:
            # 질문(h3)+답(p) 쌍을 눌러서 여는 접이식으로 바꾼다. 본문은 그대로 두고 감싸기만 한다
            qa = re.sub(r'<h3>(.*?)</h3>\n<p>(.*?)</p>', r'<details><summary>\1</summary><p>\2</p></details>', a['faq'][lang], flags=re.S)
            faq = f'<section class="faq"><h2>{u["faq"]}</h2>\n' + qa + '\n</section>'
        # 출시 전 앱(store가 비어 있음)은 누를 곳이 없으니 하단 바를 만들지 않는다
        cta_bar = f'<div class="cta-bar away" aria-label="{u["get"]}">{store}</div>' if a['store'] else ''
        alts = a.get('alts', {}).get(lang, [])
        # 스크린샷을 본 사람이 설치를 망설이는 자리에 믿을 근거 세 가지를 글만으로 보여 준다(카드·아이콘 없음). 출시 전 앱은 약속할 게 없어 만들지 않는다
        promise = ''
        # 숨김 앱은 출시 때 모습 그대로 미리 만들어 두는 페이지라 보여 준다
        if a.get('promise') and (a['store'] or a.get('hidden')):
            promise = '<ul class="promise">' + ''.join(f'<li><b>{escape(h)}</b><span>{escape(d)}</span></li>' for h, d in a['promise'][lang]) + '</ul>'
        free_line = f'<p class="free">{escape(a["free"][lang])}</p>' if a.get('free') and a['store'] else ''
        # 스크린샷 띠 아래의 이전/다음 + 현재 위치(main.js가 움직인다). 출시 전 앱처럼 띠가 비면 만들지 않는다
        chev = lambda d: f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{d}"/></svg>'
        shots_nav = '' if a.get('teaser') or not shots else f'<div class="shots-nav"><button type="button" class="prev" aria-label="{u["prev"]}" disabled>{chev("M15 5l-7 7 7 7")}</button><span class="count" aria-live="polite">1 / {len(shots)}</span><button type="button" class="next" aria-label="{u["next"]}">{chev("M9 5l7 7-7 7")}</button></div>'
        note = f'<p class="note">{escape(t["note"])}</p>' if t['note'] else ''
        write(f'{base}{a["slug"]}/index.html', head(lang, f"{t['name']} — {t['kind']} · {u['studio']}", t['lead'], 1, f"{a['slug']}/", a.get('og', a['icon']).format(lang=lang), noindex=a.get('hidden')) + header(lang, f"{a['slug']}/") + f"""<main class="proj" style="--poster:{a['poster']}">
  <aside class="side">
    <div class="head">
    <div class="titlebar"><img class="app-icon" src="/{a['icon']}" alt="" width="64" height="64"><h1 class="title"{f' style="font-size:{t["title_size"]}"' if t.get('title_size') else ''}>{escape(t['name'])}</h1></div>
    <p class="kind">{escape(t['kind'])}</p>
    <p class="lead">{escape(t['lead'])}</p>
    {note}
    <div class="cta">{store}</div>
    {free_line}
    </div>
    <div class="more">
    <p class="say"><img src="/assets/cat.png" alt="" width="40" height="40"><span>{escape(t['say'])}</span></p>
    {'' if a.get('teaser') else f"<h2>{u['how']}</h2>\n    <p>{escape(t['how'])}</p>"}
    <h2>{u['platforms']}</h2>
    <div class="pills">{''.join(f'<span class="pill">{escape(x)}</span>' for x in a['pills'] + [pick(m['released'], lang), pick(m['price'], lang)] if x)}</div>
    <p class="legal">{legal}<a href="mailto:{EMAIL}">{u['contact']}</a></p>
    </div>
  </aside>
  <div class="main">
    <div class="shots">{'' if a.get('teaser') else ''.join(f'<figure class="shot" style="--rot:{("-1.5deg", "1.2deg", "-0.8deg", "1.6deg", "-1.2deg")[i % 5]}"><span class="tape"></span><img src="/{s}" alt="{escape(alts[i] if i < len(alts) else t["name"])}" loading="lazy"></figure>' for i, s in enumerate(shots))}</div>
    {shots_nav}
    {promise}
    {faq}
    <section class="others" aria-label="{u['others']}"><h2>{u['others']}</h2>
{cards(lang, a['slug'], small=True)}
    </section>
  </div>
</main>
{cta_bar}
""" + footer(lang))

    # ── 소개: 왼쪽에 연락처·앱 목록, 오른쪽에 큰 한마디·만드는 방식·앱 폴라로이드 ──
    sns = ''.join(f'<a href="{h}">{n}</a>' for n, h in SNS if h)
    sns = f'<h2>{u["sns_h"]}</h2><p class="links">{sns}</p>' if sns else ''
    app_pills = ''.join(f'<a class="pill" href="{PREFIX[lang]}{a["slug"]}/">{escape(a[lang]["name"])}</a>' for a in APPS if not a.get('hidden'))
    privacy = ''.join(f'<a href="{pick(a["legal"]["privacy"], lang)}">{escape(a[lang]["name"])}</a>' for a in APPS if 'privacy' in a['legal'] and not a.get('hidden'))
    ways = ''.join(f'<li><b>{escape(h)}</b><p>{escape(t)}</p></li>' for h, t in u['ways'])
    write(f'{base}about/index.html', head(lang, f"{u['about_h']} · {u['studio']}", u['about_p'][0], 1, 'about/') + header(lang, 'about/') + f"""<main class="proj about">
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
