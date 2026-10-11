# 豆莢浪歌 — v60 現況盤點、競品使用者研究、Persona 與 SD 洞察
（2026-10-11 整理；數字皆附來源，查無資料者標註「無公開資料」。標 ⚠ 者為低可信度二手彙整站，僅供參考）

## 1. v60 原型現況（/workspace/v60）
**實際畫面：單頁三步驟**
- ① 錄音或上傳：開始錄音 / 停止並轉換 / 上傳音檔 / 只載入 MIDI 配伴奏；狀態文字列
- ② 播放：旋律＋伴奏、只聽旋律、停止；勾選「小聲播放原聲」「自動找調（關＝固定 B♭ 小調）」
- ③ 下載：旋律 MIDI、旋律＋伴奏 MIDI；下方「音符清單」表格（開始秒/長度秒…）

**真的有做（可運作）**
- 瀏覽器內 哼唱→MIDI（演算法 A：不搶拍、不重疊），全本地處理不上傳
- 自動伴奏：鋼琴＋尼龍吉他（Tone.js＋CDN 音色），風格只有「悲傷」一種；可自動找調
- Python 版 v60.py / accomp.py 可產 MP3（含/不含原聲），有測試與比對報告

**尚未存在（概念/佔位）**
- 降噪、歌詞保留/辨識、RVC 換聲（伺服器排隊）、圖片幻燈片影片、社群分享、接唱/Remix、豆莢樹、裝置綁定身分、多語系 —— 都不在 v60 中

**UX 痛點**
- 工程導向用語：「MIDI」「演算法 A」「音符清單」「B♭ 小調」對一般年輕使用者無意義
- 產出物是 MIDI 檔下載 → 手機上幾乎無法使用/分享；缺少「聽到成品＋一鍵分享」的爽點
- 歌聲變鋼琴 → 使用者自己的聲音與歌詞消失，情感連結斷掉（原聲只是「小聲」選項）
- 錄音前無引導（哼多久、哼什麼、靠近麥克風）、無倒數、無即時音高/音量回饋
- 只有悲傷風格，無選擇；無預覽前的等待/進度感
- 依賴 CDN、需 https；錄音失敗/權限被拒時缺少友善說明
- 三步驟排在同一頁，主要 CTA 不突出；手機上按鈕多且平權

## 2. 競品使用者研究
### 台灣／華語
- **歡歌 17Sing（台灣在地 K 歌）**：定位「年輕人都愛玩的語音唱歌軟體」，核心是 K 歌房、搶唱、猜歌、家族、送禮、家族寵物打 BOSS；App 分級 17+/18+。年齡/性別分布：無公開資料。機制：家族＋每週賽事＋禮物＝長期黏著；變現靠直播/禮物。 [App Store](https://apps.apple.com/us/app/%E6%AD%A1%E6%AD%8Clive-%E6%89%8B%E6%A9%9Fk%E6%AD%8C%E5%B0%B1%E4%B8%8A%E6%AD%A1%E6%AD%8C/id1481170659)、[Google Play](https://play.google.com/store/apps/details?hl=zh_TW&id=com.subto.osqui)
- **TikTok（台灣）**：2025 初 18+ 廣告受眾 834 萬（成人 41.9%），女 50.9%／男 49.1%，最大族群 25–34。Duet/Stitch/「使用此聲音」是華語圈最大的接唱/混音行為場域；Duet 功能專屬使用者畫像：無公開資料。 [DataReportal Digital 2025 Taiwan](https://datareportal.com/reports/digital-2025-taiwan)
- **全民K歌（騰訊，中國）**：2021 年 1–10 月平均月活約 1.3 億、唱吧約 2,000 萬 [艾媒](https://www.iimedia.cn/c400/82279.html)；2021Q3 移動 K 歌用戶 25 歲以下 31.2%、男 51.3% [智研](https://www.chyxx.com/industry/202201/992812.html)；70 後占 17%，合唱/私信/分享次數高於其他年齡 [36氪](https://m.36kr.com/p/2843504562739586)。機制：微信/QQ 關係鏈分享、合唱（千人合唱）、評分、禮物。勝唱吧的關鍵是社交鏈導流 [簡書](https://www.jianshu.com/p/945ce551b6b0)。
- **唱吧**：2013 年註冊破億，2016 起被全民K歌超越（渗透率下滑）[簡書](https://www.jianshu.com/p/945ce551b6b0)；用戶 30–40 歲占比較大 [南都/比達](https://m.mp.oeeee.com/a/BAAFRD000020200227271454.html)。失敗教訓：缺乏關係鏈、被巨頭生態擠壓。
- **唱鴨（相關參考）**：25 歲以下 82.3%，95 後最喜愛 K 歌 App（85%）；賣點是「多種樂器伴奏彈唱」，95 後偏好古風（65.4%）、嘻哈、二次元 [比達 2019](https://m.mp.oeeee.com/a/BAAFRD000020200227271454.html) → **最接近豆莢「哼唱＋自動伴奏」的年輕人需求證據**。

### 日本
- **nana（最相關）**：多重錄音接力「コラボ」，90 秒上限。2016：15 歲以下 20%、16–18 歲 41%，女 76% [ケータイWatch](https://k-tai.watch.impress.co.jp/docs/news/758609.html)；2017 年調查（6,435 人）：19 歲以下 58.5%、20–24 歲 18.2%，女 76%，認識管道 42.9% 為「朋友介紹」，500 萬註冊 [PR TIMES](https://prtimes.jp/main/html/rd/p/000000024.000011341.html)；10 代女性在 Twitter 掛 nana 帳號互相邀約 [CNET Japan](https://japan.cnet.com/article/35087611/)。「トーク」（說話投稿）也是熱門投稿類型。失敗/困境：舊版 App 直播「nanaパーティー」2024 年因外部因素故障終止 [note](https://note.com/nanamusic/n/n1d50220d49c6)，後重做新版 App。
- **Pokekara**：累計 4,500 萬 DL、MAU 400 萬+ [PR TIMES](https://prtimes.jp/main/html/rd/p/000000011.000106670.html)；2023 年 10 代 16%、20 代 26%、30 代 23%、40 代 20%、50 代 15%（日經クロストレンド，依搜尋摘要）[日經](https://xtrend.nikkei.com/atcl/contents/18/00020/00020/)。機制：AI 評分、投稿、直播＋ライバー事務所。

### 韓國
- **Everysing（에브리싱）**：2019/7 活躍用戶中 女 20 代 16.1%、女 10 代 15.7%、男 30 代 13.1%、男 20 代 12.1% [소마코](https://somako.co.kr/%ec%96%b8%ec%a0%9c-%ec%96%b4%eb%94%94%ec%84%9c%eb%82%98-%ec%8a%a4%eb%a7%88%ed%8a%b8-%eb%85%b8%eb%9e%98%eb%b0%a9-%ec%95%a0%eb%b8%8c%eb%a6%ac%ec%8b%b1-%ec%95%b1/)。近期資料：無公開資料。

### 英語／全球
- **Smule**：受眾「年輕且偏女性」[Appfigures](https://appfigures.com/resources/app-teardowns/smule-karaoke)；2022/12 大規模裁員 [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7018308583234633729)，員工數下滑 [Revelio](https://www.reveliolabs.com/companies/smule/employees)。⚠「東南亞 >40%」等數字來自彙整站，不可信。教訓：訂閱牆＋版權成本、被短影音取代。
- **StarMaker**：註冊 3.1 億，強在東南亞/中東/南美；靠賽事 IP（Supernova 盲聽投票）、社群、禮物 [新浪](https://finance.sina.com.cn/roll/2025-08-29/doc-infnscia5838924.shtml)。年齡性別：無公開資料。
- **BandLab**：2024 年 1 億註冊；多數 24 歲以下、美國約 30%、多在手機創作、內建 Voice to MIDI [Sound Connections](https://soundconnections.io/sound-connections/39-the-future-of-music-at-bandlab-technologies-dani-deahl/)、[MBW](https://www.musicbusinessworldwide.com/music-making-app-bandlab-surpasses-100-million-users/)。
- **Suno**：投資簡報稱核心用戶偏男性、25–34 歲、每次約 20 分鐘、每日約 700 萬首 [Blunt](https://bluntmag.com.au/music/suno-users-create-7-million-songs-per-day-according-to-250m-investor-pitch-deck/)；流量估計 18–24 31.4%、男 65% ⚠[AI NavHub](https://ainavhub.com/ai/suno-com/analysis)。
- **Udio**：使用者畫像無公開資料。
- **Voicemod**：自稱 7,200 萬用戶；核心 16–35 遊戲玩家、實況主、VRChat ⚠[彙整](https://aitechmodel.com/voicemod-statistics-by-usage-demographics-and-info-2026/)。
- **Google Hum to Search**：使用量與人口統計無公開資料（僅證明「哼一段」是大眾熟悉的行為）。

### 跨產品共通模式
- 年輕、偏女性的是「社交唱歌/接唱」（nana、Smule、Everysing 女 10–20 代）；偏男性 25–34 的是「AI 生成/製作」（Suno）
- 成長靠既有關係鏈（全民K歌×微信、nana 朋友介紹 42.9%＋Twitter）
- 長期留存靠 群體（家族/社群）＋ 週期活動（賽事、每週搶唱）＋ 被回應（拍手、接唱）
- 失敗：版權/訂閱成本（Smule）、無社交鏈（唱吧）、技術債拖垮社群功能（nana パーティー）

## 3. Persona
1. **小柔，16 歲高二女生（台中）** — 參考 nana/Everysing 主力。睡前躺床、補習回家後開；想被聽見但不敢露臉。會接朋友的豆莢、合聲、錄一句「トーク」式旁白。動機：同好圈、被回應。
2. **阿哲，22 歲大學生／業餘創作（台北）** — 參考 BandLab、唱鴨、Suno。洗澡/走路時腦中冒旋律，怕忘記先哼下來；要「變成像樣的 demo」丟 IG 限動、Threads。動機：創作自我認同、作品感。
3. **Mia，27 歲上班族 TikTok 重度使用者** — 參考 TikTok 台灣 25–34 主力。通勤/午休滑到好玩聲音就想「接一段」或用 RVC 變聲搞笑；作品一次性，追求梗與分享數。動機：迷因、社交貨幣。
4. **Kenji／小夏，19–24 歲 ACG/VTuber 圈（台＋日）** — 參考 nana 二次元與唱鴨古風/二次元偏好。圍繞角色、OC、團體企劃接龍，長期養一棵豆莢樹。動機：共同創作企劃、圈內地位。

## 4. SD 洞察（獲客＋留存）
**獲客**
- 分享物必須是「影片＋原聲」而非 MIDI；影片內嵌「接唱我」QR/連結，開啟即可直接哼（免註冊是巨大優勢，零摩擦）
- 主攻 IG 限動/Reels、Threads、TikTok、LINE 群組（台灣關係鏈）；仿 nana「朋友邀約」— 接唱邀請本身就是獲客
- 種子：台灣大學熱音/阿卡貝拉社、ACG 同人圈、VTuber 企劃；每週主題（例「把這段旋律接下去」）
- 降低害羞門檻：可只哼不唱詞、可換聲（RVC）、可匿名
**留存**
- 被回應的通知迴圈：「你的豆莢被接了 3 次」（RVC 10–20 分鐘等待也做成通知/回訪理由）
- 豆莢樹可視化＝長期收集與成長感（年輕人「長期遊玩」）；個人「豆莢園」、樹的分支徽章
- 小群體：私密樹/朋友圈（仿家族），週期活動與季賽
- 風險：裝置綁定 → 換機/清快取即失去作品，需「備份碼/綁 LINE」選項；未成年比例高 → 審核與隱私設計；避免依賴版權歌曲（Smule 教訓），原創哼唱正是差異化
