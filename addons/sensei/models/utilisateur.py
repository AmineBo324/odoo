from odoo import models, fields

class Utilisateur(models.Model):
    _name = 'gestion.utilisateur'
    _description = 'Utilisateur (Coach, Consultant, Psychologue)'

    name = fields.Char(string='Nom complet', required=True)
    role = fields.Selection([
        ('coach', 'Coach'),
        ('consultant', 'Consultant'),
        ('psychologue', 'Psychologue'),
    ], string='Rôle', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Téléphone')
    address = fields.Text(string='Adresse')
    specialty = fields.Char(string='Spécialité')
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Actif', default=True)
