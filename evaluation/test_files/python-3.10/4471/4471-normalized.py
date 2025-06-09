def parse_duration(duration):
    """
    Parse duration string, such as '3h2m3s' into milliseconds

    >>> parse_duration('3h2m3s')
    10923000

    >>> parse_duration('0.3s')
    300

    >>> parse_duration('5')
    5000
    """
    _re_token = re.compile('([0-9.]+)([dhms]?)')

    def parse_token(time, multiplier):
        multipliers = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}
        if multiplier:
            if multiplier in multipliers:
                return int(float(time) * multipliers[multiplier] * 1000)
            else:
                raise StepperConfigurationError('Failed to parse duration: %s' % duration)
        else:
            return int(float(time) * 1000)
    return sum((parse_token(*token) for token in _re_token.findall(duration)))