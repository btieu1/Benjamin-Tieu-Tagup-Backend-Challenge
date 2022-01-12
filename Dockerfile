FROM python:3.7
COPY . /exercise
WORKDIR /exercise
RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["exercise.py"]