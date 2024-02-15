FROM python:3.11.7

# Set the working directory
WORKDIR /app

COPY requirements.txt /app/
COPY *.py /app/

# Install dependencies using apt-get
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --assume-yes -y \
    poppler-utils \
    swig \
    libgl1-mesa-glx \
    libleptonica-dev \
    tesseract-ocr \
    libtesseract-dev \
    python3-pil \
    tesseract-ocr-eng \
    tesseract-ocr-fra \
    tesseract-ocr-script-latn \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir --upgrade setuptools \
    && pip3 install --no-cache-dir pip-tools \
    && pip3 install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip*

# Copy your application code to the container
# COPY tokenizers /root/

# comment this when pushing to git
WORKDIR /app/

CMD ["streamlit", "run", "app.py"]

EXPOSE 8501
