# SDSC NYC 2023 Workshop Book

## Installing

- Install Cargo [Cargo Book: Installation](https://doc.rust-lang.org/cargo/getting-started/installation.html)

- Install [`mdbook`](https://github.com/rust-lang/mdBook)

```bash
cargo install mdbook
```

## Plugins

[List of plugins for MDBook](https://github.com/fredrhen/mdbook-plugin-list)

### Admonish Preprocessor

- Install [`mdbook-admonish`](https://github.com/tommilligan/mdbook-admonish/tree/main) for admonishments

```bash
cargo install mdbook-admonish
```

Then let mdbook-admonish add the required files and configuration:

```bash
# Note: this may need to be rerun for new minor versions of mdbook-admonish
# see the 'Semantic Versioning' section below for details.
# specify a directory where CSS files live, relative to the book root

mdbook-admonish install --css-dir ./theme/css .
```

This will add the following configuration to your book.toml:

```bash
[output.html]
additional-css = ["./theme/css/mdbook-admonish.css"]

[preprocessor.admonish]
command = "mdbook-admonish"
```

### Presentation Preprocessor

To toggle between slides and web, you can press `alt+p`

- Install [`mdbooks-presentation-preprocessor`](https://github.com/FreeMasen/mdbook-presentation-preprocessor) for turning the books into slides

```bash
cargo install mdbook-presentation-preprocessor
```

Add the preprocessor to `book.toml`

```bash
[preprocessor.presentation-preprocessor]
```

### Wordcount Preprocessor

- Install [`mdbook-wordcount`](https://github.com/nomorepanic/mdbook-wordcount)

```bash
cargo install mdbook-wordcount
```

Add the following to `book.toml`

```bash
[output.wordcount]
```

## Building

```bash
mdbook serve --open
```
