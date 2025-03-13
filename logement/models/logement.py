from odoo import models, fields, api
from datetime import datetime

class Logement(models.Model):
    _name = 'knsai.logement'
    _description = 'Logement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nom', required=True, tracking=True)
    reference = fields.Char(string='Référence', required=True, tracking=True)
    adresse = fields.Text(string='Adresse', required=True, tracking=True)
    surface = fields.Float(string='Surface (m²)', tracking=True)
    nb_pieces = fields.Integer(string='Nombre de pièces', tracking=True)
    etat = fields.Selection([
        ('neuf', 'Neuf'),
        ('bon', 'Bon état'),
        ('moyen', 'État moyen'),
        ('mauvais', 'Mauvais état')
    ], string='État', required=True, tracking=True)
    diagnostic = fields.Text(string='Diagnostic', tracking=True)
    date_diagnostic = fields.Date(string='Date du diagnostic', tracking=True)
    photos = fields.Many2many('ir.attachment', string='Photos')
    proprietaire_id = fields.Many2one('res.partner', string='Propriétaire', tracking=True)
    locataire_id = fields.Many2one('res.partner', string='Locataire actuel', tracking=True)
    date_creation = fields.Datetime(string='Date de création', default=fields.Datetime.now, readonly=True)
    date_modification = fields.Datetime(string='Dernière modification', compute='_compute_date_modification', store=True)

    @api.depends('write_date')
    def _compute_date_modification(self):
        for record in self:
            record.date_modification = record.write_date

    @api.model
    def create(self, vals):
        if not vals.get('reference'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('knsai.logement') or 'Nouveau'
        return super(Logement, self).create(vals) 