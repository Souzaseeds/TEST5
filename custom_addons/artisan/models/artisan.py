from odoo import models, fields, api
from datetime import datetime

class Artisan(models.Model):
    _name = 'knsai.artisan'
    _description = 'Artisan'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nom', required=True, tracking=True)
    reference = fields.Char(string='Référence', required=True, tracking=True)
    type_artisan = fields.Selection([
        ('plombier', 'Plombier'),
        ('electricien', 'Électricien'),
        ('menuisier', 'Menuisier'),
        ('peintre', 'Peintre'),
        ('autre', 'Autre')
    ], string='Type d\'artisan', required=True, tracking=True)
    competence_ids = fields.Many2many('knsai.competence', string='Compétences')
    disponibilite = fields.Selection([
        ('disponible', 'Disponible'),
        ('occupe', 'Occupé'),
        ('indisponible', 'Indisponible')
    ], string='Disponibilité', required=True, tracking=True)
    telephone = fields.Char(string='Téléphone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    adresse = fields.Text(string='Adresse', tracking=True)
    siret = fields.Char(string='Numéro SIRET', tracking=True)
    assurance = fields.Text(string='Assurance', tracking=True)
    documents = fields.Many2many('ir.attachment', string='Documents')
    intervention_ids = fields.One2many('knsai.intervention', 'artisan_id', string='Interventions')
    date_creation = fields.Datetime(string='Date de création', default=fields.Datetime.now, readonly=True)
    date_modification = fields.Datetime(string='Dernière modification', compute='_compute_date_modification', store=True)

    @api.depends('write_date')
    def _compute_date_modification(self):
        for record in self:
            record.date_modification = record.write_date

    @api.model
    def create(self, vals):
        if not vals.get('reference'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('knsai.artisan') or 'Nouveau'
        return super(Artisan, self).create(vals)

class Competence(models.Model):
    _name = 'knsai.competence'
    _description = 'Compétence'

    name = fields.Char(string='Nom', required=True)
    description = fields.Text(string='Description')
    artisan_ids = fields.Many2many('knsai.artisan', string='Artisans')

class Intervention(models.Model):
    _name = 'knsai.intervention'
    _description = 'Intervention'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nom', required=True, tracking=True)
    artisan_id = fields.Many2one('knsai.artisan', string='Artisan', required=True, tracking=True)
    logement_id = fields.Many2one('knsai.logement', string='Logement', required=True, tracking=True)
    date_debut = fields.Datetime(string='Date de début', required=True, tracking=True)
    date_fin = fields.Datetime(string='Date de fin', tracking=True)
    etat = fields.Selection([
        ('planifie', 'Planifié'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé')
    ], string='État', required=True, tracking=True)
    description = fields.Text(string='Description', tracking=True)
    cout = fields.Float(string='Coût', tracking=True)
    documents = fields.Many2many('ir.attachment', string='Documents') 