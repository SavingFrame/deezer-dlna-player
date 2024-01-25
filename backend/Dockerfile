# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code:$PYTHONPATH

# Set work directory
WORKDIR /code

RUN apk add gcc musl-dev

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip wheel setuptools
RUN pip install -r requirements.txt

# Copy project
COPY ./ /code/

# Expose port
EXPOSE 8062

# Run the application:
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8062"]