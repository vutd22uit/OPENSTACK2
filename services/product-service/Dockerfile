FROM python:3.11-slim
RUN groupadd -r prodservice && useradd -r -g prodservice prodservice
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=prodservice:prodservice . .
USER prodservice
ENV PORT=5002
EXPOSE 5002
CMD ["python", "app.py"]
