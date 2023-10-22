from commons import LabelType, Token
from dateutil.parser import parse
from calendar import month_abbr, month_name


def extract_parse_dates(tokens: list[Token]):
    other_tokens = list(filter(lambda x: x.label != LabelType.DATE, tokens))
    date_tokens = filter(lambda x: x.label == LabelType.DATE, tokens)
    for token in date_tokens:
        datetime = parse(token.text)
        day = datetime.date().day
        month = datetime.date().month
        year = datetime.date().year

        short_year = None
        if year < 2000 and year > 1900:
            short_year = year % 100

        day_month = day * 100 + month

        short_month = month_abbr[month]
        long_month = month_name[month]

        new_tokens = [
            Token(str(day), LabelType.DATE),
            Token(str(month), LabelType.DATE),
            Token(str(year), LabelType.DATE),
            Token(str(day_month), LabelType.DATE),
            Token(short_month, LabelType.DATE),
            Token(long_month, LabelType.DATE),
        ]

        if short_year:
            new_tokens.append(Token(str(short_year), LabelType.DATE))

        other_tokens.extend(new_tokens)

    return other_tokens
