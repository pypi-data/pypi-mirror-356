# Pipeline Implementation Guide

Marimba is designed with a clear separation between the core Marimba system and the Pipelines that process data for single or multi-instrument systems. This modular approach allows you to create custom Pipelines tailored to your unique data processing needs, while leveraging the robust functionalities provided by the core Marimba framework.

In a Marimba project, the core system manages the overall workflow, including the execution of importing, processing, and packaging of datasets. The Pipeline, on the other hand, contains all the necessary logic and code to process data from specific instruments or systems. This separation ensures that the core Marimba remains flexible and adaptable, while Pipelines provide the specialised processing required for different types of data.

## Marimba Project Overview

A Marimba project will follow a specific directory structure designed to keep your data and processing logic organised and allow Marimba to perform it's operations. This is an overview of the structure of a Marimba project:

```plaintext
marimba-project
├── .marimba                    - Hidden configuration and state directory managed by Marimba
│
├── collections                 - Marimba collections directory containing individual Marimba Collections
│   ├── collection1             - Individual Marimba Collection
│   └── collection2             - Individual Marimba Collection
│
├── datasets                    - Marimba datasets directory containing fully processed FAIR Marimba datasets
│   ├── dataset1                - Individual Marimba Dataset
│   └── dataset2                - Individual Marimba Dataset
│
├── pipelines                   - Marimba pipelines directory containing individual Marimba Pipelines
│   ├── pipeline1               - Individual Marimba Pipeline
│   └── pipeline2               - Individual Marimba Pipeline
│
├── targets                     - Marimba targets directory containing configuration for distribution targets
│
└── project.log                 - Log file containing a detailed record of all operations performed within the Marimba project

```

## Introduction to Pipelines

Overview: Define what a Marimba Pipeline is and its role within the Marimba ecosystem.
Pipeline Capabilities: Describe the types of processing tasks Pipelines handle, such as image processing, metadata management, and integration with external systems.

### Description of the pipeline structure

Code example of an empty pipeline

## Setting Up a New Pipeline

Creating a Pipeline Directory: Instructions on setting up the directory structure for a new Pipeline within a Marimba project.
Pipeline Configuration: Guidance on setting up the pipeline.yaml configuration file and other necessary setup files.
Dependency Management: Explain how to manage dependencies using requirements.txt or other tools.

### Multi-level iFDO and summaries