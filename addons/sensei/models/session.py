from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError


class Session(models.Model):
    _name = 'gestion.session'
    _description = 'Séance de coaching / consulting / psy'

    name = fields.Char(string="Nom", compute="_compute_name")
    type_seance = fields.Selection([
        ('coaching', 'Coaching'),
        ('psychologie', 'Psychologie'),
        ('consulting', 'Consulting'),
    ], string="Type de séance", required=True)
    utilisateur_id = fields.Many2one('gestion.utilisateur', string='Employé', required=True)
    client_id = fields.Many2one('res.partner', string='Client', required=True)
    facture_id = fields.Many2one("gestion.facture", string="Facture", readonly=True)
    date_seance = fields.Datetime(string="Date et heure de la séance", required=True)
    duree = fields.Float(string="Durée (heures)", required=True)
    tarif = fields.Float(string="Tarif (€)", compute="_compute_tarif", store=True)
    etat = fields.Selection([
        ('prevue', 'Prévue'),
        ('annulee', 'Annulée'),
        ('terminee', 'Terminée'),
    ], string='État', default='prevue', required=True)
    description = fields.Text(string="Description")


    @api.depends('type_seance')
    def _compute_name(self):
        for rec in self:
            rec.name = dict(self._fields['type_seance'].selection).get(rec.type_seance, '') if rec.type_seance else 'Séance'
    
    # Calcul du tarif selon type de séance
    @api.depends('type_seance', 'duree')
    def _compute_tarif(self):
        for rec in self:
            tarif_horaire = 0
            if rec.type_seance == 'coaching':
                tarif_horaire = 80
            elif rec.type_seance == 'psychologie':
                tarif_horaire = 60
            elif rec.type_seance == 'consulting':
                tarif_horaire = 100
            else:
                tarif_horaire = 0
            
            rec.tarif = tarif_horaire * (rec.duree or 0)

    def update_sessions_terminees(self):
        now = fields.Datetime.now()
        sessions = self.search([
            ('etat', '!=', 'terminee'),
            ('date_seance', '<=', now),
        ])
        for session in sessions:
            date_fin = session.date_seance + timedelta(hours=session.duree)
            if date_fin <= now:
                session.etat = 'terminee'


    @api.constrains('utilisateur_id', 'client_id', 'date_seance', 'duree')
    def _check_disponibilite(self):
        for rec in self:
            if not rec.utilisateur_id or not rec.client_id or not rec.date_seance or not rec.duree:
                continue

            date_debut = rec.date_seance
            date_fin = date_debut + timedelta(hours=rec.duree)

            # Vérifier chevauchement pour l'utilisateur
            conflits_utilisateur = self.env['gestion.session'].search([
                ('id', '!=', rec.id),
                ('utilisateur_id', '=', rec.utilisateur_id.id),
                ('etat', 'in', ['prevue', 'terminee']),
                ('date_seance', '<', date_fin),
                ('date_seance', '>=', date_debut - timedelta(hours=24)),
            ])

            for conflit in conflits_utilisateur:
                conflit_fin = conflit.date_seance + timedelta(hours=conflit.duree)
                if date_debut < conflit_fin and date_fin > conflit.date_seance:
                    raise ValidationError(
                        f"L'utilisateur {rec.utilisateur_id.name} a déjà une séance "
                        f"entre {conflit.date_seance.strftime('%Y-%m-%d %H:%M')} et {conflit_fin.strftime('%Y-%m-%d %H:%M')}."
                    )
            
            # Vérifier chevauchement pour le client
            conflits_client = self.env['gestion.session'].search([
                ('id', '!=', rec.id),
                ('client_id', '=', rec.client_id.id),
                ('etat', 'in', ['prevue', 'terminee']),
                ('date_seance', '<', date_fin),
                ('date_seance', '>=', date_debut - timedelta(hours=24)),
            ])

            for conflit in conflits_client:
                conflit_fin = conflit.date_seance + timedelta(hours=conflit.duree)
                if date_debut < conflit_fin and date_fin > conflit.date_seance:
                    raise ValidationError(
                        f"Le client {rec.client_id.name} a déjà une séance "
                        f"entre {conflit.date_seance.strftime('%Y-%m-%d %H:%M')} et {conflit_fin.strftime('%Y-%m-%d %H:%M')}."
                    )

