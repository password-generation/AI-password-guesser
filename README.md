## Table of contents

- [Table of contents](#table-of-contents)
- [The goals for June 2023](#the-goals-for-june-2023)
- [Installation and Requirements](#installation-and-requirements)
- [How to use the generator](#how-to-use-the-generator)
  - [Options](#options)
  - [Evidence](#evidence)
- [The password-generation rules](#the-password-generation-rules)
- [Information obtained from the evidence file(s)](#information-obtained-from-the-evidence-files)

## The goals for June 2023

- [ ]  Terminal-based application accepting the evidence as the input file(s) in one of the `.txt`, `.pdf`, `.docx`, `.odt` formats
- [ ]  The possibility to include and use a custom-made password-creation rules’ file
- [ ]  The generation of the user-specified number of passwords based on the evidence and password-creation rules

## Installation and Requirements

- [ ]  TODO

## How to use the generator

To run the program type the following command in the terminal

`$ python password_guessing.py [options] [evidence]`

### Options

- [ ]  TODO

### Evidence

A single file or a directory containing the evidence in `.txt` format.

## The password-generation rules

The text file describing the password-generation rules contains exactly one rule per line. 

The specification of the rule definitions’ syntax is a part of the tasks for the first sprint. 

The effect of applying rules for example tuple of tokens “`aleksandra`” and “`1995`”

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

Extracted tokens: `Marek`, `Euzebia`, `Filomena`, `Rex`, `Max`, `maj`, `1995`, `10`

The correspondence:

- Tomek: Hej Marek! Jak spędziłeś weekend?
- Marek: Cześć! Było wspaniale, dzięki, że pytasz. Spędziłem trochę czasu z Euzebią i Filomeną. Zabraliśmy Rexa, naszego uroczego psa, do parku i świetnie się bawił, goniąc swoją ulubioną piłeczkę tenisową. Jak o tobie?
- Tomek: To brzmi wspaniale! Mój weekend też był udany. A propos, Marek, czy mógłbyś mi przypomnieć datę swoich urodzin? Chcę mieć pewność, że kupię ci odpowiedni prezent.
- Marek: Jasne, jest 10 maja 1995. Z góry dziękuję! Swoją drogą, jak się ma twój pies? Pamiętam, jak wspomniałeś, że adoptowałeś nowego szczeniaka.
- Tomek: Ach, dzięki za przypomnienie. Ma na imię Max i szybko rośnie.
- Marek: Oczywiście! Przy okazji, czy Euzebia mówiła ci o zbliżającym się spotkaniu rodzinnym w przyszłym tygodniu? Planujemy małe spotkanie z okazji urodzin Filomeny.
- Tomek: Nie, jeszcze o tym nie wspomniała. Na pewno zaznaczę to w kalendarzu. Daj mi znać, jeśli potrzebujesz pomocy w przygotowaniach.
- Marek: Dzięki, Marek! Twoje wsparcie jest zawsze mile widziane. Z radością świętujemy piąte urodziny Filomeny.