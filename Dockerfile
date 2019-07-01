FROM lambci/lambda:build-python3.7

LABEL maintainer="jkatzbrown@elizabethwarren.com"

RUN echo ' \
      python -m venv /app/venv && \
      source /app/venv/bin/activate && \
      pip install -U invoke pip zappa && \
      pip install -r /app/requirements-dev.txt \
    ' >> /root/.bashrc

# Fancy prompt to remind you are in zappashell
RUN echo 'export PS1="\[\e[36m\]zappashell>\[\e[m\] "' >> /root/.bashrc

CMD ["bash"]
