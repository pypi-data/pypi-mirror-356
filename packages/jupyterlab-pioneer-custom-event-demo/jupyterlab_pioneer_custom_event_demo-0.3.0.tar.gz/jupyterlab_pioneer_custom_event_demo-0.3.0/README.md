# JupyterLab Pioneer Custom Event Demo

[![PyPI](https://img.shields.io/pypi/v/jupyterlab-pioneer-custom-event-demo.svg)](https://pypi.org/project/jupyterlab-pioneer-custom-event-demo)
[![npm](https://img.shields.io/npm/v/jupyterlab-pioneer-custom-event-demo.svg)](https://www.npmjs.com/package/jupyterlab-pioneer-custom-event-demo)

A JupyterLab extension that generates telemetry data when a user clicks a specific button.

This extension is an example of how to write a simple extension that leverages functionalities provided by [`jupyterlab-pioneer`](https://github.com/educational-technology-collective/jupyterlab-pioneer) to generate telemetry data for custom events.

## Get started

### Requirements

- JupyterLab >= 4.0.0

### Install

To install the extension, execute:

```bash
pip install jupyterlab-pioneer-custom-event-demo
```

### Configuration

To add a data exporter, users need to configure the `jupyterlab-pioneer` extension.

See more details [here](https://github.com/educational-technology-collective/jupyterlab-pioneer#configurations).

## Troubleshoot

If you are seeing the frontend extension, but it is not working, check
that the server extension is enabled:

```bash
jupyter server extension list
```

If the server extension is installed and enabled, but you are not seeing
the frontend extension, check the frontend extension is installed:

```bash
jupyter labextension list
```

## How to implement a custom event extension

https://github.com/educational-technology-collective/jupyterlab-pioneer-custom-event-demo/blob/main/doc/how-to-implement-a-custom-event-extension.md
