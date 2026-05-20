from odoo import fields, models, api


class HrEmployee(models.Model):
    _inherit = "hr.contract"

    extra_expense_ids = fields.One2many('hr.contract.expense.line', 'contract_id', string="Extra Expenses")
    medical_allowance = fields.Monetary(string="Medical Allowance", help="Medical allowance")
    other_allowance = fields.Monetary(string="Other Allowance", help="Other allowances")
    total_allowance = fields.Monetary(string="Total Amount", compute="_compute_total_allowance", store=True)

    @api.depends('extra_expense_ids.amount')
    def _compute_total_allowance(self):
        for record in self:
            total_expense_amount = sum(record.extra_expense_ids.mapped('amount'))
            record.total_allowance = total_expense_amount

    def print_contract_report(self):
        return self.env.ref('backend_customization.action_report_expense').report_action(self)


class HrContractExpenseLine(models.Model):
    _name = 'hr.contract.expense.line'
    _description = 'Contract Extra Expense Line'

    contract_id = fields.Many2one('hr.contract', string="Contract", ondelete='cascade')
    date = fields.Date(string="Date")
    description = fields.Char(string="Description")
    amount = fields.Float(string="Amount")



