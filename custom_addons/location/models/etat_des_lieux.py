from odoo import models, fields, api
from datetime import datetime

class EtatDesLieux(models.Model):
    _name = 'knsai.etat_des_lieux'
    _description = 'État des lieux'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    name = fields.Char(string='Référence', required=True, copy=False, readonly=True, default=lambda self: 'Nouveau')
    bail_id = fields.Many2one('knsai.bail', string='Bail', required=True, tracking=True)
    type = fields.Selection([
        ('entree', 'Entrée'),
        ('sortie', 'Sortie')
    ], string='Type', required=True, tracking=True)
    date = fields.Date(string='Date', required=True, tracking=True)
    commentaire = fields.Text(string='Commentaire', tracking=True)
    photos = fields.Many2many('ir.attachment', string='Photos')
    documents = fields.Many2many('ir.attachment', string='Documents')
    date_creation = fields.Datetime(string='Date de création', default=fields.Datetime.now, readonly=True)
    date_modification = fields.Datetime(string='Dernière modification', compute='_compute_date_modification', store=True)

    @api.depends('write_date')
    def _compute_date_modification(self):
        for record in self:
            record.date_modification = record.write_date

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nouveau') == 'Nouveau':
            vals['name'] = self.env['ir.sequence'].next_by_code('knsai.etat_des_lieux') or 'Nouveau'
        return super(EtatDesLieux, self).create(vals)

    def action_envoyer(self):
        self.ensure_one()
        # Envoyer l'email
        template = self.env.ref('knsai_location.email_template_etat_des_lieux')
        template.send_mail(
            self.id,
            force_send=True,
            raise_exception=True
        ) 