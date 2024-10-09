from datetime import datetime, timedelta
import dateutil.parser
import sys
from toolkit.logger import logger


def unique_timestamp() -> str:
    """
    Returns a unique timestamp string.

    :returns: Current timestamp formatted as 'YYYYMMDD_HHMMSS'.
    """
    return datetime.now().strftime('%Y%m%d_%H%M%S')


def remove_timezone(date_string: str) -> str:
    """
    Removes timezone from a date string.

    :param date_string: The date string from which to remove the timezone.
    :returns: The date string without the timezone.
    """
    timezones = [
        'EET', 'CET', 'UTC', 'EDT', 'ULAT', 'LHDT', 'SAST', 'MT', 'EASST',
        'BRST', 'ADT', 'SST', 'KRAT', 'KST', 'W', 'Z', 'QYZT', 'KGT',
        'AEST', 'T', 'PMDT', 'AKDT', 'BNT', 'MAGT', 'L', 'LINT', 'GET',
        'ANAST', 'NCT', 'TFT', 'NFT', 'ACDT', 'SGT', 'MUT', 'CEST',
        'ORAT', 'CLT', 'VET', 'KUYT', 'ACWST', 'AZT', 'CCT', 'CST',
        'AMT', 'CHOST', 'EEST', 'IRDT', 'CHUT', 'MSD', 'TOT', 'TVT',
        'ChST', 'MST', 'CHADT', 'PDT', 'HST', 'VLAST', 'FKST', 'GALT',
        'MHT', 'AZOT', 'WITA', 'JST', 'NZDT', 'ART', 'OMSST', 'FNT',
        'TOST', 'AFT', 'GST', 'PET', 'HKT', 'SRT', 'PKT', 'RET',
        'CIST', 'WGST', 'ANAT', 'SYOT', 'SAMT', 'TKT', 'GILT', 'GYT',
        'PMST', 'IRST', 'NOVT', 'IRKT', 'CLST', 'G', 'Q', 'E', 'BST',
        'AWDT', 'AEDT', 'WAT', 'WST', 'H', 'SCT', 'ET', 'BOT', 'KOST',
        'IOT', 'AKST', 'CDT', 'CHOT', 'TRT', 'WAST', 'WFT', 'HDT',
        'WEST', 'CXT', 'TJT', 'NOVST', 'EAT', 'UYST', 'CHAST', 'S',
        'MSK', 'ICT', 'CKT', 'ROTT', 'AoE', 'IST', 'COT', 'FKT',
        'M', 'WARST', 'CVT', 'FJT', 'U', 'PETT', 'TMT', 'BTT', 'N',
        'PYST', 'DAVT', 'HOVT', 'PST', 'I', 'FET', 'MART', 'CAST',
        'TLT', 'IDT', 'VOST', 'YEKST', 'NFDT', 'UYT', 'WT', 'AMST',
        'P', 'AST', 'MVT', 'CT', 'NST', 'TAHT', 'PETST', 'ACT',
        'EAST', 'BRT', 'YAKT', 'D', 'SAKT', 'SRET', 'VUT', 'DDUT',
        'NDT', 'OMST', 'PHT', 'VLAT', 'GMT', 'LHST', 'GAMT', 'PGT',
        'EGST', 'WAKT', 'KRAST', 'WIB', 'AZST', 'UZT', 'B', 'MAWT',
        'X', 'ECT', 'Y', 'O', 'CIDST', 'CAT', 'NPT', 'MDT', 'PT',
        'WGT', 'AQTT', 'EGT', 'PWT', 'AT', 'WET', 'YAKST', 'MYT',
        'GFT', 'NZST', 'AWST', 'C', 'ALMT', 'R', 'SBT', 'WIT',
        'NUT', 'YAPT', 'MMT', 'PONT', 'K', 'F', 'YEKT', 'IRKST',
        'MAGST', 'PYT', 'V', 'AET', 'AZOST', 'HOVST', 'PHOT',
        'FJST', 'ACST', 'NRT', 'EST', 'ULAST'
    ]
    timezones = [" {}".format(t.lower()) for t in timezones if t and len(t) > 2]
    date_string = date_string.lower()
    matching_timezone = [t for t in timezones if t in date_string]
    if matching_timezone:
        logger.info("Found time zone: {}".format(matching_timezone))
        ind = date_string.rfind(matching_timezone[0])
        date_string = date_string[:ind].strip()
    return date_string


def parse_date_string(date_string: str) -> datetime:
    """
    Parses a date string and returns a datetime object.

    :param date_string: The date string to parse.
    :returns: Parsed datetime object.
    """
    date_string = date_string.strip("–").strip().lower()
    date_string = remove_timezone(date_string)
    date_string = date_string.replace("today at ", "").replace("today", "").strip()

    if "tomorrow" in date_string:
        date_string = handle_tomorrow(date_string)
        return dateutil.parser.parse(date_string) + timedelta(days=1)

    if "yesterday" in date_string:
        date_string = handle_yesterday(date_string)
        return dateutil.parser.parse(date_string) - timedelta(days=1)

    return dateutil.parser.parse(date_string)


def handle_tomorrow(date_string: str) -> str:
    """
    Handles the 'tomorrow' case in a date string.

    :param date_string: The date string containing 'tomorrow'.
    :returns: Modified date string.
    """
    for string in ["tomorrow at ", "by tomorrow", "tomorrow"]:
        date_string = date_string.replace(string, "").strip()
    return date_string


def handle_yesterday(date_string: str) -> str:
    """
    Handles the 'yesterday' case in a date string.

    :param date_string: The date string containing 'yesterday'.
    :returns: Modified date string.
    """
    for string in ["yesterday at ", "yesterday"]:
        date_string = date_string.replace(string, "").strip()
    return date_string


def format_date(date_string: str, stronly: bool = False) -> str or datetime:
    """
    Formats a date string into a datetime object.

    :param date_string: The date string to format.
    :param stronly: If True, return the date as a string formatted as 'YYYY-MM-DD'.
    :returns: Formatted date as datetime or string.
    """
    _date = None
    try:
        if isinstance(date_string, int) or isinstance(date_string, str) and date_string.isdigit():
            _date = datetime.fromtimestamp(int(date_string) / 1000)
            return _date

        _date = parse_date_string(date_string)

    except Exception as e:
        logger.error(
            f"Error occurred [{str(e)}] at line [{sys.exc_info()[2].tb_lineno}] with date_string: [{date_string}]")

    return _date.strftime("%Y-%m-%d") if stronly and isinstance(_date, datetime) else _date
