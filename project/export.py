import dbfread


def convert(args):
    db = dbfread.dbf.DBF(args.filename)

    fieldnames = [f.name for f in db.fields]
    print(",".join(fieldnames))
    for record in db:
        values = []
        for field in db.fields:
            value = ''
            raw = record[field.name]
            # https://dbfread.readthedocs.io/en/latest/field_types.html
            if field.type in ('BCMV'):
                value = '"{}"'.format((raw or '').strip('\xa0 ').replace('"', '""'))
            elif field.type in ('@TD'):
                if raw:
                    value = raw.isoformat()
            elif field.type in ('FONIY+'):
                value = str(raw or 0)
            elif field.type in ('L'):
                value = 'true' if raw else 'false'
            else:
                raise Exception("Type {} not managed".format(field.type))
            values.append(value)
        print(",".join(values))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Convert DBF files.')
    parser.add_argument('-f', '--filename', metavar='filename', type=str,
                        help='Filename to convert')
    args = parser.parse_args()
    convert(args)
