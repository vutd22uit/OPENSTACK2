FROM python:3.11-slim
RUN groupadd -r gateway && useradd -r -g gateway gateway
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=gateway:gateway . .
USER gateway
ENV PORT=8080
EXPOSE 8080
CMD ["python", "app.py"]
