# Efficient Outlier Detection in Numerical and Categorical Data

# To Cite (to appear)
    @article{HYSORTOD2025,
        title={Efficient Outlier Detection in Numerical and Categorical Data},
        author={Eugênio F. Cabral, Braulio V. S. Vinces, Guilherme D. F. Silva, Jörg Sander, Robson L. F. Cordeiro},
        journal={Data mining and knowledge discovery},
        year={2025},
        publisher={Springer}
    }    

# Abstract

> How to spot outliers in a large, unlabeled dataset with both numerical and categorical attributes? How to do it in a fast and scalable way? Outlier detection has many applications; it is covered therefore by an extensive literature. The distance-based detectors are the most popular ones. However, they still have two major drawbacks: (a) the intensive neighborhood search that takes hours or even days to complete in large data, and; (b) the inability to process categorical attributes. This paper tackles both problems by presenting HySortOD: a new, fast and scalable detector for numerical and categorical data. Our main focus is the analysis of datasets with many instances, and a low-to-moderate number of attributes. We studied dozens of real, benchmark datasets with up to **one million instances**; HySortOD outperformed **nine competitors** from the state of the art in runtime, being up to **six orders of magnitude faster** in large data, while maintaining high accuracy. Finally, we also performed an extensive experimental evaluation that confirms the ability of our method to obtain high-quality results from both real and synthetic datasets with categorical attributes.

# Main Sections
1. [Directory Tree]
2. [HySortOD Usage]
3. [HySortOD Competitors]
4. [Experiments]

## Directory Tree

A summary of the file structure can be found in the following directory tree.

```bash
HySortOD
├───code
│   ├───hysortod \\ Java implementation, HySortOD instantiation and overall code
├───competitors \\ All competitors
├───datasets
│   ├───categorical \\ Real datasets with categorical attributes
│   ├───numerical \\ Real datasets with numerical attributes
│   ├───scalability \\  Samples of real datasets
│   ├───synthetic \\  Synthetic datasets with categorical attributes
├───experiments
│   ├───q1_effectiveness_efficiency
│   ├───q2_scalability
│   ├───q3_parametrization
│   ├───q4_categorical_data
```

## HySortOD Usage

HySortOD and its competitors use a number of open source tools to work properly. The following packages should be installed before starting

#### Related to Java

- jre8+ - Java Runtime Environment version 8 or more.
- maven - Software project management and comprehension tool.

#### Related to Python

- python - Python interpreter in version 3.7 or above.

#### Related to R

- Rscript - R interpreter in version 4.3.1 or above.

### Building HySortOD

Run with no options:

```sh
sh code/build.sh
```

### Running HySortOD

For Java implementation, run:

```sh
java -jar code/hysortod/target/HySortOD-1.0.jar --input INPUT [--inputSeparator INPUTSEPARATOR] [--hasHeader {true,false}] [--labelColumn LABELCOLUMN] [--b B] [--minSplit MINSPLIT] [--reportOutput {true,false}]
```

## HySortOD Competitors

All competitors are publicly available, below are the source code download links:

- ABOD, kNN-Out, DB-Out, LOF, ODIN, HilOut, aLOCI - <https://repo1.maven.org/maven2/io/github/elki-project/elki/0.8.0/elki-0.8.0.jar>

- iForest - <https://cran.r-project.org/web/packages/isotree/vignettes/An_Introduction_to_Isolation_Forests.html>

- HDoutliers - <https://cran.r-project.org/web/packages/HDoutliers/HDoutliers.pdf>

## Experiments

Before running the experiments, we recommend using [Anaconda](https://docs.anaconda.com/anaconda/install/) to create the environment with all the necessary packages with the following command:

```sh
conda env create -f experiments/environment.yml
conda activate hysortod_env
```

To evaluate how effectiveness and efficiency is HySortOD (**Q1**),

```sh
python experiments/q1_effectiveness_efficiency/run.py
```

To evaluate how scalabilable is HySortOD (**Q2**),

```sh
python experiments/q2_scalability/run.py
```

To investigate the parametrization values of HySortOD (**Q3**),

```sh
python experiments/q3_parametrization/run.py
```

To evaluate the impact on HySortOD accuracy of relevant/irrelevant attributes in categorical data (**Q4**),

```sh
python experiments/q4_categorical_data/run.py
```

_This software was designed in Unix-like systems, it is not yet fully tested in other OS._