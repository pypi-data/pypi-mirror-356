FROM ghcr.io/nvidia/jax:jax-2025-06-01
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

ARG USERNAME=ubuntu
RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && mkdir /commandhistory \
    && touch /commandhistory/.bash_history \
    && chown -R $USERNAME /commandhistory \
    && echo "$SNIPPET" >> "/home/$USERNAME/.bashrc"


RUN mkdir -p /home/$USERNAME/.pip \
    && echo '[global]' > /home/$USERNAME/.pip/pip.conf \
    && echo 'index-url = https://pypi.tuna.tsinghua.edu.cn/simple' >> /home/$USERNAME/.pip/pip.conf \
    && echo 'trusted-host = pypi.tuna.tsinghua.edu.cn' >> /home/$USERNAME/.pip/pip.conf

ENV LC_ALL en_US.UTF-8
