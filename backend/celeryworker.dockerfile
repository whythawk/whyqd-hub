FROM python:3.11
WORKDIR /app/
ARG \
  HATCH_VERSION=1.14.2 \
  PIPX_VERSION=1.2.0
ENV \
  C_FORCE_ROOT=1 \
  HATCH_ENV_TYPE_VIRTUAL_PATH=.venv \
  HATCH_VERSION=$HATCH_VERSION \
  PATH=/opt/pipx/bin:/app/.venv/bin:$PATH \
  PIPX_BIN_DIR=/opt/pipx/bin \
  PIPX_HOME=/opt/pipx/home \
  PIPX_VERSION=$PIPX_VERSION \
  PYTHONPATH=/app
COPY ./app/ /app/
RUN python -m pip install --no-cache-dir --upgrade pip "pipx==$PIPX_VERSION"
RUN pipx install "hatch==$HATCH_VERSION"
RUN hatch env prune && hatch env create production
RUN chmod +x /app/worker-start.sh

CMD ["bash", "worker-start.sh"]

