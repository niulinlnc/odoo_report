# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class PsPrintFormat(models.Model):
    _name = "ps.print.format"
    _description = "打印格式数据"

    name = fields.Char(string='格式名称', required=True)
    description = fields.Char(string='格式描述')
    model_id = fields.Many2one('ir.model', string='单据', required=True)
    is_valid = fields.Boolean('是否启用', readonly=True)
    state = fields.Selection([('draft', '草稿'), ('validate', '生效')], string='状态', required=True, readonly=True,
                             copy=False, default='draft')
    action_server_id = fields.Integer()

    @api.model
    def action_ps_print(self):
        """
        打印核心
        :return:
        """
        print(6666)
        pass

    def _set_action(self, state):
        """
        对应单据action操作
        :return:
        """
        if state == 'validate':
            """
            设置为生效时增加action
            """
            action_server = self.env['ir.actions.server'].create({
                'name': '打印',
                'activity_user_field_name': 'user_id',
                'fields_lines': [],
                'binding_type': 'action',
                'link_field_id': False,
                'template_id': False,
                'activity_date_deadline_range': 0,
                'activity_summary': False,
                'activity_note': '<p><br></p>',
                'model_id': self.model_id.id,
                'child_ids': [(6, 0, [])],
                'type': 'ir.actions.server',
                'crud_model_id': False,
                'sequence': 10,
                'activity_user_id': False,
                'state': 'code',
                'channel_ids': [(6, 0, [])],
                'binding_model_id': self.model_id.id,
                'activity_type_id': False,
                'partner_ids': [(6, 0, [])],
                'help': False,
                'activity_user_type': 'specific',
                'activity_date_deadline_range_type': 'days',
                'usage': 'ir_actions_server',
                'code': 'records.action_ps_print()'
            })
            return action_server
        if state == 'draft':
            """
            设置为草稿时删除已存在的action
            """
            self.env['ir.actions.server'].browse(self.action_server_id).unlink()
            return False

    def validate(self):
        """
        设置打印格式为启用状态
        :return:
        """
        self.state = 'validate'
        self.is_valid = True
        action_server = self._set_action(self.state)
        if action_server:
            self.action_server_id = action_server.id

    def draft(self):
        """
        设置打印格式为封存草稿状态
        :return:
        """
        self.state = 'draft'
        self.is_valid = False
        self._set_action(self.state)

