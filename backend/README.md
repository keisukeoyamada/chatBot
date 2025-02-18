# Docker(GUI)
## DevContainerの利用
    1. Dockerアプリが起動していることを確認
    2. VS CodeでDev Containerをインストール済みなことを確認
    3. .devcontainerファイルの設定に従ってコンテナビルドする
        Ctr + Shift + p コンテナのリビルド


# Docker(手動)
## Dockerイメージ作成
## -tはイメージの名称とタグ名称を指定するオプション name:tagの形式で指定
    docker build . -t chatbot:latest
## Dockerイメージ一覧
    docker image ls
## Docker操作ヘルプ
    docker image --help
## Dockerコンテナ作成、起動
    docker run -d -p 49500:5000 chatbot　
>コンテナ内の 5000 番をホストの 49500 番にマッピング
## アクセス先
    http://localhost:49500/
## 起動してるコンテナ一覧
    docker ps
## コンテナの停止
    docker stop 7b48564dc191

# dockerログ確認（エラーでコンテナ落ちた時など原因確認）
docker logs $(docker ps -q -l)
