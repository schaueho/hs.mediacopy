import EXIF as exif

def parse_exif(file):
    "Parse exif tag from file"
    tags = None
    f = open(file, 'rb')
    try:
        tags = exif.process_file(f)
    except:
        pass
    return tags


