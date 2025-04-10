from odoo import fields, models, _
from odoo.exceptions import AccessError


class Digest(models.Model):
    _inherit = 'digest.digest'

    kpi_mate_appointment_total = fields.Boolean('New Appointments')
    kpi_mate_appointment_total_value = fields.Integer(compute='_compute_kpi_mate_appointment_total_value')

    kpi_mate_treatment_total = fields.Boolean('New Treatments')
    kpi_mate_treatment_total_value = fields.Integer(compute='_compute_kpi_mate_treatment_total_value')

    kpi_mate_procedure_total = fields.Boolean('New Procedures')
    kpi_mate_procedure_total_value = fields.Integer(compute='_compute_kpi_mate_procedure_total_value')

    kpi_mate_evaluation_total = fields.Boolean('New Evaluation')
    kpi_mate_evaluation_total_value = fields.Integer(compute='_compute_kpi_mate_evaluation_total_value')

    kpi_mate_patients_total = fields.Boolean('New Patients')
    kpi_mate_patients_total_value = fields.Integer(compute='_compute_kpi_mate_patients_total_value')

    def _compute_kpi_mate_appointment_total_value(self):
        if not self.env.user.has_group('mate_hms_base.mate_group_hms_user'):
            raise AccessError(_("Do not have access, skip this data for user's digest email"))
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            appointment = self.env['mate.appointment'].search_count([('company_id', '=', company.id), ('date', '>=', start), ('date', '<', end), ('state', 'not in', ['cancel'])])
            record.kpi_mate_appointment_total_value = appointment

    def _compute_kpi_mate_treatment_total_value(self):
        if not self.env.user.has_group('mate_hms_base.mate_group_hms_user'):
            raise AccessError(_("Do not have access, skip this data for user's digest email"))
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            treatment = self.env['hms.treatment'].search_count([('company_id', '=', company.id), ('date', '>=', start), ('date', '<', end), ('state', 'not in', ['cancel'])])
            record.kpi_mate_treatment_total_value = treatment

    def _compute_kpi_mate_procedure_total_value(self):
        if not self.env.user.has_group('mate_hms_base.mate_group_hms_user'):
            raise AccessError(_("Do not have access, skip this data for user's digest email"))
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            procedure = self.env['mate_hms.patient.procedure'].search_count([('company_id', '=', company.id), ('date', '>=', start), ('date', '<', end), ('state', 'not in', ['cancel'])])
            record.kpi_mate_procedure_total_value = procedure

    def _compute_kpi_mate_evaluation_total_value(self):
        if not self.env.user.has_group('mate_hms_base.mate_group_hms_user'):
            raise AccessError(_("Do not have access, skip this data for user's digest email"))
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            evaluation = self.env['mate_hms.patient.evaluation'].search_count([('company_id', '=', company.id), ('date', '>=', start), ('date', '<', end), ('state', 'not in', ['cancel'])])
            record.kpi_mate_evaluation_total_value = evaluation

    def _compute_kpi_mate_patients_total_value(self):
        if not self.env.user.has_group('mate_hms_base.mate_group_hms_user'):
            raise AccessError(_("Do not have access, skip this data for user's digest email"))
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            patient = self.env['mate_hms.patient'].search_count([('company_id', '=', company.id), ('create_date', '>=', start), ('create_date', '<', end)])
            record.kpi_mate_patients_total_value = patient

    def _compute_kpis_actions(self, company, user):
        res = super(Digest, self)._compute_kpis_actions(company, user)
        res['kpi_mate_appointment_total'] = 'mate_hms.action_appointment&menu_id=%s' % self.env.ref('mate_hms.action_main_menu_appointmnet_opd').id
        res['kpi_mate_treatment_total'] = 'mate_hms.mate_action_form_hospital_treatment&menu_id=%s' % self.env.ref('mate_hms.main_menu_treatment').id
        res['kpi_mate_procedure_total'] = 'mate_hms.action_mate_patient_procedure&menu_id=%s' % self.env.ref('mate_hms.menu_mate_patient_procedure_treatment').id
        res['kpi_mate_evaluation_total'] = 'mate_hms.action_mate_patient_evaluation'
        res['kpi_mate_patients_total'] = 'mate_hms_base.action_patient&menu_id=%s' % self.env.ref('mate_hms_base.main_menu_patient').id
        return res