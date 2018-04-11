FROM python:3.6

ENV TZ 'Asia/Shanghai'
ENV PYTHONUNBUFFERED '0'

WORKDIR /app

ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple/
COPY . /app

CMD ["python", "bot.py"]