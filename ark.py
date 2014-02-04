import argparse, zipfile, os, sys, time, datetime
from os.path import join, getsize

def archive(zipPath, topDir, modbefore=None):
  toDelete = []

  with zipfile.ZipFile(zipPath, 'w', allowZip64=True) as z:
    print "Creating %s" % (zipPath)
    for root, dirs, files in os.walk(topDir):
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

  return toDelete


def ark(rootDir, force=False, shallow=False, modbefore=None):
  if shallow == True:
    dirs = []

    for d in os.listdir(rootDir):
      x = '%s%s%s' % (rootDir, os.sep, d)
      if os.path.isdir(x):
        dirs.append(x)
        archive("%s.zip" % (x), modbefore)
  # else:
  #   with zipfile.ZipFile(zipname, 'w', allowZip64=True) as z:
  #     for root, dirs, files in os.walk(rootDir):
  #       for f in files:
  #         x = '%s%s%s' % (root, os.sep, f)
  #         modtime = time.localtime(os.path.getmtime(x))

  #         if modbefore is not None:
  #           # add the file to the deletion array
  #           toDelete.append(x)
  #           if modtime < modbefore:
  #             z.write(x)

  #         else:
  #           z.write(x)

  #   # remove files
  #   if force == True:
  #     for f in toDelete:
  #       print 'Deleting: %s' % (f)
  #       os.remove(f)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()

  parser.add_argument('--force', dest='force', action='store_true', help='Delete files from disk that have been added to the archive')

  parser.add_argument('--modbefore', type=str, default=None, help='Set modified before date to limit the scope of the archive. YYYY-MM-DD')

  parser.add_argument('--dir', type=str, help='Root directory to search from')

  parser.add_argument('--shallow', dest='shallow', action='store_true', help='Sets the flag to create multiple zip files under the immediate root')

  parser.set_defaults(force=False)
  parser.set_defaults(shallow=False)

  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(0)

  args = parser.parse_args()
  modbefore = None

  if 'modbefore' in args:
    modbefore = time.strptime(args.modbefore, '%Y-%m-%d')

  ark(args.dir, args.force, args.shallow, modbefore)
