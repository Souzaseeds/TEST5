from odoo import models, fields, api

class RelanceWizard(models.TransientModel):
    _name = 'knsai.relance.wizard'
    _description = 'Assistant de génération de relance'

    bail_id = fields.Many2one('knsai.bail', string='Bail', required=True)
    relance_id = fields.Many2one('knsai.relance', string='Relance')
    date = fields.Date(string='Date', required=True)
    montant = fields.Float(string='Montant', required=True)
    type_relance = fields.Selection([
        ('premier_rappel', 'Premier rappel'),
        ('deuxieme_rappel', 'Deuxième rappel'),
        ('mise_en_demeure', 'Mise en demeure'),
        ('autre', 'Autre')
    ], string='Type de relance', required=True)
    commentaire = fields.Text(string='Commentaire')

    def action_generer(self):
        self.ensure_one()
        # Créer la relance
        relance = self.env['knsai.relance'].create({
            'bail_id': self.bail_id.id,
            'relance_id': self.relance_id.id if self.relance_id else False,
            'date': self.date,
            'montant': self.montant,
            'type_relance': self.type_relance,
            'commentaire': self.commentaire,
        })
        # Générer le PDF
        return self.env.ref('knsai_location.report_relance').report_action(relance) 