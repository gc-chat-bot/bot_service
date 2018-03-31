FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY infopuls_crawler ./
COPY texts ./


COPY . .

EXPOSE 3001

CMD ["./start_service.sh" ]