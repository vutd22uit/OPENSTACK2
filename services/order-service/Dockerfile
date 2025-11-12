FROM python:3.11-slim
RUN groupadd -r orderservice && useradd -r -g orderservice orderservice
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=orderservice:orderservice . .
USER orderservice
ENV PORT=5003
EXPOSE 5003
CMD ["python", "app.py"]
