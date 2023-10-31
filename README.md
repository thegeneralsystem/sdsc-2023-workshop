# SDSC NYC 2023 Workshop

![Python versions](https://img.shields.io/badge/python-_3.10_|_3.11_|_3.12-blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat)](https://timothycrosley.github.io/isort/)

> **Deeper, Broader, Faster, Stronger: Expanding into new dimensions with spatiotemporal data**
>
> Spatial data that changes over time presents difficulties because of the cost, time, and complexity to process and analyze at scale. But this data holds valuable, latent and undiscovered insights that can make your analysis deeper (historically), broader (spatially), faster (analytically), and stronger! Join us for a fun and interactive session with Josh and Robert, senior data scientists who specialise in working with global-scale, spatiotemporal datasets. In this session, you'll use CARTO, Python and other familiar technologies to explore and overcome some of the most complex and challenging examples of geospatial analysis, get a glimpse into the future of geospatial data science and pocket some actionable takeaways.

- Presentation website - [https://sdsc-2023-workshop-nyc.ds.generalsystem.com/](https://sdsc-2023-workshop-nyc.ds.generalsystem.com/)

## Notebooks

The analysis for the workshop is located in the `notebooks` directory.

### Docker

```bash
docker compose up jupyter
```

### Python Environment

```bash
pip install -r requirements.txt
jupyter lab
```

## Workshop Presentation

The presentation is publicly available at [https://sdsc-2023-workshop-nyc.ds.generalsystem.com/](https://sdsc-2023-workshop-nyc.ds.generalsystem.com/) but can be viewed locally by running the Docker container.

```bash
docker compose up presentation
```
