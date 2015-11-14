# -*- coding: utf-8 -*-

from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface


class IVieesmTheme(IDefaultPloneLayer):
    """
    Theme for vie-esem
    """


class IManageVieesm(Interface):
    """
    outils communs
    """
    def getWysiwygField(name, value):
        """
        generates a WYSIWYG field containing value
        """

    def getAddRemoveField(name, title, values, nameKey='name', pkKey='pk', selectedPks=[]):
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
        insertion ou update d'un auteur
        """

    def getFormationByLeffeSearch(self, searchString):
        """
        table pg auteur
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
