FROM python:3.9.0-slim
RUN useradd -m app
COPY --chown=app:app . /home/app
RUN pip install -r /home/app/requirements.txt
USER app
WORKDIR /home/app
EXPOSE 8080/tcp
CMD ["python3", "example.py"]