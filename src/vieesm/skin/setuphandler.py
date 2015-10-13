# -*- coding: utf-8 -*-


def setupSite(context):
    if context.readDataFile('vieesm.skin_various.txt') is None:
        return
