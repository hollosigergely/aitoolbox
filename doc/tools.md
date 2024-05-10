# AI Toolbox developer manual

Before starting to develop AI Tool, please get known with the AI Toolbox concept, by reading the [paper](doc/NOMS2024.pdf). To get into developing AI Tools, we present the [demo tool](https://github.com/hollosigergely/demo-tool) as an example in the following.

## Integration level
While the rules for implementing an AI Tool is lazy, an AI Tool shall follow some guidelines stated by the AI Toolbox as follows:

 * Clear definition of the algorithm, the implementation and the dependencies
 * Precise documentation of the algorithm
 * Summary of the best practices (e.g. training data requirements, hyperparameter selection, etc.)
 * Easy experimentation and deployment (for proof-of-concept)
 * Example inputs 

Also, the tool shall be granular, modular and reusable respecting its interfaces and methods. Based on the guidelines, one can distinct two different levels of integration, depending on the deployment support of the AI Tool:

 * **deep integration**: deeply integrated tools accepts the usual means provided by the AI Toolbox to deploy the tool service
 * **shallow integration**: the tool can be deployed in a user specified way, however, documentation structure and guidelines are respected

Shallow integration makes it possible to include AI Tools which are hard to fit into the implementation of the AI Toolbox, however, they also contribute to the tool catalogue.

## Directory structure
Clone the demo tool with
```
cd ~/aitools
git clone https://github.com/hollosigergely/demo-tool.git
```

Check the directory structure of the demo tool, which is the prefered way of organize the directory structure of a AI Tool.
```
├── assets
│   └── aitoolbox-impl.png
├── config.ai
├── .deploy
│   ├── docker-compose.yml
│   └── service
│       ├── Dockerfile
│       └── requirements.txt
├── doc
│   └── BP.md
├── query.ipynb
├── README.md
└── test
    └── example.http
```
Each tool has a `config.ai` metadata file, describing the most important information about the tool itself in YAML format, consisting of the name and description of the tool and deploy information.

Tools shall have a `README.md` file which introduces the tool itself, describing the goal of the tool and the basic usage information.

Tools typicall provides a couple of `ipynb` Python nootebook files, however, tools do not need to be implemented in Python, they can use any (e.g. compiled) languages without Jupyter support. Here, `query.ipynb` implements the algorithm itself (which is a simple one), but complicated algorithms can consists of multiple notebook files, and also learning algorithms can have training notebooks.

The `.deploy` directory contains everything which is required for deploying the tool as a service. `assets` contains any file which is required (e.g. small data, binary files, etc.). Huge files shall be referenced instead of version checked.

The `doc` directory holds the detailed documentation of the tool. One of the is the `BP.md` which describes the experiences gathered while developing the tool itself. 

The `test` directory holds basic tests or example inputs for the service.


## config.ai
The file holds the main information about the tool. The demo tool has for example:
```
tool:
    name: "AI Toolbox Demo Service"
    descr: "This is an example demo service for the AIMS AI Toolbox"
    version: 1.0.0
deploy:
    mode: "rest_builtin"
    deploy_dir: ".deploy"
    nb_path: "query.ipynb"
```
These are the mandatory parts. At this moment, only `rest_builtin` deployment is supported. The deployment stub directory (`deploy_dir`) and the default service notebook (`nb_path`) is defined.


## Deployment


## Notebook
See the [notebook development guidelines](notebook.md).