from password_mangler.commons import LabelType, Token
from dateutil.parser import parse


def extract_parse_dates(tokens: list[Token]):
    date_mask = LabelType.to_binary_mask([LabelType.DATE])
    other_tokens = set(filter(lambda x: date_mask != x.binary_mask, tokens))
    date_tokens = list(filter(lambda x: date_mask == x.binary_mask, tokens))

    # TODO
    # language version here

    for token in date_tokens:
        try:
            datetime = parse(token.text)
        except:  # not a valid datetime format to parse, we skip it
            continue
        else:
            labels = token.binary_mask
            d, m, y = datetime.date().day, datetime.date().month, datetime.date().year

            day = str(d) if len(str(d)) > 1 else "0" + str(d)
            month = str(m) if len(str(m)) > 1 else "0" + str(m)
            year = str(y)
            short_year = year[2:]
            day_month = day + month

            time_vars = [day, month, year, short_year, day_month]
            other_tokens.update([Token(t, labels) for t in time_vars])

    return list(other_tokens)
