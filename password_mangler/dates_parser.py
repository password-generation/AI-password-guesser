from commons import LabelType, Language, Token
from dateutil.parser import parse
from datetime import datetime
import translators as ts


def extract_parse_dates(tokens: list[Token], language: Language):
    date_mask = LabelType.to_binary_mask([LabelType.DATE])
    other_tokens = set(filter(lambda x: date_mask != x.binary_mask, tokens))
    date_tokens = list(filter(lambda x: date_mask == x.binary_mask, tokens))

    date_units = []
    for token in date_tokens:
        text = token.text
        mask = token.binary_mask

        try:
            date_units = process_date_units(text)

        except ValueError:
            if language == Language.POLISH:
                text = ts.translate_text(text, from_language="pl", to_language="en")

                try:
                    date_units = process_date_units(text)
                except ValueError:
                    continue  # not a valid datetime format to parse, we skip it

        finally:
            other_tokens.update([Token(t, mask) for t in date_units])

    return list(other_tokens)


def process_date_units(text):
    d, m, y = extract_day_month_year(text)
    date_units = []

    if d is not None:
        day = str(d) if len(str(d)) > 1 else "0" + str(d)
        date_units.append(day)

    if m is not None:
        month = str(m) if len(str(m)) > 1 else "0" + str(m)
        date_units.append(month)

    if y is not None:
        year = str(y)
        short_year = year[2:]
        date_units.extend([year, short_year])

    if d is not None and m is not None:
        day_month = day + month
        date_units.append(day_month)

    return date_units


def extract_day_month_year(text):
    dflt_1 = datetime(1, 1, 1)
    dflt_2 = datetime(2, 2, 2)

    dt1 = parse(text, default=dflt_1)
    dt2 = parse(text, default=dflt_2)

    day = dt1.day if dt1.day == dt2.day else None
    month = dt1.month if dt1.month == dt2.month else None
    year = dt1.year if dt1.year == dt2.year else None

    return day, month, year
