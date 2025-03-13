from odoo import models, fields, api
from datetime import datetime, timedelta

class Bail(models.Model):
    _name = 'knsai.bail'
    _description = 'Contrat de bail'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_debut desc'

    name = fields.Char(string='Référence', required=True, copy=False, readonly=True, default=lambda self: 'Nouveau')
    logement_id = fields.Many2one('knsai.logement', string='Logement', required=True, tracking=True)
    bailleur_id = fields.Many2one('res.partner', string='Bailleur', required=True, tracking=True)
    locataire_id = fields.Many2one('res.partner', string='Locataire', required=True, tracking=True)
    date_debut = fields.Date(string='Date de début', required=True, tracking=True)
    date_fin = fields.Date(string='Date de fin', required=True, tracking=True)
    montant_loyer = fields.Float(string='Montant du loyer', required=True, tracking=True)
    montant_charges = fields.Float(string='Charges', tracking=True)
    montant_depot_garantie = fields.Float(string='Dépôt de garantie', required=True, tracking=True)
    etat = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('actif', 'Actif'),
        ('termine', 'Terminé'),
        ('resilie', 'Résilié')
    ], string='État', default='brouillon', tracking=True)
    paiement_ids = fields.One2many('knsai.paiement', 'bail_id', string='Paiements')
    relance_ids = fields.One2many('knsai.relance', 'bail_id', string='Relances')
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
            vals['name'] = self.env['ir.sequence'].next_by_code('knsai.bail') or 'Nouveau'
        return super(Bail, self).create(vals)

    def action_activer(self):
        self.write({'etat': 'actif'})

    def action_terminer(self):
        self.write({'etat': 'termine'})

    def action_resilier(self):
        self.write({'etat': 'resilie'})

    def generer_quittance(self):
        self.ensure_one()
        return {
            'name': 'Générer une quittance',
            'type': 'ir.actions.act_window',
            'res_model': 'knsai.quittance.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_bail_id': self.id,
                'default_montant': self.montant_loyer + self.montant_charges,
                'default_date': fields.Date.today(),
            }
        }

    def generer_relance(self):
        self.ensure_one()
        return {
            'name': 'Générer une relance',
            'type': 'ir.actions.act_window',
            'res_model': 'knsai.relance.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_bail_id': self.id,
                'default_montant': self.montant_loyer + self.montant_charges,
                'default_date': fields.Date.today(),
            }
        }

    @api.model
    def _cron_relance_automatique(self):
        """Méthode appelée par la tâche planifiée pour gérer les relances automatiques"""
        # Récupérer tous les baux actifs
        baux = self.search([('etat', '=', 'actif')])
        
        # Pour chaque bail
        for bail in baux:
            # Vérifier si le loyer du mois en cours a été payé
            today = fields.Date.today()
            debut_mois = today.replace(day=1)
            fin_mois = (debut_mois + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            # Récupérer les paiements du mois en cours
            paiements_mois = bail.paiement_ids.filtered(lambda p: 
                p.date >= debut_mois and 
                p.date <= fin_mois and 
                p.type_paiement == 'loyer' and 
                p.etat == 'valide'
            )
            
            # Si aucun paiement n'a été effectué
            if not paiements_mois:
                # Vérifier s'il n'y a pas déjà une relance pour ce mois
                relances_mois = bail.relance_ids.filtered(lambda r: 
                    r.date >= debut_mois and 
                    r.date <= fin_mois and 
                    r.etat == 'envoye'
                )
                
                # Si aucune relance n'a été envoyée
                if not relances_mois:
                    # Créer une nouvelle relance
                    self.env['knsai.relance'].create({
                        'bail_id': bail.id,
                        'date': today,
                        'montant': bail.montant_loyer + bail.montant_charges,
                        'type_relance': 'premier_rappel',
                    }) 