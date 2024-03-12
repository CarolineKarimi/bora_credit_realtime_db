FROM python:3.7
WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt 
EXPOSE 8005


ENTRYPOINT ["streamlit","run","--server.port","8005"]
CMD ["bora_credit_dashboard.py"]

