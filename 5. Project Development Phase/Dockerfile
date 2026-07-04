# Rising Waters — Flood Prediction Web App
# Build & run:
#   docker build -t rising-waters .
#   docker run -p 5000:5000 rising-waters
#
# Deploy to IBM Cloud Code Engine (after pushing the image to a registry):
#   ibmcloud ce application create --name rising-waters --image <your-registry>/rising-waters --port 5000

FROM python:3.11-slim

WORKDIR /srv

# Install dependencies first (better layer caching)
COPY app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model bundle and the Flask app
COPY model/ ./model/
COPY app/ ./app/

WORKDIR /srv/app
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
