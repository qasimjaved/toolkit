from toolkit.logger import logger


def remove_timezone_from_date(date_string):
    timezones = ['EET', 'CET', 'UTC', 'EDT', 'ULAT', 'LHDT', 'SAST', 'MT', 'EASST', 'BRST', 'ADT', 'SST', 'KRAT', 'KST',
                 'W', 'Z', 'QYZT', 'KGT', 'AEST', 'T', 'PMDT', 'AKDT', 'BNT', 'MAGT', 'L', 'LINT', 'GET', 'ANAST',
                 'NCT', 'TFT', 'NFT', 'ACDT', 'SGT', 'MUT', 'CEST', 'ORAT', 'CLT', 'VET', 'KUYT', 'ACWST', 'AZT', 'CCT',
                 'CST', 'AMT', 'CHOST', 'EEST', 'IRDT', 'CHUT', 'MSD', 'TOT', 'TVT', 'ChST', 'MST', 'CHADT', 'PDT',
                 'HST', 'VLAST', 'FKST', 'GALT', 'MHT', 'AZOT', 'WITA', 'JST', 'NZDT', 'ART', 'OMSST', 'FNT', 'TOST',
                 'AFT', 'GST', 'PET', 'HKT', 'SRT', 'PKT', 'RET', 'CIST', 'WGST', 'ANAT', 'SYOT', 'SAMT', 'TKT', 'GILT',
                 'GYT', 'PMST', 'IRST', 'NOVT', 'IRKT', 'CLST', 'G', 'Q', 'E', 'BST', 'AWDT', 'AEDT', 'WAT', 'WST', 'H',
                 'SCT', 'ET', 'BOT', 'KOST', 'IOT', 'AKST', 'CDT', 'CHOT', 'TRT', 'WAST', 'WFT', 'HDT', 'WEST', 'CXT',
                 'TJT', 'NOVST', 'EAT', 'UYST', 'CHAST', 'S', 'MSK', 'ICT', 'CKT', 'ROTT', 'AoE', 'IST', 'COT', 'FKT',
                 'M', 'WARST', 'CVT', 'FJT', 'U', 'PETT', 'TMT', 'BTT', 'N', 'PYST', 'DAVT', 'HOVT', 'PST', 'I', 'FET',
                 'MART', 'CAST', 'TLT', 'IDT', 'VOST', 'YEKST', 'NFDT', 'UYT', 'WT', 'AMST', 'P', 'AST', 'MVT', 'CT',
                 'NST', 'TAHT', 'PETST', 'ACT', 'EAST', 'BRT', 'YAKT', 'D', 'SAKT', 'SRET', 'VUT', 'DDUT', 'NDT',
                 'OMST', 'PHT', 'VLAT', 'GMT', 'LHST', 'GAMT', 'PGT', 'EGST', 'WAKT', 'KRAST', 'WIB', 'AZST', 'UZT',
                 'B', 'MAWT', 'X', 'ECT', 'Y', 'O', 'CIDST', 'CAT', 'NPT', 'MDT', 'PT', 'WGT', 'AQTT', 'EGT', 'PWT',
                 'AT', 'WET', 'YAKST', 'MYT', 'GFT', 'NZST', 'AWST', 'C', 'ALMT', 'R', 'SBT', 'WIT', 'NUT', 'YAPT',
                 'MMT', 'PONT', 'K', 'F', 'YEKT', 'IRKST', 'MAGST', 'PYT', 'V', 'AET', 'AZOST', 'HOVST', 'PHOT', 'FJST',
                 'ACST', 'NRT', 'EST', 'ULAST']
    timezones = [" {}".format(t.lower()) for t in timezones if t and len(t) > 2]
    date_string = date_string.lower()
    matching_timezone = [t for t in timezones if t in date_string]
    if matching_timezone:
        logger.info("Found time zone: {}".format(matching_timezone))
        ind = date_string.rfind(matching_timezone[0])
        date_string = date_string[:ind].strip()
    return date_string


def format_date(date_string, stronly=False):
    _date = date_string
    try:
        if type(_date) is not datetime:
            try:
                _date = int(_date)
            except:
                pass
            _date = str(_date)
            if str(_date).isdigit():
                _date = datetime.fromtimestamp(int(_date) / 1000)
                return _date
            else:
                date_string = date_string.strip("–").strip()
                date_string = date_string.lower()
                date_string = remove_timezone_from_date(date_string)
                date_string = date_string.replace("today at ", "").replace("today", "").strip()
                if "tomorrow" in date_string:
                    junks_strings = ["tomorrow at ", "by tomorrow", "tomorrow"]
                    for string in junks_strings:
                        date_string = date_string.replace(string, "").strip()
                    _date = dateutil.parser.parse(date_string)
                    _date = _date + timedelta(1)
                elif "yesterday" in date_string:
                    junks_strings = ["yesterday at ", "yesterday"]
                    for string in junks_strings:
                        date_string = date_string.replace(string, "").strip()
                    _date = dateutil.parser.parse(date_string)
                    _date = _date + timedelta(-1)
                else:
                    _date = dateutil.parser.parse(date_string)
        else:
            _date = date_string
        if stronly:
            return "{}-{}-{}".format(_date.year, _date.month, _date.day)
    except Exception as e:
        logger.error("Error is [{0}] at line [{1}] of date_string: [{2}]".format(
            str(e), sys.exc_info()[2].tb_lineno, date_string)
        )
    return _date if type(_date) is datetime else None
