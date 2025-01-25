# Dockerイメージ作成
## -tはイメージの名称とタグ名称を指定するオプション name:tagの形式で指定
docker build . -t chatbot:latest

# Dockerイメージ一覧
docker image ls
 
# Docker操作ヘルプ
docker image --help

# Dockerコンテナ作成、起動
docker run -d -p 49500:5000 chatbot

# アクセス先
http://localhost:49500/


# DevContainerの利用
VS CodeでDev Containerをインストール
.devcontainerファイルの設定があるのでコンテナビルドする