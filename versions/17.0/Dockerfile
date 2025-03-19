FROM python:3.9-buster

# --- Troubleshooting Stage: Find libxcb or Alternatives (Temporary) ---
# This stage is ONLY for finding the correct package name. It won't be part of the final image.
FROM python:3.9-buster as dependency-finder

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

# Search for libxcb-dev and related packages.  The output of this command is KEY.
RUN apt-cache search libxcb

# Install fallback X11 dev libraries (in case we can't find a specific libxcb-dev).
RUN apt-get install -y --no-install-recommends libx11-dev libxext-dev


# --- Main Odoo Stage ---
# This is the stage that builds the actual Odoo image.
FROM python:3.9-buster

# Install system dependencies.  REPLACE placeholder with the correct package name(s)
# found in the dependency-finder stage.
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

# Clone Odoo
WORKDIR /opt
RUN git clone https://github.com/odoo/odoo.git --branch 17.0 --single-branch odoo

# Install Odoo's Python dependencies
WORKDIR /opt/odoo
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
