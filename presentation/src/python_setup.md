# Environment Setup

The analysis for this workshop exists in the `notebooks` directory of the [sdsc-2023-workshop](https://github.com/thegeneralsystem/sdsc-2023-workshop/tree/main) repository. This workshop can be followed in a few ways. In recommended order:

- `0_getting_started_with_dfi.ipynb`
- `1_identifying_bsc_customers`
- `2_mobility_analysis.ipynb`
- `3_spatiotemporal_analysis.ipynb`

## I. Docker

If you have Docker installed you can run the notebooks in a container. Then, in a browser go to [http://127.0.0.1:8888/lab](http://127.0.0.1:8888/lab).

```bash
git clone https://github.com/thegeneralsystem/sdsc-2023-workshop.git && cd sdsc-2023-workshop
docker compose up jupyter
```

## II. Local Python Environment

You can clone this repo and follow along in your own Python environment. Jupyter Lab should automatically open in a new browser tab. But if it doesn't, then, in a browser go to [http://127.0.0.1:8888/lab](http://127.0.0.1:8888/lab).

```bash
git clone https://github.com/thegeneralsystem/sdsc-2023-workshop.git && cd sdsc-2023-workshop
pip install -r requirements.txt
jupyter lab
```

## III. MyBinder

_MyBinder limits the number of instances of a repo. Please only use if Docker and local Python environment are not viable. It can also take a bit to start up._

Each analysis will have a badge with a link to the notebook in a MyBinder environment. The following badge will take you a [MyBinder](https://mybinder.org/) environment with the notebooks in this workshop.

[![Notebook 2 - Dynamic Spatiotemporal Analysis](https://img.shields.io/badge/notebooks-workshop-FF5008)](https://mybinder.org/v2/gh/thegeneralsystem/sdsc-2023-workshop/HEAD?labpath=notebooks)

## IV. No Environment

If there are complications with the options above, you can follow along by just watching the presentation. All relevant code samples and outputs will be included.

<center>
<img src="./assets/images/oh-no-anyway.png" alt="Oh No!  Anyway" style="border-radius:10px">
</center>
