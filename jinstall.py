#!/usr/local/bin/python2.7

import os
import sys

uname = os.uname()
bsd_arch = uname[-1]
bsd_ver = uname[2].split('-')[0]
bsd_pks = ['base.txz', 'lib32.txz']
outdir = '/usr/freebsd-dist'

if bsd_arch != "amd64":
   i = bsd_pks.index("lib32")
   del bsd_pks[i]

def bsd_download():
   if bsd_arch != "amd64":
      i = bsd_pks.index("lib32")
      del bsd_pks[i]

   if not os.path.exists(outdir):
      os.mkdir(outdir)

   for p in  bsd_pks:
      if os.path.exists("%s/%s" % (outdir, p)):
         yes = raw_input("replace existing  %s/%s (y)> " % (outdir, p))
         if 'y' not in yes:
            continue
      os.system("fetch -q -1 ftp://ftp.freebsd.org/pub/FreeBSD/releases/%s/%s-RELEASE/%s -o %s" % (bsd_arch, bsd_ver, p, outdir))


def bsd_install(jaildir):
  if os.path.exists(jaildir):
     print '%s exist' % jaildir
  else:
     os.mkdir(jaildir)
  for i in bsd_pks:
    os.system("tar xfp %s/%s -C %s" % (outdir, i, jaildir))

def bsd_skel(path):
   os.chdir('%s' % path)
   if not os.path.exists('%s/usr/ports' %path):
      os.system('mkdir -p %s/usr/ports' % path)
   os.system('mkdir -p %s/SROOT/home %s/SROOT/usr-X11R6 %s/SROOT/distfiles %s/SROOT/usr-share-keys %s/SROOT/compat' % (path,  path, path, path, path))
   os.system('mv %s/etc SROOT/' % path)
   os.system('mv %s/usr/local SROOT/usr-local' % path)
   os.system('mv %s/usr/share/keys/* SROOT/usr-share-keys/' % path)
   os.system('rm -rf %s/usr/share/keys/' % path)
   os.system('mv %s/tmp SROOT/' % path)
   os.system('chmod 1777 SROOT/tmp')
   os.system('mv %s/var SROOT/' % path)
   os.system('mv %s/root SROOT/' % path)
   os.system('ln -s SROOT/etc etc')
   os.system('ln -s SROOT/home home')
   os.system('ln -s SROOT/root root')
   os.system('ln -s /SROOT/usr-local usr/local')
   os.system('ln -s /SROOT/usr-share-keys usr/share/keys')
   os.system('ln -s /SROOT/usr-X11R6 usr/X11R6')
   os.system('ln -s /SROOT/distfiles usr/ports/distfiles')
   os.system('ln -s SROOT/tmp tmp')
   os.system('chmod 1777 %s/SROOT/tmp/' % path)
   os.system('ln -s SROOT/var var')
   os.system('ln -s SROOT/compat compat')
   os.system('echo  \"WRKDIRPREFIX?=  /SROOT/portbuild\"  > %s/etc/make.conf' % path)

def create_jail(base, jail):
   os.system('mkdir -p %s/rw %s/mnt' % (jail, jail))
   os.system('cp -R  %s/SROOT/ %s/rw/' % (base, jail))
   os.system('echo \"%s %s/mnt nullfs ro 0 0\" > %s/rw/etc/fstab' % (base, jail, jail))
   os.system('echo \"%s/rw %s/mnt/SROOT nullfs rw 0 0\" >> %s/rw/etc/fstab' % (jail, jail, jail))

# MAIN
bjdir = sys.argv[1]
njdir = sys.argv[2]

bsd_download()
bsd_install(bjdir)
bsd_skel(bjdir)
create_jail(bjdir, njdir)
