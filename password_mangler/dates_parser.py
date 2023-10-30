from password_mangler.commons import LabelType, Token
from dateutil.parser import parse


def extract_parse_dates(tokens: list[Token]):
    other_tokens = set(filter(lambda x: LabelType.DATE not in x.labels, tokens))
    date_tokens = list(filter(lambda x: LabelType.DATE in x.labels, tokens))

    for token in date_tokens:
        try:
            datetime = parse(token.text)
            labels = token.labels

            day = datetime.date().day
            month = datetime.date().month
            year = datetime.date().year

            short_year = None
            if year < 2000 and year > 1900:
                short_year = year % 100

            day_month = day * 100 + month

            new_tokens = [
                Token(str(day), labels),
                Token(str(month), labels),
                Token(str(year), labels),
                Token(str(day_month), labels),
            ]

            if short_year:
                new_tokens.append(Token(str(short_year), labels))

            other_tokens.update(new_tokens)

        except:  # not a valid datetime format to parse, we skip it
            continue

    return list(other_tokens)
