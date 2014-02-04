import argparse, zipfile, os, sys, time, datetime
from os.path import join, getsize

def ark(rootDir, force=False, modbefore=None):
  toDelete = []

  zipname = 'ark.zip'
  origmodbefore = ''

  # convert modbefore
  if modbefore is not None:
    origmodbefore = modbefore
    modbefore = time.strptime(modbefore, '%Y-%m-%d')
    zipname = 'before-%s-ark.zip' % (origmodbefore)

  with zipfile.ZipFile(zipname, 'w', allowZip64=True) as z:
    for root, dirs, files in os.walk(rootDir):
      for f in files:
        x = '%s%s%s' % (root, os.sep, f)
        modtime = time.localtime(os.path.getmtime(x))

        if modbefore is not None:
          # add the file to the deletion array
          toDelete.append(x)
          if modtime < modbefore:
            z.write(x)

        else:
          z.write(x)

  # remove files
  if force == True:
    for f in toDelete:
      print 'Deleting: %s' % (f)
      os.remove(f)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()

  parser.add_argument('--force', dest='force', action='store_true', help='Delete files from disk that have been added to the archive')
  parser.add_argument('--modbefore', type=str, default=None, help='Set modified before date to limit the scope of the archive. YYYY-MM-DD')
  parser.add_argument('--dir', type=str, help='Root directory to search from')

  parser.set_defaults(force=False)

  args = parser.parse_args()

  ark(args.dir, args.force, args.modbefore)
