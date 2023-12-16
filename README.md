## Table of contents

- [Table of contents](#table-of-contents)
- [Requirements](#requirements)
- [Installation](#installation)
- [How to use the generator](#how-to-use-the-generator)
  - [Options](#options)
  - [Evidence](#evidence)
- [The password-generation rules](#the-password-generation-rules)
- [Information obtained from the evidence file(s)](#information-obtained-from-the-evidence-files)

## Requirements
- Python 3.10 or newer

## Installation
```
git clone https://github.com/password-generation/AI-cryptanalysis.git
cd AI-cryptanalysis

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## How to use the generator

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

### Evidence

Files or a directory containing the evidence in `.txt`, `.pdf`, `.odt`, `.docx` format.

## The password-generation rules

A text file describing the password-generation rules contains exactly one rule per line.

The specification of the rule definitions’ syntax is a part of the tasks for the first sprint.

The effect of applying rules for example tuple of tokens `aleksandra` and `1995`

```bash
AL3KS@NDRA
AlEkSaNdR@
aLeKsAnDrA
Aleks@ndra1995
a1l9e9k5sa
Ksandra95
ale95
```

## Example of program execution

### Evidence data - text messages:

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
$ ./guess_passwords.py -l EN -n 16 -o passwords.txt -mg test1.txt
Passwords max length: 16
Output file: ./output/passwords.txt
Evidence files: ['test1.txt']
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
