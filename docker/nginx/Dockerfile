FROM nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

RUN apt update
RUN apt install -y libjs-bootstrap4 fonts-font-awesome libjs-jquery libjs-popper.js libjs-jquery-datatables

RUN mkdir /srv/media
RUN mkdir /srv/static
