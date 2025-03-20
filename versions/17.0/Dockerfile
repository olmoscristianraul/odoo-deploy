FROM python:3.10-buster as builder

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

# Clone Odoo (with --depth 1 for speed)
WORKDIR /opt
RUN git clone https://github.com/odoo/odoo.git --branch 17.0 --single-branch --depth 1 odoo

WORKDIR /opt/odoo

# --- KEY STEP: Replace gevent and greenlet versions BEFORE installing ---
RUN sed -i 's/^\s*gevent.*$/gevent==22.10.2/' requirements.txt
RUN sed -i 's/^\s*greenlet.*$/greenlet>=2.0.0/' requirements.txt

# Install Odoo's Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install pyright and pre-commit (for stubs and linting)
RUN pip install --no-cache-dir pyright pre-commit

# Generate stubs
RUN pyright --createstub odoo

# --- Final Stage ---
FROM python:3.10-buster
COPY --from=builder /opt/odoo /opt/odoo
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Create the addon directories.
RUN mkdir -p /mnt/custom_addons
RUN mkdir -p /mnt/extra_addons
RUN adduser --system --group odoo  # Create a non-root user
USER odoo

# Expose the port
EXPOSE 8069

# Set the default command.  Run Odoo normally.
CMD ["python3", "/opt/odoo/odoo-bin", "-c", "/etc/odoo/odoo.conf"]