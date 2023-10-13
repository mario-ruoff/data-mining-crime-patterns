# Data Mining - Group 4

> An Examination of Crime Patterns in the City of Chicago for Use in Determining Optimal Police Presence

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Developing](#developing)

## Introduction
This is a brief introduction to the project.

## Installation
1. Clone or download this project
2. Install [conda](https://www.anaconda.com/download) and create an environment from the provided file:
```
conda env create -f environment.yml
```

## Usage
Instructions on how to use the project.

## Developing
### Updating Dependencies
If you add new dependencies to your conda environment, make sure to export it properly to the `environment.yml` file:
```
conda env export | grep -v "^prefix: " > environment.yml
```


