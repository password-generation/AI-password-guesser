# Evidence Based AI Password Guesser

- [Requirements](#requirements)
- [Installation](#installation)
- [How to use the password guesser](#how-to-use-the-password-guesser)
  - [Options](#options)
  - [Input files format](#input-files-format)
- [User config file](#user-config-file)
- [Password generation rules](#password-generation-rules)
- [Example of program execution](#example-of-program-execution)
  - [Input file](#input-file)
  - [Extracted tokens](#extracted-tokens)
  - [Mangled passwords](#mangled-passwords)
  - [Generated passwords](#generated-passwords)
  - [Snippet from program execution](#snippet-from-program-execution)
- [Disclaimer about password model file](#disclaimer-about-password-model-file)

## Requirements
- Python 3.10 or newer

## Installation
```
git clone https://github.com/password-generation/AI-password-guesser.git
cd AI-password-guesser

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## How to use the password guesser

To run the program execute the following command in the terminal

```
./guess_passwords.py [options] [evidence]
```

### Options

```
usage: guess_passwords.py [-h] [-m] [-g] [-v]
                          [-n LENGTH] [-o OUTPUT]
                          [-l {EN,PL}] [-c CONFIG]
                          FILENAME [FILENAME ...]

This program generates a dictionary of passwords based on the provided evidence.
Currently supported evidence formats are: .txt, .pdf, .docx, .odt

positional arguments:
  FILENAME              Name of the file containing the evidence (can be a folder name)

options:
  -h, --help            show this help message and exit
  -n LENGTH, --length LENGTH
                        Max length of passwords
  -o OUTPUT, --output OUTPUT
                        Output file with result passwords
  -l {EN,PL}, --language {EN,PL}
                        Language of the evidence (default: EN)
  -c CONFIG, --config CONFIG
                        User config file
  -m, --mangle          Use password mangling
  -g, --generate        Use password generation model
  -v, --verbose         Flag for printing verbose output
```

### Input files format

Files or a directory containing the evidence in `.txt`, `.pdf`, `.odt`, `.docx` format.

## User config file

`config.yaml` is a YAML file where user can define:

* password model parameters: `stddev` and `samples_count` - max number of passwords generated from one template
* type of spacy NER model: `polish_tokenizer`, `english_tokenizer`
* `mangling_schedule` which declares which mangling rules should be used when
* `pre_generation_schedule` - the same as mangling schedule but used before generation

Here's default abbreviated user config:

```YAML
std_dev: 0.05
samples_count: 10

polish_tokenizer: pl_core_news_lg
english_tokenizer: en_core_web_lg

mangling_schedule:
  - type: unary
    rules:
      - nothing
      - capitalize
      - toggle_case
      - cut_end: 1
      - gamerize: 5
    labels:
      - PERSON
      - DATE
      - ORG

  - type: binary
    rules:
      - join
      - interlace
    labels:
      - PERSON
      - ORG

  - type: unary
    rules:
      - nothing
    labels:
      - PERSON

pre_generation_schedule:
  - type: binary
    rules:
      - join
    labels:
      - PERSON
      - WILDCARD
```

## Password generation rules

There are two types of password rules:
* unary, which accept and return one token/password, e.g.: capitalize, cut_end, gamerize.
* binary: which accept two tokens and return one password, e.g.: join, interlace

Here are passwords created from tokens `aleksandra` and `1995` using different kind of password rules:
```
AL3KS@NDRA
AlEkSaNdR@
aLeKsAnDrA
Aleks@ndra1995
a1l9e9k5sa
Ksandra95
ale95
```

## Example of program execution

### Input file

Text messages in txt format:

* Hey `John`! How was your weekend?

* It was great. I spent some time with `Elizabeth` and `Chris`. We took `Rex`, our dog, to the park. Btw, when is your birthdate?

* It’s `May 10, 1995`.

### Extracted tokens

NER (Named Entity Recognition) model extraced these tokens:

```
1995      [DATE]
chris     [PERSON]
elizabeth [PERSON]
john      [PERSON]
may 10    [DATE]
rex       [PERSON]
```

### Mangled passwords

Using default mangling schedule from `config.yaml`, password mangler generated 23064 passwords.
Here are 5 examples of these passwords:
```
c#r!sELIZA8ETH  [PERSON]
1005elIzab3th   [PERSON, DATE]
r3Xelizab3      [PERSON]
rex1995         [PERSON, DATE]
reXc#Ris        [PERSON]
```

### Generated passwords

Using default pre-generation mangling schedule from `config.yaml`, mangler generated 8849 templates.
Using them password model generated 3287 passwords.
Here are 5 examples of these passwords:
```
ilovelizabeth   [PERSON]
johncena        [PERSON]
matrex          [PERSON]
1005elarabeth   [PERSON, DATE]
chrioray        [PERSON]
```

### Snippet from program execution

```
$ ./guess_passwords.py -l EN -n 16 -o passwords.txt -mg msgs.txt
Passwords max length: 16
Output file: ./output/passwords.txt
Evidence files: ['msgs.txt']
Language: EN
Password mangling: On
Password generation: On

Reading evidence...
Tokenizing text...
Merging tokens: 100%|██████████████████████████| 6/6 [00:00<00:00, 31575.69it/s]
Extracted 6 tokens

Mangling tokens...
[1/4]  Unary mangling: 100%|██████████████| 144/144 [00:00<00:00, 370994.95it/s]
[2/4]  Unary mangling: 100%|██████████████| 350/350 [00:00<00:00, 217546.89it/s]
[3/4] Binary mangling:  99%|█████████▉| 24864/25088 [00:00<00:00, 157160.30it/s]
[4/4]  Unary mangling: 100%|██████████| 23064/23064 [00:00<00:00, 297485.20it/s]
Mangled 23064 tokens

Generating passwords...
Creating password templates...
[1/2] Binary mangling:  99%|███████████▊| 9310/9409 [00:00<00:00, 490460.21it/s]
[2/2]  Unary mangling: 100%|████████████| 8849/8849 [00:00<00:00, 535166.41it/s]
Created 8849 templates
Max number of passwords generated from one template: 10
Generating passwords: 100%|████████████████| 8849/8849 [00:35<00:00, 252.61it/s]
Generated 3298 tokens

Merging tokens: 100%|████████████████| 26362/26362 [00:00<00:00, 1233946.48it/s]
Merging tokens: 100%|████████████████| 26157/26157 [00:00<00:00, 1328711.86it/s]
Saved 26156 passwords to ./output/passwords.txt
```

## Disclaimer about password model file

In our application we've used pretrained autoencoder model file from https://github.com/pasquini-dario/PLR
