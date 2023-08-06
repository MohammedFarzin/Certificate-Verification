from odoo import api, models, fields, _
from odoo.odoo.exceptions import UserError


class StudentCertificate(models.Model):
    # _name = 'student.certificate'
    _inherit = 'sale.order'
    _description = 'student ceritficate verification'

    partner_id = fields.Many2one('res.partner', string='Student')
    user_id = fields.Many2one('res.users', string='Administrator')
    amount_total = fields.Monetary(string='Fees')
    phone = fields.Char(related='partner_id.phone', string='Phone', readonly=True)
    full_address = fields.Char(string='Full Address', compute='_compute_full_address', store=True)
    fees_paid_ids = fields.One2many('sale.order.line', 'order_id', string='Fees Paid')
    total_fees_paid = fields.Monetary(string='Total Fees Paid', compute='_compute_total_fees_paid', store=True)
    state = fields.Selection(selection_add=[
        ('draft', 'Pending'),
        ('sent', 'Sent For Approval'),
        ('sale', 'Completed'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft')

    @api.depends('partner_id.street', 'partner_id.street2', 'partner_id.city')
    def _compute_full_address(self):
        for order in self:
            address_parts = []
            if order.partner_id.street:
                address_parts.append(order.partner_id.street)
            if order.partner_id.street2:
                address_parts.append(order.partner_id.street2)
            if order.partner_id.city:
                address_parts.append(order.partner_id.city)
            order.full_address = ', '.join(address_parts)

    def action_confirm(self):
        if self.order_line.fees_paid == self.order_line.price_unit:
            return super(StudentCertificate, self).action_confirm()
        else:
            raise UserError("Please ensure that you have paid the full fees before confirming the order.")

    def _compute_total_fees_paid(self):
        for order in self:
            order.total_fees_paid = sum(order.mapped('fees_paid_ids.fees_paid'))

    def print_report(self):
        return self.env.ref('certificate.report_certificate_card').report_action(self)



class StudentCertificationCourse(models.Model):
    _inherit = "sale.order.line"

    product_template_id = fields.Many2one('product.template', string="Course")
    product_uom_qty = fields.Float(default=1.0, readonly=False)
    fees_paid = fields.Float(string='Fees Paid')
    price_unit = fields.Float(string='Fees')
    balance_fees = fields.Monetary(string='Balance', compute='_compute_fees', store=True)
    price_subtotal = fields.Monetary(default=0)
    fully_paid = fields.Boolean(compute='_compute_fully_paid', default=False)

    # # price_tax = fields.Float(string='Tax Amount', compute='_compute_tax_fees', store=True)
    #
    @api.depends('fees_paid', 'price_unit')
    def _compute_fees(self):
        for record in self:
            record.balance_fees = (record.price_unit - record.fees_paid)
