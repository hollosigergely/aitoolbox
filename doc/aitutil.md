# AI Toolbox utility script

The script can be used to deploy notebooks into proof-of-concept services. At this point, only REST server deployment is supported directly.

## Usage
The tool can be used by running
```
python3 -m aitoolbox
```

### Deploy
To deploy a tool as a service, use
```
python3 -m aitoolbox deploy <tool directory> -o <deploy dir>
```

Note, that the deploy dir is removed and replaced with the files required for deployment. The exact way of deployment is described in the documentation of the tools.