FROM node:18-slim

RUN apt-get update -qq
RUN npm install -g @vue/cli

WORKDIR /app
COPY package.json package.json
# WORKDIR /app/frontend
RUN npm install
# CMD ["/bin/bash"]
# アプリのソースコードをコピー
# COPY . .
# RUN npm install
CMD ["npm", "run", "serve"]
