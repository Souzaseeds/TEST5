from odoo import models, fields, api
from datetime import datetime

class Relance(models.Model):
    _name = 'knsai.relance'
    _description = 'Relance de paiement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    name = fields.Char(string='Référence', required=True, copy=False, readonly=True, default=lambda self: 'Nouveau')
    bail_id = fields.Many2one('knsai.bail', string='Bail', required=True, tracking=True)
    date = fields.Date(string='Date', required=True, tracking=True)
    montant = fields.Float(string='Montant', required=True, tracking=True)
    type_relance = fields.Selection([
        ('premier_rappel', 'Premier rappel'),
        ('deuxieme_rappel', 'Deuxième rappel'),
        ('mise_en_demeure', 'Mise en demeure'),
        ('autre', 'Autre')
    ], string='Type de relance', required=True, tracking=True)
    etat = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('envoye', 'Envoyé'),
        ('annule', 'Annulé')
    ], string='État', default='brouillon', tracking=True)
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
            vals['name'] = self.env['ir.sequence'].next_by_code('knsai.relance') or 'Nouveau'
        return super(Relance, self).create(vals)

    def action_envoyer(self):
        self.ensure_one()
        # Envoyer l'email
        template = self.env.ref('knsai_location.email_template_relance')
        template.send_mail(
            self.id,
            force_send=True,
            raise_exception=True
        )
        self.write({'etat': 'envoye'})

    def action_annuler(self):
        self.write({'etat': 'annule'})

    def generer_relance(self):
        self.ensure_one()
        return {
            'name': 'Générer une relance',
            'type': 'ir.actions.act_window',
            'res_model': 'knsai.relance.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_relance_id': self.id,
                'default_bail_id': self.bail_id.id,
                'default_montant': self.montant,
                'default_date': self.date,
            }
        } 