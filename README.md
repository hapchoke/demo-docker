# shopping 
ecommerceのデモサイトです。  
ecサイトの機能を楽しむことができます。  
https://ecommerce-py-haruki.herokuapp.com/
## paymentのクレジット番号
```
成功   4242 4242 4242 4242
失敗   4000 0025 0000 3155
      4000 0000 0000 9995
```
# 使用技術
- Django 4.0.3
- Python 3.10.4
- Heroku/heroku-postgresql
- Docker/docker-compose/nginx,postgresql,gunicorn
- AWS/S3
- Bootstrap/html/css
- stripe
- CircleCi
# インフラ構成図
![This is an image](./media/read.jpg)
- dockerで開発し、githubのmainブランチにpushするとcircleciが自動でデプロイする。
- 初めはpythonの仮想環境を利用していたが、psycopg2でエラーが起こり、osの依存関係を解消するため、dockerを利用。deployはfargateを使用していたが料金が発生してしまったためherokuに変更した。
- 画像ファイルはawsのS3上のファイルに保存し、取り出して利用している。
# 機能一覧
- サインアップ、ログイン、ログアウト
- カテゴリー検索、文字検索
- ページネーション
- アドレス登録、自動入力
- 郵便番号から住所自動入力
- 注文、カート

