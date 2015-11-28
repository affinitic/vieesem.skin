# -*- coding: utf-8 -*-


def setupSite(context):
    if context.readDataFile('vieesem.skin_various.txt') is None:
        return
