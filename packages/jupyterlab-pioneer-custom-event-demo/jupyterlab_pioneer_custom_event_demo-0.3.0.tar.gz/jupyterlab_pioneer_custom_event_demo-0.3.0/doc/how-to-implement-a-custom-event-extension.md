# How to implement a custom event extension

Set up development environment

```
conda create -n telemetry-demo --override-channels --strict-channel-priority -c conda-forge -c nodefaults jupyterlab=4 nodejs=18 copier=8 jinja2-time jupyter-packaging git

conda activate telemetry-demo
```

### Implement the extension from scratch

Initialize from the extension template

```
mkdir jupyterlab-pioneer-custom-event-demo

cd jupyterlab-pioneer-custom-event-demo

copier copy --UNSAFE https://github.com/jupyterlab/extension-template .
```

Add `jupyterlab-pioneer` as a dependency in `pyproject.toml` and `package.json`.

```toml
<!-- pyproject.toml -->
dependencies = [
    "jupyter_server>=2.0.1,<3",
    "jupyterlab-pioneer"
]
```

```json
// package.json
    "jupyterlab": {
        ...
        "sharedPackages": {
            "jupyterlab-pioneer": {
                "bundled": false,
                "singleton": true,
                "strictVersion": true
            }
        }
    },
```

Note: You will need NodeJS to build the extension package.

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Install package in development mode
pip install -e "."
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Server extension must be manually installed in develop mode
jupyter server extension enable jupyterlab-pioneer-custom-event-demo
# Rebuild extension Typescript source after making changes
jlpm build
```

You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm watch
# Run JupyterLab in another terminal
jupyter lab
```

### Implement the extension based on the demo extension

```bash
# Clone the repo to your local environment
git clone https://github.com/educational-technology-collective/jupyterlab-pioneer-custom-event-demo
# Change directory to the jupyterlab-pioneer-custom-event-demo directory
cd jupyterlab-pioneer-custom-event-demo
# Install package in development mode
pip install -e "."
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Server extension must be manually installed in develop mode
jupyter server extension enable jupyterlab-pioneer-custom-event-demo
# Rebuild extension Typescript source after making changes
jlpm build
# Or watch the source directory in one terminal, automatically rebuilding when needed
jlpm watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```

### Development Workflow

#### Client Side

- Make changes to the TypeScript client extension.
- Refresh the browser.
- Observe the changes in the running application.

#### Server Side

- Make changes to the Python server extension.
- Stop the Jupyter server.
- Start the Jupyter server.
- Observe the changes in the running application.

### Useful links

https://jupyterlab.readthedocs.io/en/stable/extension/extension_tutorial.html

https://jupyter-server.readthedocs.io/en/latest/operators/configuring-extensions.html

https://github.com/educational-technology-collective/jupyterlab-pioneer

### Development uninstall

```bash
# Server extension must be manually disabled in develop mode
jupyter server extension disable jupyterlab-pioneer-custom-event-demo
pip uninstall jupyterlab-pioneer-custom-event-demo
```

In development mode, you will also need to remove the symlink created by `jupyter labextension develop`
command. To find its location, you can run `jupyter labextension list` to figure out where the `labextensions`
folder is located. Then you can remove the symlink named `jupyterlab-pioneer-custom-event-demo` within that folder.

### Packaging the extension

See [RELEASE](RELEASE.md)

## How to utilize the `jupyter-pioneer` extension to export telemetry data

The `jupyter-pioneer` extension helps to monitor notebook states and export telemetry data. It also provides a basic JupyterLab events library.

The extension's router provides 2 methods, `loadNotebookPanel` and `publishEvent`.

`loadNotebookPanel` should be called first when activating the producer extension, to associate the telemetry events with the correct notebook panel before exporting data.

`publishEvent` could be called whenever we want to publish the event and export telemetry data to the desired endpoints. The `publishEvent` method takes two arguments, `eventDetail: Object` and `logNotebookContent: Boolean`.

There is generally no limitation on the structure of the `eventDetail` object, as long as the information is wrapped in a serializable javascript object. `logNotebookContent` is optional and should be a `Boolean` object. Only if it is provided and is `true`, the router will send out the entire notebook content along with the event data.

When `publishEvent` is called, the router checks if the notebook panel is loaded properly, and then insert the notebook session ID, notebook file path, and the notebook content (when `logNotebookContent` is `true`) into the data. Then, the router checks the type of each exporter, processes and sends out the data one by one. If `env` and `params` are provided in the configuration file when defining the desired exporter, the router would extract the environment variables and add the params to the exported data. Finally, the router will assemble the responses from the exporters in an array and print the response array in the console.

## (Optional) Event Producer

There is no specific restrictions on when and where the telemetry router should be invoked. However, when writing complex event producer libraries, we recommend developers write an event producer class for each event, implement a `listen()` class method, and call the producer's `listen()` method when the producer extension is being activated. Within the `listen()` method, you may write the logic of how the extension listens to Jupyter signals or DOM events and how to use the `pioneer.router.publishEvent()` function to export telemetry data.

## (Optional) Producer Configuration

In this demo extension, there is only one event and actually does not need to go through the configuration.

However, writing code on top of the configuration file might be very useful when the event library is complex, and when the telemetry system is going to be deployed under different contexts with different needs of telemetry events.

For more details, see https://jupyter-server.readthedocs.io/en/latest/operators/configuring-extensions.html.
