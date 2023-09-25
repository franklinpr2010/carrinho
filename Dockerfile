FROM python:3.8
COPY requirements.txt /carrinhoapp/requirements.txt
WORKDIR /carrinhoapp
RUN pip install -r requirements.txt
COPY . /carrinhoapp
ENTRYPOINT ["python"]
CMD ["app.py"]