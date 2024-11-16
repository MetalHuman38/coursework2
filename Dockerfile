FROM python:3.9-alpine

LABEL maintainer="metalbrain"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Set working directory
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app

EXPOSE 8080

ARG DEV=false

RUN apk add --update --no-cache nodejs npm

RUN npm install -g npm@latest

RUN python -m venv /py && \
   /py/bin/pip install --upgrade pip && \
   /py/bin/pip install -r /tmp/requirements.txt && \
   if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt; fi && \
   rm -rf /tmp && \
   adduser \
      --disabled-password \
      --no-create-home \
      django-user

ENV PATH="/py/bin:$PATH"

USER django-user

# Default command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]