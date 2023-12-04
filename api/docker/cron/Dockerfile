# Dockerイメージのベースとして公式のPHPイメージを使用
FROM php:8.1.17-fpm-alpine3.17

# cronパッケージのインストール
RUN apk --no-cache add busybox-suid

# cron設定ファイルのコピー
COPY ./docker/cron/cron.root /etc/crontabs/root

# フォアグラウンドでcronを起動する
CMD ["crond", "-f"]


