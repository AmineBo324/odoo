from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class FactureMailWizard(models.TransientModel):
    _name = "gestion.facture.mail.wizard"
    _description = "Prévisualisation Email Facture"

    facture_id = fields.Many2one('gestion.facture', string="Facture", required=True)
    subject = fields.Char(string="Objet")
    body_html = fields.Html(string="Contenu de l'email")
    email_to = fields.Char(string="Destinataire")
    email_from = fields.Char(string="Expéditeur")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        facture_id = self._context.get('active_id')
        if not facture_id:
            return res

        facture = self.env['gestion.facture'].browse(facture_id)
        template = self.env.ref("sensei.email_template_facture", raise_if_not_found=False)
        if template and facture:
            sender_email = template.email_from or 'facturation@mycompany.com'
            email_to = facture.client_id.email if facture.client_id else ''

            # Évaluation du template avec safe_eval pour remplacer ${object.xxx}
            from odoo.tools.safe_eval import safe_eval

            context = {'object': facture, 'user': self.env.user}
            subject = safe_eval("f'''{}'''".format(template.subject), context)
            body_html = safe_eval("f'''{}'''".format(template.body_html), context)

            res.update({
                'facture_id': facture.id,
                'subject': subject,
                'body_html': body_html,
                'email_to': email_to,
                'email_from': sender_email,
            })
        return res

    def action_envoyer_mail(self):
        template = self.env.ref("sensei.email_template_facture", raise_if_not_found=False)
        if not template:
            _logger.error("Le template d'email 'email_template_facture' est introuvable.")
            return False

        for wizard in self:
            facture = wizard.facture_id
            # Logger l'objet entier
            _logger.info("DEBUG object details: %s", facture.read()[0])
            client_name = facture.client_id.name or "Nom client inconnu"
            client_email = facture.client_id.email or "Email client inconnu"

            sender_email = template.email_from or "Expéditeur inconnu"

            _logger.info(
                f"Préparation envoi email pour le client : {client_name} <{client_email}> "
                f"depuis l'expéditeur : {sender_email}, facture {facture.name}"
            )

            if not facture.client_id.email:
                _logger.warning(f"Le client {client_name} n'a pas d'adresse email.")
                continue

            try:
                mail_id = template.send_mail(facture.id, force_send=True, raise_exception=True)
                _logger.info(f"Email envoyé avec succès pour {client_name} <{client_email}>, mail_id={mail_id}")
            except Exception as e:
                _logger.error(f"Erreur lors de l'envoi de l'email pour {client_name} <{client_email}> : {str(e)}")

