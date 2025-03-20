FROM python:3.10-buster

# --- Troubleshooting Stage (Keep as-is, for now) ---
FROM python:3.10-buster as dependency-finder

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

# Search for libxcb-dev
RUN apt-cache search libxcb

# Install fallback X11 dev libraries
RUN apt-get install -y --no-install-recommends libx11-dev libxext-dev


# --- Main Odoo Stage ---
FROM python:3.10-buster

# Check Python Version (for debugging)
RUN python3 --version

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    build-essential \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    libldap2-dev \
    libsasl2-dev \
    libtiff5-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    git \
    libxcb1-dev \
    && rm -rf /var/lib/apt/lists/*

# Create directories for addons
RUN mkdir -p /mnt/custom_addons && chmod -R 777 /mnt/custom_addons
RUN mkdir -p /mnt/extra_addons && chmod -R 777 /mnt/extra_addons

# Clone Odoo (with --depth 1)
WORKDIR /opt
#RUN git clone https://github.com/odoo/odoo.git --branch 17.0 --single-branch odoo
RUN git clone https://github.com/odoo/odoo.git --branch 17.0 --depth 1 odoo


# Install Odoo's Python dependencies
WORKDIR /opt/odoo

# Upgrade setuptools and wheel *BEFORE* installing requirements.
RUN pip install --no-cache-dir --upgrade setuptools wheel
# Install Cython explicitly
RUN pip install --no-cache-dir Cython
# Pin gevent (add to Odoo's requirements.txt)
#RUN echo "gevent==21.8.0" >> requirements.txt
# --- KEY STEP: Replace gevent version BEFORE installing ---
RUN sed -i 's/^\s*gevent.*$/gevent==22.10.2/' requirements.txt
# ALSO replace greenlet:
RUN sed -i 's/^\s*greenlet.*$/greenlet>=2.0.0/' requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install pyright and generate stubs
RUN pip install --no-cache-dir pyright pre-commit
RUN pyright --createstub odoo

# Install custom module dependencies (if any)
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Expose Odoo's port
EXPOSE 8069

# Default command
CMD ["python3", "/opt/odoo/odoo-bin", "-c", "/etc/odoo/odoo.conf"]