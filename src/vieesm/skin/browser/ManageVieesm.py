# -*- coding: utf-8 -*-

import datetime
from mailer import Mailer
from Products.Five import BrowserView
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from Products.AddRemoveWidget.AddRemoveWidget import AddRemoveWidget
from Products.Archetypes.atapi import LinesField
from Products.Archetypes.Renderer import renderer
from Products.Archetypes.atapi import BaseContent
from interfaces import IManageVieesm


class ManageVieesm(BrowserView):
    implements(IManageVieesm)

# ### gestion des widgets kupu addRemoveList ###
    def getWysiwygField(self, name, value):
        """
        generates a WYSIWYG field containing value
        """

        class MyField:
            __name__ = name
            required = False
            default = value
            missing_value = None

        request = self.request
        request.form = {}
        field = WYSIWYGWidget(MyField(), request)
        return field()

    def getAddRemoveField(self,
                          name,
                          title,
                          values,
                          nameKey='name',
                          pkKey='pk',
                          selectedPks=[],
                          selectedNames=[],
                          canAddValues=False,
                          liveSearch=True):
        """
        generates an Add / Remove from list field with already selected pks
        nameKey and pkKey are used for the display value and the record pk to
        save
        """

        class MyContext(BaseContent):
            def getSelectedValues(self):
                return [str(pk) for pk in selectedPks]
                #if selectedNames:
                #    return selectedNames
        if not isinstance(nameKey, list):
            nameKey = [nameKey]
        items = []
        for value in values:
            if isinstance(value, dict):
                display = ' '.join([value.get(n) for n in nameKey])
                #display = ' '.join([n and getattr(value, n) or '-' for n in nameKey])
                term = (str(value.get(pkKey)), display)
            else:
                display = ' '.join([getattr(value, n) for n in nameKey])
                #display = ' '.join([n and getattr(value, n) or '-' for n in nameKey])
                term = (str(getattr(value, pkKey)), display)
            items.append(term)

        field = LinesField(name,
                           vocabulary=items,
                           edit_accessor='getSelectedValues',
                           enforceVocabulary=not canAddValues,
                           write_permission='View',
                           widget=AddRemoveWidget(size=10,
                                                  description='',
                                                  label=title,
                                                  liveSearch=liveSearch))

        wrappedContext = MyContext('dummycontext').__of__(self.context)
        widget = field.widget
        res = renderer.render(name, 'edit', widget, wrappedContext, field=field)
        return res

    def sendMail(self, sujet, message):
        """
        envoi de mail à vie-esem-admin, Thierry Vanloo
        "cenforsoc@brutele.be"
        """
        mailer = Mailer("localhost", "alain.meurant@affinitic.be")
        mailer.setSubject(sujet)
        mailer.setRecipients("alain.meurant@affinitic.be")
        mail = message
        mailer.sendAllMail(mail)

    def sendMailToVieesm(self, sujet, message):
        """
        envoi de mail à l'operateur dont les donnees change d'état
        """
        mailer = Mailer("localhost", 'cenforsoc@brutele.be')
        #mailer = Mailer("relay.skynet.be", 'alain.meurant@affinitic.be')
        mailer.setSubject(sujet)
        #recipients = "%s" % ('alain.meurant@skynet.be')
        recipients = "%s, %s, %s, %s" % ('alain.meurant@affinitic.be', 'cenforsoc@brutele.be', 'riet.vandeputte@fgtb.be', 'adriana.muccilli@fgtb.be')
        mailer.setRecipients(recipients)
        mail = message
        mailer.sendAllMail(mail)

    def sendMailForInscription(self, sujetInscrit, messageInscrit, emailInscrit):
        """
        envoi de mail à la personne qui a fait une demande d'inscription
        """
        mailer = Mailer("localhost", emailInscrit)
        #mailer = Mailer("relay.skynet.be", 'alain.meurant@skynet.be')
        mailer.setSubject(sujetInscrit)
        #recipients = "%s" % ('alain.meurant@skynet.be')
        recipients = "%s, %s, %s, %s, %s" % ('alain.meurant@affinitic.be', 'cenforsoc@brutele.be', 'riet.vandeputte@fgtb.be', 'adriana.muccilli@fgtb.be', emailInscrit)
        mailer.setRecipients(recipients)
        mail = messageInscrit
        mailer.sendAllMail(mail)

    def getTimeStamp(self):
        timeStamp = datetime.datetime.now()
        return timeStamp

    def getUserAuthenticated(self):
        """
        retourne le nom du user loggué
        """
        pm = getToolByName(self, 'portal_membership')
        user = pm.getAuthenticatedMember()
        user = user.getUserName()
        return user

    def getRoleUserAuthenticated(self):
        """
        retourne le nom du user loggué
        """
        pm = getToolByName(self.context, 'portal_membership')
        user = pm.getAuthenticatedMember()
        userRole = user.getRoles()
        return userRole
