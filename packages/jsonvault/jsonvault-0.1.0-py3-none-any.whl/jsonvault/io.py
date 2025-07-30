from io import TextIOWrapper


def _open(fpath):
    return open(fpath, 'r+')

def close(fobj: TextIOWrapper):
    fobj.flush()
    fobj.close()
