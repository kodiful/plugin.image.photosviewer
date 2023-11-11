# Kodiアドオン：フォトビューア

macOSの写真アプリケーションで管理されている写真をTV画面で閲覧するためのKodiアドオンです。
写真アプリケーションのデータベースを参照し、撮影日、撮影場所、顔画像認識による人物等にしたがって写真やビデオをブラウズできます。

macOS High Sierra（バージョン10.13）の写真アプリケーション（バージョン3.0）にて動作を確認しています。
最新の写真アプリケーションではデータベースの構成が異なるため動作しません。

はじめに[アドオン設定画面-設定](アドオン設定画面-設定)で写真ライブラリへのパスを設定してください。


## メイン画面

アドオン起動直後にメイン画面が表示されます。

![メイン画面](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/8c0ee9d1-a994-455a-83ce-cc50871ddc68)

### 写真

写真の撮影日にしたがって年月日別にブラウズします。

![撮影日ブラウズ画面](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/8c0ee9d1-a994-455a-83ce-cc50871ddc68)

![撮影日ブラウズ画面](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/66712300-154e-4906-a6c4-7755ac820ae7)

![撮影日ブラウズ画面](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/4e4bcf7d-2ea8-469b-a4e1-922f680eb99c)

![撮影日ブラウズ画面](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/852cfa78-bb75-4a0b-a7a9-d459b20b45b1)

![撮影日ブラウズ画面](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/b3edaaca-6d29-4653-8f67-5992dbe22fcd)

![撮影日ブラウズ画面](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/7ceed763-4062-4b73-8dc1-853ca69a1d07)

### 写真のコンテクストメニュー

撮影日の絞り込み時に、年または月単位にまとめてブラウズできます。

![撮影日ブラウズ画面コンテクストメニュー](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/7ef431e3-6711-4660-8d1c-206332816cc6)

### ピープル

写真からの顔画像認識にしたがって人物別にブラウズします。

### 撮影地

写真に設定されている位置情報にしたがって撮影地別にブラウズします。

![撮影地ブラウズ画面](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/f86e359c-2505-4745-b0c7-f41542aa5edb)

![撮影地ブラウズ画面](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/bb6d2d73-0144-4559-8fe0-bc44e41351ab)

![撮影地ブラウズ画面](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/0a20f8b1-2516-400d-b72e-2a969a8e2c7a)

![撮影地ブラウズ画面](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/d09e4da1-c7ad-4072-9478-c739aaaaa347)

![撮影地ブラウズ画面](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/a88dc006-37fc-41fd-87a6-ea9f0c8ae7fc)

![撮影地ブラウズ画面](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/34eef5ff-67cd-44da-9dc0-2b9324e3ea17)


### 撮影地のコンテクストメニュー

撮影地の絞り込み時に、都道府県や市町村等の地域単位にまとめてブラウズできます。

![撮影地ブラウズ画面コンテクストメニュー](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/240262a9-bace-4685-bdab-4e222eb105ee)

### ビデオ

ビデオをブラウズします。

![ビデオブラウズ画面](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/7cd74462-e9f5-4ae4-92c6-f13af8d5b7ca)

![video-select](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/a27bbcbd-e193-4b2d-b562-7533dde8702f)

### アルバム

写真アプリケーションのアルバムの階層にしたがってブラウズします。

![アルバムブラウズ画面](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/e1524cb4-1410-4636-b1e5-b12d60de1751)

![アルバムブラウズ画面](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/bc55b9af-5714-46e4-bebe-de4de11cba9a)


## アドオン設定画面-設定

![アドオン設定画面](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/add5c124-ce85-4c90-ba72-526b3e26c4f8)

### 写真ライブラリへのパス

写真ライブラリへのパス（デフォルトでは（"/Users/(username)/Pictures/写真ライブラリ.photoslibrary"）を設定してください。


## アドオン設定画面-その他

![アドオン設定画面](https://github.com/kodiful/plugin.image.photosviewer/assets/12268536/cd682ccd-e414-476d-9dda-249a34114c0c)

### HEIC画像の表示

iOS11から採用された写真データの形式HEICは、そのままではKodiで表示できないため、これを表示する方法を「サムネイルで代替」「JPEGに変換」から選択してください。それぞれ以下の特徴があります。

|方法|特徴|
|:---|:---|
|サムネイルで代替|サムネイル画像で置き換えます。表示に時間はかかりませんが、画質はよくありません。|
|JPEGに変換|macOSのsipsコマンドによりHEIC画像をJPEG画像に変換して表示します。変換に時間を要しますが、高画質です。|
|変換しない|HEIF image decoderが利用可能な場合はこれを選択してください。|

### デバッグ

通常はオフにしてください。


