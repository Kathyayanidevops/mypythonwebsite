FROM python:3.12-alpine 
WORKDIR /mymovieapp
COPY req.txt .
RUN pip install -r req.txt
COPY . .
CMD ["python", "app.py"]
