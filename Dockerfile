FROM python:alpine

ENV APP_DIR_NAME backend
ENV APP_PATH /opt/$APP_DIR_NAME

RUN apk update \
  && apk add --virtual build-deps gcc make python3-dev musl-dev postgresql-dev postgresql libffi-dev
RUN apk add --no-cache libstdc++ && \
    apk add --no-cache g++ && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    pip3 install numpy && \
    pip3 install pandas

#Pillow requirements
RUN apk update \
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

#installing django
COPY requirements.txt /
RUN pip install --default-timeout=100 -r requirements.txt
RUN rm requirements.txt

#adding entrypoint scripts
COPY docker-entrypoint.sh /
COPY create_superuser.py /
COPY create_groups.py /
COPY setup_perms.py /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

#backup year setup
COPY remove_models.py /
COPY backup_year.sh /
RUN chmod +x /backup_year.sh

#adding the django project
RUN mkdir -p $APP_PATH
COPY ./backend $APP_PATH