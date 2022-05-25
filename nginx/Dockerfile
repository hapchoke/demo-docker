FROM  --platform=linux/x86_64 nginx:1.19.0
 
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d


RUN apt-get update && \
    apt-get install -y certbot python-certbot-nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    ln -sf  /usr/share/zoneinfo/Asia/Tokyo /etc/localtime