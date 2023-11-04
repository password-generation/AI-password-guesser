from password_mangler.commons import LabelType, Language, Token
from dateutil.parser import parse
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
            datetime = parse(text)

        except ValueError:
            if language == Language.POLISH:
                text = ts.translate_text(text, from_language="pl", to_language="en")

                try:
                    datetime = parse(text)
                except ValueError:
                    continue  # not a valid datetime format to parse, we skip it
                else:
                    date_units = extract_date_units(datetime)

        else:
            date_units = extract_date_units(datetime)

        finally:
            other_tokens.update([Token(t, mask) for t in date_units])

    return list(other_tokens)


def extract_date_units(datetime):
    d, m, y = datetime.date().day, datetime.date().month, datetime.date().year

    day = str(d) if len(str(d)) > 1 else "0" + str(d)
    month = str(m) if len(str(m)) > 1 else "0" + str(m)
    year = str(y)
    short_year = year[2:]
    day_month = day + month

    date_units = [day, month, year, short_year, day_month]
    return date_units
