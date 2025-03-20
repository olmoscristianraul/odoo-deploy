# Entorno de Desarrollo Odoo 17 con Docker

Este repositorio proporciona un entorno de desarrollo completo y reproducible para Odoo 17, utilizando Docker y Docker Compose.  Incluye integración continua con GitHub Actions, pre-commit hooks para control de calidad de código, y soporte para debugging con VS Code.

## Prerrequisitos

*   Docker y Docker Compose instalados en tu sistema.  Consulta la documentación oficial de Docker para instrucciones de instalación: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
*   Git instalado.
* Visual Studio Code (Opcional, para debugging)

## Estructura del Proyecto

odoo-deploy/
├── .github/workflows/  <- Workflows de GitHub Actions (CI)
│   ├── ci.yml
│   └── cd.yml          <-  (Opcional, para despliegue continuo)
├── versions/           <- Versiones de Odoo
│   ├── 17.0/
│   │   ├── docker-compose.yml  <-  Define los servicios (Odoo, PostgreSQL)
│   │   ├── Dockerfile         <-  Construye la imagen de Odoo
│   │   ├── odoo.conf          <-  Configuración de Odoo
│   │   ├── requirements.txt   <- Dependencias para módulos personalizados
│   │   └── typings/           <-  (Se genera automáticamente) Stubs para pyright
│   └── ...
├── custom_addons/      <-  Tus módulos personalizados
│   └── my_module/       <-  Ejemplo (puedes eliminarlo)
│       ├── manifest.py
│       ├── models/
│       │   └── models.py
│       └── ...
├── extra_addons/       <- Módulos de terceros (OCA, etc.)
├── .pre-commit-config.yaml <- Configuración de pre-commit
├── pre-commit-docker  <-  Script para ejecutar pre-commit en Docker
├── .gitignore          <- Archivos/directorios ignorados por Git
├── LICENSE             <- Licencia del proyecto
└── README.md           <- Este archivo

## Instalación y Uso

1.  **Clonar el repositorio:**

    ```bash
    git clone <URL_de_tu_repositorio>  # Reemplaza con la URL de TU repositorio
    cd odoo-deploy
    ```

2.  **Instalar los hooks de pre-commit:**

    ```bash
    ./pre-commit-docker install
    ```
    Este paso configura `pre-commit` para que se ejecute *dentro* de un contenedor Docker, asegurando un entorno consistente para las comprobaciones de calidad de código.  No necesitas instalar `pre-commit` localmente.

3.  **Construir y ejecutar los contenedores:**

    ```bash
    cd versions/17.0
    docker-compose up -d --build
    ```

    Esto descargará las imágenes base, clonará Odoo *dentro* del contenedor, instalará las dependencias, y creará los contenedores de Odoo y PostgreSQL.  La primera vez, este proceso puede tardar varios minutos.

4.  **Generar los "stubs" de tipo (para autocompletado en VS Code):**

      ```bash
      docker-compose exec odoo bash -c "pyright --createstub odoo"
      docker cp $(docker-compose ps -q odoo):/opt/odoo/typings ./
      ```
      Estos comandos generan y copian los "stubs" de tipado para Odoo, mejorando el autocompletado y la detección de errores en VS Code.

5.  **Acceder a Odoo:**

    Abre tu navegador y ve a  `http://localhost:8069`.  Crea una nueva base de datos (por ejemplo, `odoo_dev`).  **Importante:** la contraseña maestra por defecto es `@HCsinergia2025` y el usuario y contraseña de la base de datos odoo, y myodoo.  **¡Cámbialas en un entorno de producción!**

6. **Instalar modulos custom**
```bash
    docker-compose run --rm odoo odoo-bin -c /etc/odoo/odoo.conf -d odoo_db -i <nombre_modulo> --stop-after-init


**Instrucciones Paso a Paso (Para el Usuario Final):**

Estas son las instrucciones *simplificadas* que pondrías en el `README.md` principal, asumiendo que el usuario ya tiene Docker y Git instalados:

1.  **Clonar el Repositorio:**

    ```bash
    git clone <URL_DEL_REPOSITORIO>  # Reemplaza con la URL real
    cd odoo-deploy
    ```

2.  **Instalar los Hooks de Pre-commit:**

    ```bash
    ./pre-commit-docker install
    ```

3.  **Construir y Ejecutar:**

    ```bash
    cd versions/17.0
    docker-compose up -d --build
    ```
    La primera vez, este comando tardará porque descarga la imagen base de Python, clona Odoo, e instala las dependencias.  Las siguientes veces será más rápido.

4. **Generar los "stubs" de tipo (para autocompletado en VS Code):**

      ```bash
      docker-compose exec odoo bash -c "pyright --createstub odoo"
      docker cp $(docker-compose ps -q odoo):/opt/odoo/typings versions/17.0/
      ```

5.  **Acceder a Odoo:** Abre un navegador y ve a  `http://localhost:8069`.  Crea una nueva base de datos (por ejemplo, `odoo_dev`).

6. **Instalar un modulo custom**
    ```
    docker-compose run --rm odoo odoo-bin -c /etc/odoo/odoo.conf -d odoo_db -i <nombre_modulo> --stop-after-init
    ```

7. **Actualizar modulos**
docker-compose run --rm odoo odoo-bin -c /etc/odoo/odoo.conf -d odoo_db -u <nombre_modulo> --stop-after-init


**Explicaciones Adicionales (para el desarrollador):**

*   **`pre-commit-docker install`:**  Este comando, *usando el script*, instala los *git hooks*.  Esto hace que `pre-commit` se ejecute *automáticamente* antes de cada commit, *dentro* de un contenedor Docker.  No se necesita ninguna instalación local de `pre-commit`.
*   **`docker-compose up -d --build`:** Construye la imagen (si es necesario, debido a cambios en el `Dockerfile`) y ejecuta los contenedores en segundo plano.
* **Typing:** Los archivos generados por el comando `pyright --createstub odoo` , deben copiarse a una carpeta local.

**Cambios en los archivos (respecto a las versiones anteriores):**

*   **`Dockerfile`:**  Se eliminó la etapa `dependency-finder` (ya no es necesaria). Se eliminó la copia de `requirements.txt` y la instalación de dependencias de módulos personalizados (se hará con volúmenes).  Se agregó la instalación de `pre-commit`. Se usa python 3.10
*   **`docker-compose.yml`:** Se eliminó el `entrypoint`. Se usan volúmenes nombrados.
*   **`ci.yml`:**  Se simplificó el script de CI. Se agregó la ejecución de `pre-commit`. Se usa Python 3.10.
* **`README.md`:** Instrucciones claras y concisas para el usuario final.
* **`launch.json`**: Se configuró el debug.

He simplificado y consolidado las instrucciones, eliminando pasos intermedios que ya no son necesarios y enfocándome en un flujo de trabajo limpio y directo.  He incluido *todos* los archivos necesarios para que el proyecto sea completamente autocontenido y reproducible.