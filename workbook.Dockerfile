FROM python:3.11.5-slim
SHELL ["/bin/bash", "-c"]
COPY . /sdsc-workshop-book
WORKDIR /sdsc-workshop-book

RUN apt update && apt install -y libgdal-dev python3-pip fontconfig fonts-indic

RUN pip3 install -r requirements.txt

# Install fonts
RUN mv presentation/theme/fonts/* /usr/share/fonts/
RUN fc-cache -fv

RUN groupadd -r developers && useradd -r -g developers dev
RUN mkdir /home/dev && chown -R dev /home/dev
USER dev

CMD ["jupyter", "lab", "--port=8888", "--ip=0.0.0.0", "--NotebookApp.token=''", "--NotebookApp.password=''"]