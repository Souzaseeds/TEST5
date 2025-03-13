from odoo import models, fields, api

class QuittanceWizard(models.TransientModel):
    _name = 'knsai.quittance.wizard'
    _description = 'Assistant de génération de quittance'

    bail_id = fields.Many2one('knsai.bail', string='Bail', required=True)
    paiement_id = fields.Many2one('knsai.paiement', string='Paiement')
    date = fields.Date(string='Date', required=True)
    montant = fields.Float(string='Montant', required=True)
    periode_debut = fields.Date(string='Période début', required=True)
    periode_fin = fields.Date(string='Période fin', required=True)
    commentaire = fields.Text(string='Commentaire')

    def action_generer(self):
        self.ensure_one()
        # Créer la quittance
        quittance = self.env['knsai.quittance'].create({
            'bail_id': self.bail_id.id,
            'paiement_id': self.paiement_id.id if self.paiement_id else False,
            'date': self.date,
            'montant': self.montant,
            'periode_debut': self.periode_debut,
            'periode_fin': self.periode_fin,
            'commentaire': self.commentaire,
        })
        # Générer le PDF
        return self.env.ref('knsai_location.report_quittance').report_action(quittance) 