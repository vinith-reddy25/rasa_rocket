# Extend the official Rasa SDK image
FROM rasa/rasa:latest-full

# Copy any additional custom requirements, if necessary (uncomment next line)
COPY ./requirements.txt /app

USER root

# Install extra requirements for actions code, if necessary (uncomment next line)
RUN pip install --no-cache-dir -r /app/requirements.txt

