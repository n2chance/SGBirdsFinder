FROM python:3.13
COPY . /
RUN pip install -r requirements.txt
RUN python setup.py

EXPOSE 5000

CMD ["python", "app/app.py"]