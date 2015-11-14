# -*- coding: utf-8 -*-

import datetime
#import time
#import random
from sqlalchemy import select, distinct
#from mailer import Mailer
#from LocalFS import LocalFS
from zope.component import getMultiAdapter
from Products.Five import BrowserView
from zope.interface import implements
from z3c.sqlalchemy import getSAWrapper
#from Products.CMFPlone.utils import normalizeString
#from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
#from Products.CMFPlone.utils import normalizeString
from Products.CMFCore.utils import getToolByName
#from Products.CMFPlone import PloneMessageFactory as _
#from Products.AddRemoveWidget.AddRemoveWidget import AddRemoveWidget
#from Products.Archetypes.atapi import LinesField
#from Products.Archetypes.Renderer import renderer
#from Products.Archetypes.atapi import BaseContent
from interfaces import IManageFormation
#from collective.captcha.browser.captcha import Captcha


class ManageFormation(BrowserView):
    implements(IManageFormation)

    def getAllFormations(self):
        """
        table pg formation
        recuperation de toutes les formations
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        FormationTable = wrapper.getMapper('formation')
        query = session.query(FormationTable)
        query = query.order_by(FormationTable.form_titre)
        allFormations = query.all()
        return allFormations

    def getFormationByPk(self, formationPk):
        """
        table pg formation
        recuperation d'une formation selon sa pk
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        FormationTable = wrapper.getMapper('formation')
        query = session.query(FormationTable)
        query = query.filter(FormationTable.form_pk == formationPk)
        formation = query.one()
        return formation

    def getFormationsByListPk(self, formationPk):
        """
        table pg formation
        recuperation d'une formation selon sa pk
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        FormationTable = wrapper.getMapper('formation')
        query = session.query(FormationTable)
        query = query.filter(FormationTable.form_pk.in_(formationPk))
        formations = query.all()
        return formations

    def getFormationForInscription(self, inscriptionPk):
        """
        table pg formation, link_formation_inscription
        retourne les formaたions suivies par une personne inscrite
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LinkFormationInscriptionTable = wrapper.getMapper('link_formation_inscription')
        query = session.query(LinkFormationInscriptionTable)
        #for pk in inscriptionPk:
        query = query.filter(LinkFormationInscriptionTable.lnk_inscription_pk == inscriptionPk)
        formationsPk = query.all()

        formations = []
        for pk in formationsPk:
            formation = self.getFormationByPk(pk.lnk_formation_pk)
            formations.append(formation)
        return formations

    def getFormationOpen(self):
        """
        table pg formation
        recuperation d'une formation selon son état ouverte
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        FormationTable = wrapper.getMapper('formation')
        query = session.query(FormationTable)
        query = query.filter(FormationTable.form_etat == 'ouvert')
        formationsOpen = query.all()
        return formationsOpen

    def getTotalHeuresFormationSelected(self, formationPk):
        """
        table pg formation
        recuperation des formations selectionneés par la personne qui s'inscrit
        totalisation des heures de formation selectionnee
        si plus de 80, refus
        """
        nbreHeureFormation = 0
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        FormationTable = wrapper.getMapper('formation')
        query = session.query(FormationTable)
        query = query.filter(FormationTable.form_pk.in_(formationPk))
        formationSelected = query.all()
        for formation in formationSelected:
            nbreHeureFormation = nbreHeureFormation + int(formation.form_duree)
        return nbreHeureFormation

    def getFormationByLeffeSearch(self, searchString):
        """
        table pg formation
        recuperation d'une formation via le livesearch
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        FormationTable = wrapper.getMapper('formation')
        query = session.query(FormationTable)
        query = query.filter(FormationTable.form_titre.ilike("%%%s%%" % searchString))
        query = query.order_by(FormationTable.form_titre)
        formation = ["%s" % (elem.form_titre) for elem in query.all()]
        return formation

    def getSearchingFormation(self, formationPk=None, formationTitre=None):
        """
        table pg periodique
        recuperation du periodique selon la pk
        la pk peut arriver via le form en hidden ou via un lien construit,
         (cas du listing de resultat de moteur de recherche)
        je teste si la pk arrive par param, si pas je prends celle du form
        """
        fields = self.request.form
        if not formationTitre:
            formationTitre = fields.get('formationTitre')
        if not formationPk:
            formationPk = fields.get('formation_pk')

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        formationTable = wrapper.getMapper('formation')
        query = session.query(formationTable)
        if formationTitre:
            query = query.filter(formationTable.form_titre == formationTitre)
        if formationPk:
            query = query.filter(formationTable.form_pk == formationPk)
        searchingFormation = query.one()
        return searchingFormation

    def insertFormation(self):
        """
        table pg formation
        ajout d'un item formation
        """
        fields = self.request.form

        formationTitre = fields.get('formationTitre', None)
        formationDuree = fields.get('formationDuree', None)
        formationDateDebut = fields.get('formationDateDebut', None)
        formationDescription = fields.get('formationDescription', None)
        formationNiveauRequis = fields.get('formationNiveauRequis', None)
        formationEtat = fields.get('formationEtat', None)

        formationTitre = unicode(formationTitre, 'utf-8')
        formationDescription = unicode(formationDescription, 'utf-8')
        formationNiveauRequis = unicode(formationNiveauRequis, 'utf-8')

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        insertAuteur = wrapper.getMapper('formation')
        newEntry = insertAuteur(form_titre=formationTitre,
                                form_duree=formationDuree,
                                form_date_deb=formationDateDebut,
                                form_description=formationDescription,
                                form_niveau_requis=formationNiveauRequis,
                                form_etat=formationEtat)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)
        formationPk = newEntry.form_pk

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"La nouvelle formation %s  a bien été enregistrée !" % unicode(formationTitre, 'utf-8')
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-de-la-base/les-formations/admin-decrire-une-formation?formationPk=%s" % (portalUrl, formationPk)
        self.request.response.redirect(url)
        return ''

    def updateFormation(self):
        """
        table pg auteur
        mise a jour d'un item auteur
        """
        fields = self.request.form

        formationPk = fields.get('formationPk', None)
        formationTitre = fields.get('formationTitre', None)
        formationDuree = fields.get('formationDuree', None)
        formationDateDebut = fields.get('formationDateDebut', None)
        formationDescription = fields.get('formationDescription', None)
        formationNiveauRequis = fields.get('formationNiveauRequis', None)
        formationEtat = fields.get('formationEtat', None)

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        updateFormationTable = wrapper.getMapper('formation')
        query = session.query(updateFormationTable)
        query = query.filter(updateFormationTable.form_pk == formationPk)
        formations = query.all()
        for formation in formations:
            formation.form_titre = unicode(formationTitre, 'utf-8')
            formation.form_duree = unicode(formationDuree, 'utf-8')
            formation.form_date_deb = unicode(formationDateDebut, 'utf-8')
            formation.form_description = unicode(formationDescription, 'utf-8')
            formation.form_niveau_requis = unicode(formationNiveauRequis, 'utf-8')
            formation.form_etat = unicode(formationEtat, 'utf-8')

        session.flush()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"La formation %s a bien été modifiée !" % unicode(formationTitre, 'utf-8')
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-de-la-base/les-formations/admin-decrire-une-formation?formationPk=%s" % (portalUrl, formationPk)
        self.request.response.redirect(url)
        return ''

    def insertInscriptionFormation(self):
        """
        table pg inscription
        ajout d'un item inscription pour une formation
        """
        fields = self.request.form

        inscriptionFormationFk = fields.get('inscriptionFormationFk', None)
        inscriptionFormationCongeEducation = fields.get('inscriptionFormationCongeEducation', None)
        nbrHeureFormationSelected = self.getTotalHeuresFormationSelected(inscriptionFormationFk)

        #si on coche OUI au CONGE EDUCATION PAYE
        #et
        #si le total des heures est supérieur à 80h
        #alors bloquer inscription et envoyer message alerte

        if nbrHeureFormationSelected > 80 and inscriptionFormationCongeEducation == 'oui':
            portalUrl = getToolByName(self.context, 'portal_url')()
            ploneUtils = getToolByName(self.context, 'plone_utils')
            message = u"""
                        Votre demande d'inscription a échoué, vous avez sélectionné %s heures
                        alors que 80 heuressont permises !""" % (nbrHeureFormationSelected, )
            ploneUtils.addPortalMessage(message, 'info')
            url = "%s/formations/probleme-lors-de-l-inscription" % (portalUrl)
            self.request.response.redirect(url)
        else:
            jourNaisssance = fields.get('jour', None)
            moisNaisssance = fields.get('mois', None)
            anneeNaisssance = fields.get('annee', None)
            inscriptionFormationDateNaissance = "%s-%s-%s" % (jourNaisssance, moisNaisssance, anneeNaisssance)

            inscriptionFormationInscriptionDate = datetime.datetime.now()
            inscriptionFormationNom = fields.get('inscriptionFormationNom', None)
            inscriptionFormationPrenom = fields.get('inscriptionFormationPrenom', None)
            inscriptionFormationAdresse = fields.get('inscriptionFormationAdresse', None)
            inscriptionFormationCP = fields.get('inscriptionFormationCP', None)
            inscriptionFormationLocalite = fields.get('inscriptionFormationLocalite', None)
            inscriptionFormationEmail = fields.get('inscriptionFormationEmail', None)
            inscriptionFormationPhone = fields.get('inscriptionFormationPhone', None)
            inscriptionFormationGsm = fields.get('inscriptionFormationGsm', None)
            inscriptionFormationCentralProFgtb = fields.get('inscriptionFormationCentralProFgtb', None)
            inscriptionFormationRegional = fields.get('inscriptionFormationRegional', None)
            inscriptionFormationProfession = fields.get('inscriptionFormationProfession', None)
            inscriptionFormationEntreprise = fields.get('inscriptionFormationEntreprise', None)
            inscriptionFormationPhoneEntreprise = fields.get('inscriptionFormationPhoneEntreprise', None)
            inscriptionFormationHoraireTravail = fields.get('inscriptionFormationHoraireTravail', None)
            inscriptionFormationCongeSyndical = fields.get('inscriptionFormationCongeSyndical', None)
            inscriptionFormationDelegationSyndicale = fields.get('inscriptionFormationDelegationSyndicale', None)
            inscriptionFormationDelegationCE = fields.get('inscriptionFormationDelegationCE', None)
            inscriptionFormationDelegationCPPT = fields.get('inscriptionFormationDelegationCPPT', None)
            inscriptionFormationFormationSuivie = fields.get('inscriptionFormationFormationSuivie', None)

            inscriptionFormationInscriptionDate = datetime.datetime.now()
            listeFormations = ""
            formationsSelected = self.getFormationsByListPk(inscriptionFormationFk)
            #listeFormations = ["%s - " % (formation.form_titre) for formation in formationsSelected]

            for formation in formationsSelected:
                formationTitre = formation.form_titre
                listeFormations = listeFormations + formationTitre + ' - '
            lf = listeFormations.encode('ascii', 'ignore')


            wrapper = getSAWrapper('cenforsoc')
            session = wrapper.session
            insertAuteur = wrapper.getMapper('formation_inscription')
            newEntry = insertAuteur(form_ins_date=inscriptionFormationInscriptionDate,
                                    form_ins_nom=unicode(inscriptionFormationNom, 'utf-8'),
                                    form_ins_prenom=unicode(inscriptionFormationPrenom, 'utf-8'),
                                    form_ins_date_naissance=inscriptionFormationDateNaissance,
                                    form_ins_adresse=unicode(inscriptionFormationAdresse, 'utf-8'),
                                    form_ins_cp=inscriptionFormationCP,
                                    form_ins_localite=unicode(inscriptionFormationLocalite, 'utf-8'),
                                    form_ins_email=inscriptionFormationEmail,
                                    form_ins_tel=inscriptionFormationPhone,
                                    form_ins_gsm=inscriptionFormationGsm,
                                    form_ins_central_pro_fgtb=inscriptionFormationCentralProFgtb,
                                    form_ins_regional=inscriptionFormationRegional,
                                    form_ins_profession=inscriptionFormationProfession,
                                    form_ins_entreprise=inscriptionFormationEntreprise,
                                    form_ins_tel_entreprise=inscriptionFormationPhoneEntreprise,
                                    form_ins_horaire_travail=inscriptionFormationHoraireTravail,
                                    form_ins_conge_educ=inscriptionFormationCongeEducation,
                                    form_ins_conge_synd=inscriptionFormationCongeSyndical,
                                    form_ins_del_synd=inscriptionFormationDelegationSyndicale,
                                    form_ins_del_ce=inscriptionFormationDelegationCE,
                                    form_ins_del_cppt=inscriptionFormationDelegationCPPT,
                                    form_ins_formation_suivie=inscriptionFormationFormationSuivie)
            session.add(newEntry)
            session.flush()

            sujet = "CENFORSOC : demande d'inscription via le site"
            message = """
                  <font color='#FF0000'><b>:: INSCRIPTION FORMATION CENFORSOC ::</b></font><br /><br />
                  Formation(s) choisie(s) : <font color='#ff9c1b'><b>%s</b></font><br />
                  Nbre d'heures total : <font color='#ff9c1b'><b>%s</b></font><br />
                  <br />
                  Nom : <font color='#ff9c1b'><b>%s</b></font><br />
                  Prénom : <font color='#ff9c1b'><b>%s</b></font><br />
                  Date de Naissance : <font color='#ff9c1b'><b>%s</b></font><br />
                  Adresse : <font color='#ff9c1b'><b>%s</b></font><br />
                  Code Postal : <font color='#ff9c1b'><b>%s</b></font><br />
                  Localité : <font color='#ff9c1b'><b>%s</b></font><br />
                  E-mail : <font color='#ff9c1b'><b>%s</b></font><br />
                  Téléphone : <font color='#ff9c1b'><b>%s</b></font><br />
                  GSM : <font color='#ff9c1b'><b>%s</b></font><br />
                  <br />
                  Centrale professionnelle FGTB : <font color='#ff9c1b'><b>%s</b></font><br />
                  Régionale de : <font color='#ff9c1b'><b>%s</b></font><br />
                  Profession : <font color='#ff9c1b'><b>%s</b></font><br />
                  Entreprise : <font color='#ff9c1b'><b>%s</b></font><br />
                  Téléphone de l'entreprise : <font color='#ff9c1b'><b>%s</b></font><br />
                  <br />
                  Horaire de travail : <font color='#ff9c1b'><b>%s</b></font><br />
                  Congé éducation : <font color='#ff9c1b'><b>%s</b></font><br />
                  Congé syndical : <font color='#ff9c1b'><b>%s</b></font><br />
                  Mandat FGTB :<br />
                  &nbsp;&nbsp;. <font color='#ff9c1b'><b>%s</b></font><br />
                  &nbsp;&nbsp;. <font color='#ff9c1b'><b>%s</b></font><br />
                  &nbsp;&nbsp;. <font color='#ff9c1b'><b>%s</b></font><br />
                  <br />
                  Formations déjà suivies : <font color='#ff9c1b'><b>%s</b></font><br />
                  """ % (lf, nbrHeureFormationSelected, inscriptionFormationNom.upper(),
                         inscriptionFormationPrenom.capitalize(), inscriptionFormationDateNaissance,
                         inscriptionFormationAdresse, inscriptionFormationCP,
                         inscriptionFormationLocalite, inscriptionFormationEmail, inscriptionFormationPhone,
                         inscriptionFormationGsm, inscriptionFormationCentralProFgtb,
                         inscriptionFormationRegional, inscriptionFormationProfession,
                         inscriptionFormationEntreprise, inscriptionFormationPhoneEntreprise,
                         inscriptionFormationHoraireTravail,
                         inscriptionFormationCongeEducation, inscriptionFormationCongeSyndical,
                         inscriptionFormationDelegationSyndicale, inscriptionFormationDelegationCE,
                         inscriptionFormationDelegationCPPT, inscriptionFormationFormationSuivie)

            sujetInscrit = "CENFORSOC : confirmation de votre demande d'inscription"
            messageInscrit = """
                         Bonjour %s %s,
                         <br /><br />
                         Votre demande d'inscription pour la formation %s à bien été envoyée.
                         Vous recevrez une réponse sous peu.
                         <br /><br />
                         Bien à vous,
                         <br /><br />
                         L'équipe Cenforsoc.
                         """ % (inscriptionFormationPrenom, inscriptionFormationNom, lf)

            cenforsocTools = getMultiAdapter((self.context, self.request), name="manageCenforsoc")
            cenforsocTools.sendMailToCenforsoc(sujet, message)
            cenforsocTools.sendMailForInscription(sujetInscrit, messageInscrit, inscriptionFormationEmail)

            portalUrl = getToolByName(self.context, 'portal_url')()
            ploneUtils = getToolByName(self.context, 'plone_utils')
            message = u"Votre demande d'inscription a bien été enregistrée !"
            ploneUtils.addPortalMessage(message, 'info')
            url = "%s/formations/merci-inscription" % (portalUrl)
            self.request.response.redirect(url)
        return ''

    def gestionFormation(self):
        """
        insertion ou update d'une formation
        """
        fields = self.context.REQUEST
        operation = getattr(fields, 'operation')

        if operation == "insert":
            self.insertFormation()

        if operation == "update":
            self.updateFormation()

### INSCRIPTION  AUX FORMATIONS ####
    def getAllInscriptions(self):
        """
        table pg inscription
        recuperation de toutes les inscriptionss
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        InscriptionFormationTable = wrapper.getMapper('formation_inscription')
        query = session.query(InscriptionFormationTable)
        query = query.order_by(InscriptionFormationTable.form_ins_nom)
        allInscriptions = query.all()
        return allInscriptions

    def getAllDistinctInscriptions(self):
        """
        table pg inscription
        recuperation de toutes les inscriptionss
        """
        wrapper = getSAWrapper('cenforsoc')
        #session = wrapper.session
        InscriptionFormationTable = wrapper.getMapper('formation_inscription')
        #query = session.query(InscriptionFormationTable)
        allInscriptions = select([distinct(InscriptionFormationTable.form_ins_nom)], order_by=InscriptionFormationTable.form_ins_nom).execute().fetchall()
        #query = query.order_by(InscriptionFormationTable.form_ins_nom)
        #allInscriptions = query.all()
        return allInscriptions

    def getInscriptionByPk(self, inscriptionPk):
        """
        table pg inscription
        recuperation d'une inscription selon sa pk
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        InscriptionFormationTable = wrapper.getMapper('formation_inscription')
        query = session.query(InscriptionFormationTable)
        query = query.filter(InscriptionFormationTable.form_ins_pk == inscriptionPk)
        inscription = query.one()
        return inscription

    def getInscriptionFormationByLeffeSearch(self, searchString):
        """
        table pg formation-inscription
        recuperation d'une inscription a une formation par le nom via le livesearch
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        InscriptionFormationTable = wrapper.getMapper('formation_inscription')
        query = session.query(InscriptionFormationTable)
        query = query.filter(InscriptionFormationTable.form_ins_nom.ilike("%%%s%%" % searchString))
        inscription = ["%s" % (elem.form_ins_nom) for elem in query.all()]
        return inscription

    def getSearchingInscriptionFormation(self, isncriptionFormationPk=None, inscriptionNom=None):
        """
        table pg formation_inscription
        recuperation de l'inscription selon la pk
        la pk peut arriver via le form en hidden ou via un lien construit,
         (cas du listing de resultat de moteur de recherche)
        je teste si la pk arrive par param, si pas je prends celle du form
        """
        fields = self.request.form
        if not inscriptionNom:
            inscriptionNom = fields.get('inscriptionNom')
        if not isncriptionFormationPk:
            isncriptionFormationPk = fields.get('inscriptionPk')

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        InscriptionFormationTable = wrapper.getMapper('formation_inscription')
        query = session.query(InscriptionFormationTable)
        if inscriptionNom:
            searchingInscriptionFormation = query.filter(InscriptionFormationTable.form_ins_nom == inscriptionNom).distinct()
            #searchingInscriptionFormation = select([distinct(InscriptionFormationTable.form_ins_nom)], order_by=InscriptionFormationTable.form_ins_nom).execute().fetchall()
        if isncriptionFormationPk:
            query = query.filter(InscriptionFormationTable.form_ins_pk == isncriptionFormationPk)
            searchingInscriptionFormation = query.all()
        return searchingInscriptionFormation
