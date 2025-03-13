from odoo import models, fields, api
from datetime import datetime

class Paiement(models.Model):
    _name = 'knsai.paiement'
    _description = 'Paiement de loyer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    name = fields.Char(string='Référence', required=True, copy=False, readonly=True, default=lambda self: 'Nouveau')
    bail_id = fields.Many2one('knsai.bail', string='Bail', required=True, tracking=True)
    date = fields.Date(string='Date', required=True, tracking=True)
    montant = fields.Float(string='Montant', required=True, tracking=True)
    type_paiement = fields.Selection([
        ('loyer', 'Loyer'),
        ('charges', 'Charges'),
        ('depot_garantie', 'Dépôt de garantie'),
        ('autre', 'Autre')
    ], string='Type de paiement', required=True, tracking=True)
    mode_paiement = fields.Selection([
        ('virement', 'Virement'),
        ('cheque', 'Chèque'),
        ('especes', 'Espèces'),
        ('autre', 'Autre')
    ], string='Mode de paiement', required=True, tracking=True)
    etat = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('valide', 'Validé'),
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
            vals['name'] = self.env['ir.sequence'].next_by_code('knsai.paiement') or 'Nouveau'
        return super(Paiement, self).create(vals)

    def action_valider(self):
        self.write({'etat': 'valide'})

    def action_annuler(self):
        self.write({'etat': 'annule'})

    def generer_quittance(self):
        self.ensure_one()
        return {
            'name': 'Générer une quittance',
            'type': 'ir.actions.act_window',
            'res_model': 'knsai.quittance.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_paiement_id': self.id,
                'default_bail_id': self.bail_id.id,
                'default_montant': self.montant,
                'default_date': self.date,
            }
        } 