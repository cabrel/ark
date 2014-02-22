import argparse, zipfile, os, sys, time, datetime, shutil
from os.path import join, getsize

def archive(zipPath, topDir, modbefore=None):
  """
    Performs a top-down enumeration starting at a given
    directory and adds any files found to a zip archive

    @zipPath    string   Path to use as the zip file we will create
    @topDir     string   Directory to start the dir walk from
    @modbefore  datetime A datetime object, if given, to filter which
                         objects are included in the archive
  """
  toDelete = []

  createZipMode = 'w'

  if os.path.isfile(zipPath):
    print "Appending to: %s" % (zipPath)
    createZipMode = 'a'
  else:
    print "Creating zip: %s" % (zipPath)

  with zipfile.ZipFile(zipPath, createZipMode, compression=zipfile.ZIP_DEFLATED, allowZip64=True) as z:
    for root, dirs, files in os.walk(topDir):
      for f in files:
        x = '%s%s%s' % (root, os.sep, f)
        modtime = time.localtime(os.path.getmtime(x))
        # add the file to the deletion array
        toDelete.append(x)

        if modbefore is not None:
          # if it was modified before the cutoff, add it
          # to the zip
          if modtime < modbefore:
            z.write(x)
        else:
          z.write(x)

  return toDelete


def ark(rootDir, forceDelete=False, acceptrisk=False, shallow=False, modbefore=None):
  """
    The controlling function for determining the appropriate properties
    or paths that should be given to archive


    @rootDir      string   Root directory
    @forceDelete  bool     Flag to set whether we will delete
                           files that are added to the archive
    @acceptrisk   bool     Flag to ensure its ok to delete folders
    @shallow      bool     Flag which forces first-level subdirectories
                           to be archived individually
    @modbefore  datetime A datetime object, if given, to filter which
                         objects are included in the archive
  """
  filesToDelete = []
  dirsToDelete = []

  rootDir = rootDir.rstrip(os.sep)

  if shallow == True:
    dirs = []

    # iterate over each first-level directory and archive those individually
    for d in os.listdir(rootDir):
      x = '%s%s%s' % (rootDir, os.sep, d)
      if os.path.isdir(x):
        dirs.append(x)
        filesToDelete += archive("%s.zip" % (x), x, modbefore)

    dirsToDelete += dirs

  else:
    filesToDelete = archive("%s.zip" % (rootDir), rootDir, modbefore)

  # remove files
  if forceDelete == True:
    print 'Deleting %s files' % (len(filesToDelete))
    for f in filesToDelete:
      os.remove(f)

    # acceptrisk allows directories to be deleted however, if modbefore
    # is set then a directory will never be deleted
    if modbefore is None and acceptrisk == True:
      print 'Deleting %s directories' % (len(dirsToDelete))
      for d in dirsToDelete:
        shutil.rmtree(d, ignore_errors=True)
    elif modbefore is not None:
      print '** Will not delete directories when modification time given **'
    elif acceptrisk == False and modbefore is None:
      print '** Without the acceptrisk flag, no directories will be deleted **'


if __name__ == '__main__':
  parser = argparse.ArgumentParser()

  parser.add_argument('--delete',
    dest='delete',
    action='store_true',
    help='Delete files from disk that have been added to the archive')

  parser.add_argument('--acceptrisk',
    dest='acceptrisk',
    action='store_true',
    help='Required flag to delete folders. Used in conjunction with --delete')

  parser.add_argument('--modbefore',
    type=str,
    default=None,
    help='Set modified before date to limit the scope of the archive. YYYY-MM-DD')

  parser.add_argument('--dir',
    type=str,
    help='Root directory to search from')

  parser.add_argument('--shallow',
    dest='shallow',
    action='store_true',
    help='Sets the flag to create multiple zip files under the immediate root')

  parser.set_defaults(delete=False)
  parser.set_defaults(acceptrisk=False)
  parser.set_defaults(shallow=False)

  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(0)

  args = parser.parse_args()
  modbefore = None

  if 'modbefore' in args and args.modbefore is not None:
    modbefore = time.strptime(args.modbefore, '%Y-%m-%d')

  ark(args.dir, args.delete, args.acceptrisk, args.shallow, modbefore)
