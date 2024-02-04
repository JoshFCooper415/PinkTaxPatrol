FROM ubuntu:22.04

ARG USERNAME=server-admin
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
# Switch from root to user
USER $USERNAME

RUN sudo apt update && sudo apt upgrade -y
RUN echo "$PWD"

RUN sudo apt install -y git
EXPOSE 5000
RUN sudo apt install -y  python3-pip
WORKDIR /

RUN pip install flask requests pandas xgboost scikit-learn joblib numpy lightbeam flask_CORS

RUN mkdir home/$USERNAME/code
WORKDIR ./home/$USERNAME/code

RUN git clone https://github.com/JoshFCooper415/PinkTaxPatrol.git
WORKDIR ./PinkTaxPatrol
RUN echo "$PWD"
RUN git checkout pythonServer --
WORKDIR ./pythonServer
RUN echo "$PWD"
CMD ["python3", "-m", "flask", "--app", "mainServer",  "run"]
