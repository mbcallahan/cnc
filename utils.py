import re

def get_bits(value, bit_count):
    bits = []
    number = int(value, 16)
    for i in range(0, bit_count):
        bits.append((number & (1 << i)) >> i)
    return bits

def get_bytes_of_uint32(n):
    for i in range(4):
        yield chr((n >> (24-8*i) & 0xFF))

def binary_search(min_val, max_val, precision):
    val = (min_val + max_val) / 2
    search_size = val

    while 1:
        result = yield val
        if search_size < precision:
            break

        search_size = search_size / 2

        if result:
            val -= search_size
        else:
            val += search_size

    return val

def display_rate(rate, unit='Hz'):
    magnitudes = (('G', 1000 ** 3), ('M', 1000 ** 2), ('k', 1000))

    for m in magnitudes:
        if rate >= m[1] and rate % m[1] == 0:
            value = rate // m[1]
            prefix = m[0]
            break
    else:
        value = rate
        prefix = ''

    return '{} {}{}'.format(value, prefix, unit)

def parse_rate(rate):
    match = re.match('(\d+) ?([kMG]?)', rate)
    if not match:
        return

    try:
        unit = {'': 1, 'k': 1000, 'M': 1000 ** 2, 'G': 1000 ** 3}[match.group(2)]
        rate = int(match.group(1)) * unit

        if rate == 0:
            raise exceptions.ClockTooFast('Cannot have a clock rate of 0 Hz')
        else:
            return rate

    except (KeyError, ValueError):
        pass

def input_rate(*args):
    while True:
        rate = parse_rate(input(*args))

        if rate is None:
            print('Invalid rate')
        else:
            return rate

def parse_duration(val):
    units = {'s': 1, 'ms': 1000, 'us': 1000**2}
    match = re.match('(\d+(.\d+)?) ?([mu]?s)?', val)
    if match:
        unit = match.group(3)

        if '.' in match.group(1):
            duration = float(match.group(1))
        else:
            duration = int(match.group(1))

        if unit:
            duration = duration / units[unit]

    return duration

def input_duration(*args):
    while 1:
        userval = input(*args).strip()
        duration = parse_duration(userval)

        if duration is not None:
            break
        else:
            print('Invalid duration, try again.')

    return duration

def parse_percent(val):
    is_fraction = True
    if '%' in val:
        val = val.replace('%', '')
        is_fraction = False

    val = val.strip()

    val = float(val)
    if val > 1 or not is_fraction:
        val = val / 100

    return val

def prompt_yesno(*args):
    return input(*args).lower().strip() in ('y', 'yes')
