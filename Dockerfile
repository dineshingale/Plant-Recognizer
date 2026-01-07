FROM python:3.9-slim

# 1. Install System Dependencies (Chrome, Node, Netcat)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Chrome & Chromedriver
# Note: In modern slim images, we might use chromium provided by Debian to ensure compat
RUN apt-get update && apt-get install -y chromium chromium-driver

# 3. Install Node.js v20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# 4. Set Workspace
WORKDIR /app

# 5. Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Install Frontend Dependencies (Cached)
COPY Client/package.json Client/package-lock.json ./Client/
RUN cd Client && npm ci

# 7. Copy Project Code
COPY . .

# 8. Set Permissions for Helper Scripts
RUN chmod +x entrypoint.sh

# 9. Default Command
ENTRYPOINT ["./entrypoint.sh"]
