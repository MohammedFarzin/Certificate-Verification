from odoo import models


class CertificateCardXlsx(models.AbstractModel):
    _name = 'report.certificate.report_certificate_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet('Certificate Report')
        format1 = workbook.add_format({'font_size': 13, 'align': 'vcenter', })
        format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter'})
        sheet.set_column(0, 0, 30)
        sheet.set_column(0, 1, 30)
        sheet.write(0, 0, 'Number', format1)
        sheet.write(0, 1, lines.name, format2)
        sheet.write(1, 0, 'Name', format1)
        sheet.write(1, 1, lines.partner_id.name, format2)
        sheet.write(2, 0, 'Course', format1)
        sheet.write(2, 1, lines.order_line.product_template_id.name, format2)
        sheet.write(3, 0, 'Fees Paid', format1)
        sheet.write(3, 1, lines.order_line.fees_paid, format2)
        sheet.write(4, 0, 'Unit Price', format1)
        sheet.write(4, 1, lines.order_line.price_unit, format2)
        sheet.write(6, 0, 'Balance Fees', format1)
        sheet.write(6, 1, lines.order_line.balance_fees, format2)
