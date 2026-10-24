FROM nginx:1.31-alpine

RUN apk --no-cache upgrade brotli-libs

COPY index.html /usr/share/nginx/html/index.html
COPY nginx.conf /etc/nginx/conf.d/default.conf
