FROM python:3.9-slim-buster

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev build-essential libpq-dev libxml2-dev libxslt1-dev \
    libldap2-dev libsasl2-dev libtiff5-dev libjpeg62-turbo-dev \
    zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev libharfbuzz-dev \
    libfribidi-dev libxcb-dev git

# Crear directorios para los addons
RUN mkdir -p /mnt/custom_addons && chmod -R 777 /mnt/custom_addons
RUN mkdir -p /mnt/extra_addons && chmod -R 777 /mnt/extra_addons

# Clonar Odoo
WORKDIR /opt
RUN git clone https://github.com/odoo/odoo.git --branch 17.0 --single-branch odoo

# Instalar dependencias de Python de Odoo
WORKDIR /opt/odoo
RUN pip install --no-cache-dir -r requirements.txt

# Instalar pyright y generar los stubs  <- ¡AQUÍ!
RUN pip install --no-cache-dir pyright
RUN pyright --createstub odoo

# Copiar requirements.txt (para dependencias de módulos personalizados)
COPY requirements.txt /tmp/

# Instalar dependencias de módulos personalizados
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Exponer el puerto de Odoo
EXPOSE 8069

# Comando por defecto
CMD ["python3", "/opt/odoo/odoo-bin", "-c", "/etc/odoo/odoo.conf"]
