from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Physician(models.Model):
    _inherit = 'mate_hms.physician'

    def _phy_rec_count(self):
        Treatment = self.env['hms.treatment']
        Appointment = self.env['mate.appointment']
        Prescription = self.env['prescription.order']
        Patient = self.env['mate_hms.patient']
        for record in self.with_context(active_test=False):
            record.treatment_count = Treatment.search_count([('physician_id', '=', record.id)])
            record.appointment_count = Appointment.search_count([('physician_id', '=', record.id)])
            record.prescription_count = Prescription.search_count([('physician_id', '=', record.id)])
            record.patient_count = Patient.search_count(['|',('primary_physician_id','=',record.id), ('assignee_ids','in',record.partner_id.id)])

    consultaion_service_id = fields.Many2one('product.product', ondelete='restrict', string='Consultation Service')
    followup_service_id = fields.Many2one('product.product', ondelete='restrict', string='Followup Service')
    appointment_duration = fields.Float('Default Consultation Duration', default=0.25)

    is_primary_surgeon = fields.Boolean(string='Primary Surgeon')
    signature = fields.Binary('Signature')
    hr_presence_state = fields.Selection(related='user_id.employee_id.hr_presence_state')
    appointment_ids = fields.One2many("mate.appointment", "physician_id", "Appointments")

    treatment_count = fields.Integer(compute='_phy_rec_count', string='# Treatments')
    appointment_count = fields.Integer(compute='_phy_rec_count', string='# Appointment')
    prescription_count = fields.Integer(compute='_phy_rec_count', string='# Prescriptions')
    patient_count = fields.Integer(compute='_phy_rec_count', string='# Patients')

    def action_treatment(self):
        action = self.env["ir.actions.actions"]._for_xml_id("mate_hms.mate_action_form_hospital_treatment")
        action['domain'] = [('physician_id','=',self.id)]
        action['context'] = {'default_physician_id': self.id}
        return action

    def action_appointment(self):
        action = self.env["ir.actions.actions"]._for_xml_id("mate_hms.action_appointment")
        action['domain'] = [('physician_id','=',self.id)]
        action['context'] = {'default_physician_id': self.id}
        return action

    def action_prescription(self):
        action = self.env["ir.actions.actions"]._for_xml_id("mate_hms.act_open_hms_prescription_order_view")
        action['domain'] = [('physician_id','=',self.id)]
        action['context'] = {'default_physician_id': self.id}
        return action

    def action_patients(self):
        action = self.env["ir.actions.actions"]._for_xml_id("mate_hms_base.action_patient")
        action['domain'] = ['|',('primary_physician_id','=',self.id), ('assignee_ids','in',self.partner_id.id)]
        return action

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: