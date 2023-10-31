FROM rust:1.72.1-slim-buster
COPY . /sdsc-workshop-book 
WORKDIR /sdsc-workshop-book/presentation

RUN cargo install mdbook 
RUN cargo install mdbook-katex
RUN cargo install mdbook-admonish
RUN cargo install mdbook-presentation-preprocessor

RUN pwd && ls && mdbook-admonish install --css-dir ./theme/css .
RUN mdbook build -d ../public

RUN groupadd -r developers && useradd -r -g developers dev
RUN mkdir /home/dev && chown -R dev /home/dev
RUN mkdir -p ./book && chown -R dev ./book
USER dev

CMD ["mdbook", "serve", "--dest-dir", "book", "--open"]
# CMD ["mdbook", "serve", "--open"]