- [Notebook development guidelines](#notebook-development-guidelines)
  - [Deployable notebooks](#deployable-notebooks)
  - [Argument decoding and encoding](#argument-decoding-and-encoding)
  - [Remote execution of notebooks](#remote-execution-of-notebooks)
  - [Best Practices](#best-practices)


# Notebook development guidelines

To ease development and evaluation of AI Tools, the AI Toolbox encourages the developers to use Jupyter notebooks to present their solution to AI problems. Notebooks has a couple of advantages:

 * step-by-step execution
 * built-in plotting and displaying diagrams and images
 * easy evaluation
 * flexible kernels (virtual environments, remote execution)
 * deployability

Please feel free to include various notebooks in your tool, however, we recommend to include two basic notebook for AI tools:

 * **query.ipynb**: the deployable AI service
 * **train.ipynb**: the notebook for training the AI model

To edit notebooks, it is preferred to use [Visual Code](https://code.visualstudio.com/) editor, since it supports notebook editing and also execution of cells in different kernels.

*Please note, that notebooks support only Python and R code execution.*

For example notebook, see the `query.ipynb` in the [demo tool](https://github.com/hollosigergely/demo-tool).

## Deployable notebooks
Properly formatted notebooks can be readily deployed into REST or other services using AI Toolbox utils. For an AI Tool, the deployable notebook is defined in the `config.ai` file by setting `deploy.nb_path`.

Deployable notebooks has some further requirements. Deployable notebooks consists of three different sections, separated by markdown cells with specific content. The two special markdown cells are:

 * *Setup placeholder*: Markdown cell with a pure `# Setup` header content
 * *Service placeholder*: Markdown cell with a pure `# Service` header content

The three different sections are:

 * *Preamble*: starts from the beginning of the notebook and lasts until the *Setup placeholder*
 * *Setup part*: starts at the *Setup placeholder* and lasts until the *Service placeholder*
 * *Service part*: starts at the *Service placeholder* and lasts until the end of the notebook

The deployed service is infered from the deployable notebook using the AI Toolbox Utils:
```
python -m aitoolbox gensrc <tool_dir> -o <out_dir>
```
Also, the deploy command of the AI Toolbox Util creates the source beyond copying the deploy stub files. The generation of the source code is as follows:

 1. The content from the *Setup part* is copied into a setup script `setup.py`
 2. The content from the *Service part* is copied into a service script `service.py`
   
All the cells are included, except:

 * Markdown cells
 * Raw cells
 * Code cells starting with `#!skip`

The setup script is executed before starting the REST server. At each request, the service script is called with the appropriate arguments. For handling different contexts (e.g. notebook context and service context), developers are encouraged to use the [AI Toolbox Support Library](https://github.com/hollosigergely/aitoolbox_support_library), which provide seamless integration of notebooks with REST services.

**TODO: Sequence diagram**

## Argument decoding and encoding

## Remote execution of notebooks
Notebooks can be executed on remote hardware, e.g. using a remote machine with advanced GPUs. In this case, it is preferred to use a remote Jupyter instance. To create remote Jupyter instance, setup the `notebook` on the remote machine using e.g. pip:
```
pip install notebook
```

For a sustainable solution, use dockerized solution. The `Dockerfile` bellow creates an Docker image e.g. based on the nVidia CUDA 11.8 image:

```
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04
WORKDIR /root

RUN apt update && \
        apt -y install python3-pip \
        && rm -rf /var/lib/apt/lists/*

ENV TZ=Europe/Budapest \
    DEBIAN_FRONTEND=noninteractive

RUN pip3 install notebook


CMD ["/usr/local/bin/jupyter",  "notebook", "--allow-root","--ip","0.0.0.0","--port","8888"]
EXPOSE 8888
```

To use the image, create the Dockerfile above, and in the same directory, run
```
docker build -t cuda_jupyter .
```

After building the image, run the container with GPU support as
```
docker run --rm --gpus all -p 8888:8888 cuda_jupyter
```

The remote Jupyter session can be accessed rmeotely on the host port 8888. Note: using GPUs in Docker images requires the [nVidia Container Toolkit](https://github.com/NVIDIA/nvidia-container-toolkit) to be installed among with the proper driver for the video card!

**TODO: Example images for Visual Code**


## Best Practices