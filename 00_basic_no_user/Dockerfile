FROM python:3.8-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Expose the port Gunicorn will listen on (you can change this if needed)
EXPOSE 8080

# The command to start Gunicorn
CMD ["gunicorn", "-w", "1", "--bind", "0.0.0.0:8080", "server:app"]
