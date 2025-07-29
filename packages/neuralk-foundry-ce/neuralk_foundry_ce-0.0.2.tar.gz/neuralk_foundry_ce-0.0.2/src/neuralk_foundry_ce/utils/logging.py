def log(verbose, level, message):
    if level <= verbose:
        print(message)