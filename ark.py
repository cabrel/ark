import argparse, zipfile, os, sys, time, datetime
from os.path import join, getsize

def ark(rootDir, force=False, modbefore=None):
  toDelete = []

  with zipfile.ZipFile('ark.zip', 'w', allowZip64=True) as z:
    for root, dirs, files in os.walk(rootDir):
      for f in files:
        x = '%s%s%s' % (root, os.sep, f)
        z.write(x)

        modtime = os.path.getmtime(x)

        # add the file to the deletion
        # array
        if force is True:
          toDelete.append(x)

        # compare given time with file time
        if modbefore is not None:
          modbefore = datetime.strptime(modbefore, '%Y-%m-%d')
          print modbefore


if __name__ == '__main__':
  parser = argparse.ArgumentParser()

  parser.add_argument('--force', type=bool, default=False, help='Force delete files after adding them to the archive')
  parser.add_argument('--modbefore', type=str, default=None, help='Set modified before date to limit the scope of the archive. YYYY-MM-DD')
  parser.add_argument('--dir', type=str, help='Root directory to search from')

  args = parser.parse_args()

  ark(args.dir, args.force, args.modbefore)
