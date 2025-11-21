from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class Facture(models.Model):
    _name = "gestion.facture"
    _description = "Facture"

    name = fields.Char(
        string="Référence",
        required=True,
        copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('gestion.facture')
    )
    client_id = fields.Many2one("res.partner", string="Client", required=True)
    session_ids = fields.Many2many("gestion.session", string="Séances")
    date_facture = fields.Date(string="Date de facture", default=fields.Date.context_today)
    montant_total = fields.Float(string="Montant total", compute="_compute_montant_total", store=True)
    # etat = fields.Selection([
    #     ("brouillon", "Brouillon"),
    #     ("validee", "Validée"),
    #     ("payee", "Payée"),
    #     ("annulee", "Annulée"),
    # ], string="État", default="brouillon")

    @api.depends('session_ids', 'session_ids.tarif', 'session_ids.etat')
    def _compute_montant_total(self):
        for facture in self:
            facture.montant_total = sum(
                session.tarif for session in facture.session_ids if session.etat == 'terminee'
            )


    @api.model
    def generer_factures(self):
        """Créer automatiquement les factures pour toutes les séances terminées sans facture."""
        Session = self.env['gestion.session']
        Facture = self.env['gestion.facture']

        # Récupérer toutes les séances terminées qui n'ont pas encore de facture
        sessions = Session.search([('etat', '=', 'terminee'), ('facture_id', '=', False)])

        # Grouper par client
        clients = {}
        for session in sessions:
            clients.setdefault(session.client_id.id, []).append(session)

        # Créer les factures
        for client_id, sessions_client in clients.items():
            facture = Facture.create({
                'client_id': client_id,
                'session_ids': [(6, 0, [s.id for s in sessions_client])],
            })
            # lier les sessions à la facture
            for s in sessions_client:
                s.facture_id = facture.id    

    def action_preview_mail(self):
        """Ouvre le wizard pour prévisualiser le mail"""
        return {
            'name': 'Prévisualisation Email Facture',
            'type': 'ir.actions.act_window',
            'res_model': 'gestion.facture.mail.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('sensei.view_facture_mail_wizard').id,
            'target': 'new',
            'context': {'active_id': self.id},
        }
    