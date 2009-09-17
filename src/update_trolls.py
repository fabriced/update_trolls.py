#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
  SYNOPSIS
    update_trolls.py [--mouche] [--equipement] [--vue <id1>[,<id2>,..]] [--gowaps <id1>[,<id2>,.].] [--aptitudes] [--bonus] [--no-profil] [--debug] [--force]

  DESCRIPTION
    Script de mise a jour du système tactique des bricoltrolls. Par défaut,
    seul le profil des trolls est mis à jour.

  OPTIONS
    --mouche
      mets à jour les mouches

    --equipement
      mets à jour l'équipement et les gigots

    --aptitudes
      mets à jour les competenes et sortileges

    --bonus
      mets à jour les bonus et malus

    --vue <id1>[,<id2>..]
      mets à jour la vue des trolls specifies

    --gowaps <id1>[,<id2>..]
      mets à jour les gowaps des trolls specifies

    --no-profil
      désactive la mise à jour du profil des trolls

    --debug
      active le mode debug, les mises a jours ne sont pas effectuées

    --help
      affiche ce message

    --force
      force l'exécution de la mise à jour sans vérifier l'existence de lockfile

  FILES
    update_trolls_settings.py containt the login informations to the website
      and the trolls settings

"""

import os
import sys, getopt
from mechanize import Browser
from time import sleep

from update_trolls_settings import *

DEBUG = LOCKCHECK_REQUIRED = False

login_url = "%s/%s/login.php" % (website, coterie)

full_update_url        = "%s/%s/update_info.php?id=" % (website, coterie)
mouche_update_url      = "%s/%s/update_mouche.php?id=" % (website, coterie)
equipement_update_url  = "%s/%s/update_equipement.php?id=" % (website, coterie)
bonus_update_url          = "%s/%s/update_bonusmalus.php?id=" % (website, coterie)
GG_update_url          = "%s/%s/update_gigots.php?id=" % (website, coterie)
aptitudes_update_url = "%s/%s/update_aptitudes.php?id=" % (website, coterie)
vue_update_url         = "%s/%s/update_vue.php?id=" % (website, coterie)
gowaps_update_url      = "%s/%s/update_gowaps.php?id=" % (website, coterie)

UPDATE_PROFILE = True
UPDATE_MOUCHE = False
UPDATE_EQUIPEMENT = False
UPDATE_APTITUDES = False
UPDATE_BONUS = False
UPDATE_GOWAPS = False
GOWAPS_LIST = []
UPDATE_VUE = False
VUE_LIST = []

def run_update():
  global DEBUG, UPDATE_PROFILE, UPDATE_MOUCHE, UPDATE_EQUIPEMENT, UPDATE_VUE, UPDATE_APTITUDES, UPDATE_BONUS, UPDATE_GOWAPS
  global VUE_LIST, GOWAPS_LIST

  br = Browser()
  br.set_debug_redirects(DEBUG)
  br.set_debug_http(DEBUG)
  if not DEBUG:
    br.set_handle_robots( False )
    br.set_handle_refresh( False )


    br.open(login_url)

    # gros hack tout laid car le formulaire n'a pas de nom
    form_list = []
    for f in br.forms():
      form_list.append(f)
    form_list[0].__dict__['name']='toto'
    # fin du gros hack tout moche

    br.select_form('toto')
    br['login'] = username
    br['password'] = password
    br.submit()

  for troll in trolls.keys():
    printed =  "MAJ de %s" % trolls[troll]['nom']
    if UPDATE_PROFILE:
      printed += " profil"
      if not DEBUG:
        br.open("%s%d" % (full_update_url, troll))
        sleep(sleep_time)
    if UPDATE_MOUCHE:
      printed += " mouches"
      if not DEBUG:
        br.open("%s%d" % (mouche_update_url, troll))
        sleep(sleep_time)
    if UPDATE_EQUIPEMENT:
      printed += " equipement"
      if not DEBUG:
        br.open("%s%d" % (equipement_update_url, troll))
        sleep(sleep_time)
        br.open("%s%d" % (GG_update_url, troll))
        sleep(sleep_time)
    if UPDATE_VUE and str(troll) in VUE_LIST:
      printed += " vue"
      if not DEBUG:
        br.set_handle_redirect( False )
        try:
          br.open("%s%d" % (vue_update_url, troll))
        except:
          br.set_handle_redirect( True )
          pass
        sleep(sleep_time)
    if UPDATE_GOWAPS and str(troll) in GOWAPS_LIST:
      printed += " gowaps"
      if not DEBUG:
        br.open("%s%d" % (gowaps_update_url, troll))
        sleep(sleep_time)
    if UPDATE_APTITUDES:
      printed += " competences"
      if not DEBUG:
        br.open("%s%d" % (aptitudes_update_url, troll))
        sleep(sleep_time)
    if UPDATE_BONUS:
      printed += " bonus"
      if not DEBUG:
        br.open("%s%d" % (bonus_update_url, troll))
        sleep(sleep_time)
    print printed

def read_options():
  global DEBUG, LOCKCHECK_REQUIRED, UPDATE_PROFILE, UPDATE_MOUCHE, UPDATE_EQUIPEMENT, UPDATE_VUE, UPDATE_APTITUDES, UPDATE_BONUS, UPDATE_GOWAPS
  global VUE_LIST, GOWAPS_LIST

  try:
    options, foo = getopt.getopt (sys.argv[1:], "mev:nabg:dhf",
              ['mouche', 'equipement', 'vue=', 'no-profil', 'aptitudes', 'bonus', 'gowaps=',
               'debug', 'help', 'force'])
  except getopt.GetoptError, desc:
    print __doc__
    sys.exit(1)

  for option, val in options:
    if option in ('-m', '--mouche'):
      UPDATE_MOUCHE = True

    elif option in ('-e', '--equipement'):
      UPDATE_EQUIPEMENT = True

    elif option in ('-v', '--vue'):
      if val:
        UPDATE_VUE = True
        VUE_LIST += val.split(',')

    elif option in ('-g', '--gowaps'):
      if val:
        UPDATE_GOWAPS = True
        GOWAPS_LIST += val.split(',')

    elif option in ('-a', '--aptitudes'):
      UPDATE_APTITUDES = True

    elif option in ('-b', '--bonus'):
      UPDATE_BONUS = True

    elif option in ('-n', '--no-profil'):
      UPDATE_PROFILE = False

    elif option in ('-d', '--debug'):
      DEBUG = True

    elif option in ('-h', '--help'):
      print __doc__
      sys.exit(0)

    elif option in ('-f', '--force'):
      LOCKCHECK_REQUIRED = True

if __name__ == '__main__':
  if LOCKCHECK_REQUIRED and os.access(LOCKFILE, os.F_OK):
    print >> sys.stderr, "update deja en cours"
    sys.exit(-1)

  read_options()
  run_update()
