# BPC Election Information Surveys

This repository contains the data, analysis, and visualizations for surveys conducted by the Bipartisan Policy Center on where Americans seek election information. Three surveys--similar but with slight variations--were carried out by Morning Consult in October 2022, December 2023, and October 2024.

## October 2024

2024 data includes results from two surveys conducted by Morning Consult. The first was fielded from October 11-12 among a sample of 1,743 registered voters. The second was fielded from October 16-17 among a sample of 1,891 registered voters. 

One question (“BPC3: In the United States, there is information voters need to register and vote. Where are you most likely to look for this information?”) was accidentally overwritten by another question (“BPC4: If you wanted to know more about how elections are run in the United States, where are you most likely to look for that information?”) in the first field. As such, we combined responses from the two surveys for all questions except BPC3. Accordingly, the total sample size for BPC3 is 1,891 and the sample size for all other questions is 3,634.

## December 2023

Our 2023 poll was conducted by Morning Consult between December 13- 15, 2023 among a sample of 2,203 adults.

## October 2022

Our 2022 poll was conducted by Morning Consult between October 14-15, 2022 among a sample of 2,002 registered voters nationally. Results from the full survey have a margin of error of plus or minus 3 percentage points.

* *CO voters oversample*: Additional poll conducted between October 14-20, 2022 among a sample of 805 Colorado voters. 

* *GA voters oversample*: Additional poll conducted between October 14-17, 2022 among a sample of 809 Georgia voters.

* *WI voters oversample*: Additional poll conducted between October 14-24 2022 among a sample of 501 Wisconsin voters.


## Folder structure

The repository is organized by year, with each year containing folders for raw and processed data, as well as codebooks and analysis files specific to that survey year.

The general structure of each year's folder is as follows.
``` yml
BPC-ELECTION-INFORMATION-SURVEYS/
├── year/
│   ├── raw/
│   │   ├── data.csv                 # Raw survey data
│   │   ├── levels_codebook.csv      # Codebook for categorical levels
│   │   └── question_codebook.csv    # Codebook for questions asked
│   └── processed/                   # Processed and cleaned data in .csv format

│   ├── mc_deck.pdf                  # PDF of the survey analysis deck provided by Morning Consult
│   ├── survey_instrument.docx       # Survey questions document in Word format
│   ├── survey_instrument.md         # Markdown version of survey questions
│   └── analyses.ipynb               # Jupyter Notebook with analysis for the each survey
```
2024 has additional subfolders for multiple survey fields, detailed below. 
```yml
├── 2024/
│   ├── raw/
│   │   ├── field1/                  # Data for first survey field with BPC3 overwritten by BPC4 (general population)
│   │   │   ├── data.csv
│   │   │   ├── levels_codebook.csv 
│   │   │   └── question_codebook.csv
│   │   ├── field2/                  # Data for second survey field with corrected BPC3
│   │   │   ├── genpop/              
│   │   │   │   └── data.csv         # General population sample data for field2
│   │   │   ├── rvoter/              
│   │   │   │   └── data.csv         # Registered voters sample data for field2 (filtered and reweighted)
│   │   ├── stacked/                 
│   │   │   └── data.csv             # Combined data from field1 and field2 (registered voters only)

```
## Survey methodology

The interviews were conducted online with data weighted to approximate a target sample of registered voters based on age and gender, educational attainment, race, marital status, homeownership, race by education, 2020 presidential vote, and region. The results have a margin of error of ±2 percentage points.

## Analysis and publications

* December 2023 survey: [Who Voters Trust for Election Information in 2024](https://bipartisanpolicy.org/explainer/who-voters-trust-election-information-2024/)
* October 2022 survey: [New Survey Data on Who Americans Look to For Election Information](https://bipartisanpolicy.org/blog/new-survey-data-election-information/)


