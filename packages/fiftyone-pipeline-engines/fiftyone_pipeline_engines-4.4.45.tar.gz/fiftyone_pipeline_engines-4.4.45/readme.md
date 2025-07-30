# Pipeline Engines

![51Degrees](https://51degrees.com/DesktopModules/FiftyOne/Distributor/Logo.ashx?utm_source=github&utm_medium=repository&utm_content=readme_main&utm_campaign=python-open-source "Data rewards the curious") **Python Pipeline Engines**

[Developer Documentation](https://51degrees.com/pipeline-python/index.html?utm_source=github&utm_medium=repository&utm_content=readme_main&utm_campaign=python-open-source "Developer Documentation")

## Introduction

The Pipeline is a generic web request intelligence and data processing solution with the ability to add a range of 51Degrees and/or custom plug ins (Engines) 

## Requirements

* Python 3.8+

## This package fiftyone_pipeline_engines

This package extends the `flow element` class created by the `fiftyone-pipeline-core` package into a specialized type of flow element called an engine. This allows for additional features including:

* An auto-updating data file for properties
* A service called when a requested property
* A caching system and implementation of an LRU (least recently used) cache

Engines created by 51Degrees:

- [**fiftyone_devicedetection**](https://pypi.org/project/fiftyone-devicedetection/) - Get details about the devices accessing your web page
- [**fiftyone_location**](https://pypi.org/project/fiftyone-location/) - Get postal address details from the location of devices accessing your web page

## Requirements 

* Python 3.8+
* The gitversion lib using `python -m pip install gitversion`

