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
`$ python3 -m pip install -r requirements.txt`

## How to use the generator

To run the program type the following command in the terminal

`$ python3 password_guessing.py [options] [evidence]`

### Options

* `-o [output_file]` - Text file with generated passwords 
* `-n [max_password_length]` - Maximal length of generated passwords
* `-l [language]` - Language of passed evidence [EN|PL]
* `-m [mangling]` - If present, program will create passwords using mangling rules
* `-g [generation]` - If present, program will create passwordsd using generational AI model

### Evidence

Files or a directory containing the evidence in `.txt`, `.pdf`, `.odt`, `.docx` format.

## The password-generation rules

A text file describing the password-generation rules contains exactly one rule per line. 

The specification of the rule definitions’ syntax is a part of the tasks for the first sprint. 

The effect of applying rules for example tuple of tokens `aleksandra` and `1995`

```bash
ALEKSANDRA
AlEkSaNdRa
aLeKsAnDrA
Aleksandra1995
aleksandra95
Ksandra95
ale15
```

## Information obtained from the evidence file(s)

Extracted tokens: `Filomena`, `Marek`, `Euzebia`, `Rex`, `Max`, `maj`, `1995`, `10`

File with the correspondence:

* Hey `Marek`! How was your weekend?

* Hi there! It was great, thanks for asking. I spent some quality time with `Euzebia` and `Filomena`. We took `Rex`, our adorable dog, to the park, and he had a blast chasing his favorite tennis ball. How about you?

* That sounds lovely! My weekend was good too. By the way, `Marek`, could you remind me of your `birthdate`? I want to make sure I get you the right gift.

* Sure, it’s `May` `10`, `1995`. Thanks in advance! By the way, how’s your dog doing? I remember you mentioned you adopted a new puppy.

* Ah, thanks for reminding me. His name is `Max`, and he’s growing fast. I hope `Rex` and `Max` can have a playdate soon!

* Absolutely! `Rex` would love that. By the way, did `Euzebia` tell you about the upcoming family gathering next week? We’re planning a small get-together for `Filomena`’s birthday.

* No, she didn’t mention it yet. But that’s wonderful! I’ll make sure to mark it on my calendar. Please let me know if you need any help with the preparations.

* Thanks! Your support is always appreciated. We’re excited to celebrate `Filomena` turning five. Time flies!

* Indeed, it does. I’m looking forward to seeing everyone. Let’s make it a memorable day for `Filomena`!
