# jupyter-activity-monitor-extension:

This package includes the JupyterLab extension built by Maxdome/Sagemaker team for checking last activity time comparing sessions and terminals. 

## Requirements
* Jupyter-server > 2.0.0
* tornado

## Installing the extension
To install the extension within local Jupyter environment, a Docker image/container or in SageMaker Studio, run:
```
pip install jupyter_activity_monitor_extension-<version>-py3-none-any.whl`
```

## Uninstalling the extension
To uninstall this extension, run:
```
pip uninstall jupyter-activity-monitor-extension`
```

## Troubleshooting
If you are unable to connect to the /api/idle endpoint, check that the server extension is enabled:

```
jupyter serverextension list
```

## Docker Sidecar Support
This activity monitor also supports checking the activity of Docker sidecar containers that are running alongside JupyterLab. For example, a proprietary execution engine that is being used by Jupyter Notebooks may be loaded as a sidecar. This activity monitor is able to incorporate activity in the sidecar into the reported last activity time by hooking into any existing activity API specified on the sidecar and served through a port.

Docker sidecars may be set up by running Docker containers using the terminal within JupyterLab.

In order to make a sidecar compatible with this extension, three labels must be configured in the running container:
1. `com.amazon.jupyter.activity.port`: This label should specify the value of the exposed or forwarded port running the sidecar's activity API
2. `com.amazon.jupyter.activity.endpoint`: This label should specify the name of the sidecar's activity API
3. `com.amazon.jupyter.activity.response`: This label should specify the key in the activity API's response that returns a numeric value, where 0 corresponds to an "idle" container, and a non-zero value mean a container is actively running tasks. This label can also be a JMESPath.
4. `com.amazon.jupyter.activity.payload`: This label should specify a payload, if the endpoint corresponds to a POST request. If this label is not specified, the activity monitor will default to a GET request.

### Example

A user is running a sidecar container to execute long-running jobs from within JupyterLab. This sidecar is running on port 8080 and has an activity API at `api/v1/jobs` which returns a response in the following format:

```json
{
    "active_jobs": number
}
```

The user may configure this sidecar's docker labels as follows:
```json
{
    "com.amazon.jupyter.activity.port": 8080,
    "com.amazon.jupyter.activity.endpoint": "api/v1/jobs",
    "com.amazon.jupyter.activity.response": "active_jobs"
}
```

If there are 0 active jobs, the extension will return the JupyterLab's last active timestamp. If there are 1 or more active jobs running, then the extension will return the current time of the request (to `/api/idle`).

If the user wishes to not set up the labels, the extension will simply ignore the status of the sidecar container.

## Steps to Publish a version to conda forge.

To publish a new version of the package to conda-forge follow the bellow steps:
1. Make changes in https://code.amazon.com/packages/MaxDomeJupyterIdleExtension and upgrade the version in setup.py
2. Make sure the changes is deployed to RepoPublishing stage in https://pipelines.amazon.com/pipelines/MaxDomeJupyterIdleExtension
3. Update the version in https://code.amazon.com/packages/MaxDomeJupyterIdleExtensionPublishingCDK in extensions-package-selection.json. Ex : https://code.amazon.com/reviews/CR-142866575/revisions/1
4. once the changes are deployed in the prod stage in https://pipelines.amazon.com/pipelines/MaxDomeJupyterIdleExtensionPublishing the package version has been published to pypi
5. You can see the pypi version here https://pypi.org/project/jupyter-activity-monitor-extension/
6. once the package is published in pypi, we have to publish the same in conda forge, for the same open a PR to https://github.com/conda-forge/jupyter-idle-feedstock/blob/main/recipe/meta.yaml by updating the sha of the new version. To update feedstock you can use this guide https://conda-forge.org/docs/maintainer/updating_pkgs/#example-workflow-for-updating-a-package
7. once the package version is published in a couple of hrs we can make installation of the package from the conda-forge channel. https://anaconda.org/conda-forge/jupyter-activity-monitor-extension
