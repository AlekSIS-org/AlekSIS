FROM nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

RUN mkdir /srv/media
RUN mkdir /srv/static
RUN mkdir /srv/javascript
