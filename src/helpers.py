def round_fast(x, decimals=0):
    multiplier = 10 ** decimals
    return int(x * multiplier + 0.5 if x > 0 else x * multiplier - 0.5) / multiplier * 1.0