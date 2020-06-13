FROM python:3.8.2-alpine3.11

ENV APP_DIR_NAME backend
ENV APP_PATH /opt/$APP_DIR_NAME

RUN pip install --upgrade pip

RUN apk update \
  && apk add --virtual build-deps gcc make python3-dev musl-dev postgresql-dev postgresql libffi-dev
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

#adding the django project
RUN mkdir -p $APP_PATH
COPY ./backend $APP_PATH
