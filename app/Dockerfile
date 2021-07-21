# Extend the official Rasa SDK image
FROM rasa/rasa-sdk

# Copy actions folder to working directory
COPY ./actions /app/actions

# Copy any additional custom requirements, if necessary (uncomment next line)
COPY ./requirements.txt /app

USER root

# Install extra requirements for actions code, if necessary (uncomment next line)
RUN pip install -r /app/requirements.txt
RUN python -m spacy download en_core_web_md

