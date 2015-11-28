# -*- coding: utf-8 -*-

from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface


class IVieesemTheme(IDefaultPloneLayer):
    """
    Theme for vie-esem
    """


class IManageVieesem(Interface):
    """
    outils communs
    """
    def getWysiwygField(self, name, value):
        """
        generates a WYSIWYG field containing value
        """

    def getAddRemoveField(self, name, title, values, nameKey='name', pkKey='pk', selectedPks=[]):
        """
        generates an Add / Remove from list field with already selected pks
        nameKey and pkKey are used for the display value and the record pk to
        save
        """


class IManageFormation(Interface):
    """
    gestion des demandes de formations
    """
    def gestionFormation():
        """
        insertion ou update d'une formation
        """

    def getFormationByLeffeSearch(self, searchString):
        """
        table pg formation
        recuperation d'une formation via le livesearch
        """
    def insertFormation():
        """
        insert a new item in formation
        """
    def updateFormation():
        """
        update items in formation
        """
