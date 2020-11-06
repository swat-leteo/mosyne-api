FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
  cd /usr/local/bin && \
  ln -s /opt/poetry/bin/poetry && \
  poetry config virtualenvs.create false

# Install wkHTMLtoPDF toolkit
ENV WKHTML2PDF_VERSION='0.12.4'

RUN sudo apt-get install -y openssl build-essential xorg libssl-dev && \
  wget "https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/${WKHTML2PDF_VERSION}/wkhtmltox-${WKHTML2PDF_VERSION}_linux-generic-amd64.tar.xz" && \
  tar -xJf "wkhtmltox-${WKHTML2PDF_VERSION}_linux-generic-amd64.tar.xz" && \
  cd wkhtmltox && \
  sudo chown root:root bin/wkhtmltopdf && \
  sudo cp -r * /usr/

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY ./app /app
