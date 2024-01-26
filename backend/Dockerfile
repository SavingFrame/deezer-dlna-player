# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code:$PYTHONPATH

# Set work directory
WORKDIR /code


# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir --upgrade pip wheel setuptools
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt
COPY start.sh /start.sh
RUN chmod +x /start.sh
COPY gunicorn_conf.py /gunicorn_conf.py

# Copy project
COPY ./ /code/

# Expose port
EXPOSE 8062

# Run the application:
CMD ["/start.sh"]