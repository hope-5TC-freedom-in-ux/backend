FROM python:3.7.4

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY ./entrypoint.sh /app/entrypoint.sh

COPY ./server.py /app/server.py
COPY ./api.py /app/api.py
COPY ./page.py /app/page.py
COPY ./conf /app/conf
COPY ./game.py /app/game.py

ENTRYPOINT ["sh"]
CMD ["entrypoint.sh"]
