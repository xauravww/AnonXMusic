FROM nikolaik/python-nodejs:python3.10-nodejs19

# Install ffmpeg
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY . /app/

# Set working directory
WORKDIR /app/

# Install Python dependencies
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Expose port 5000 (assuming your application listens on this port)
EXPOSE 5000

# Command to run the application
CMD ["bash", "start"]
