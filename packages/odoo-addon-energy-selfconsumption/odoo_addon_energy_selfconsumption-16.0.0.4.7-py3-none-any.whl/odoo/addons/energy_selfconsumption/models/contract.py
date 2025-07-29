from collections import namedtuple

from odoo import fields, models


class Contract(models.Model):
    _inherit = "contract.contract"

    supply_point_assignation_id = fields.Many2one(
        "energy_selfconsumption.supply_point_assignation",
        string="Supply point assignation",
    )
    # TODO: Move this field into energy_project module
    project_id = fields.Many2one(
        "energy_project.project",
        ondelete="restrict",
        string="Energy Project",
        related="supply_point_assignation_id.distribution_table_id.selfconsumption_project_id.project_id",
        store=True,
        auto_join=True,
    )
    code = fields.Char(related="supply_point_assignation_id.supply_point_id.code")
    supply_point_name = fields.Char(
        related="supply_point_assignation_id.supply_point_id.name"
    )
    last_period_date_start = fields.Date(
        string="Last Period Start",
        readonly=True,
    )
    last_period_date_end = fields.Date(
        string="Last Period End",
        readonly=True,
    )

    def get_main_line(self):
        self.ensure_one()
        main_line_record = self.contract_line_ids.filtered(lambda line: line.main_line)
        return main_line_record

    def invoicing_wizard_action(self):
        """
        We create the wizard first, so it triggers the constraint of the contract_ids
        :return: Window action with the wizard already created
        """
        wizard_id = self.env["energy_selfconsumption.invoicing.wizard"].create(
            {"contract_ids": [(6, 0, self.ids)]}
        )
        action = self.env.ref(
            "energy_selfconsumption.invoicing_wizard_act_window"
        ).read()[0]
        action["res_id"] = wizard_id.id
        return action

    def _recurring_create_invoice(self, date_ref=False):
        last_period_date_start = last_period_date_end = False
        if len(self) > 1:
            last_period_date_start = self[0].next_period_date_start
            last_period_date_end = self[0].next_period_date_end
        res = super()._recurring_create_invoice(date_ref=date_ref)
        if res and last_period_date_start and last_period_date_end:
            self.write(
                {
                    "last_period_date_start": last_period_date_start,
                    "last_period_date_end": last_period_date_end,
                }
            )
        return res

    def _get_contracts_to_invoice_domain(self, date_ref=None):
        domain = super()._get_contracts_to_invoice_domain(date_ref)
        domain.extend(
            [("project_id.selfconsumption_id.invoicing_mode", "!=", "energy_delivered")]
        )
        return domain

    def get_active_monitoring_members(self):
        QueryResult = namedtuple("QueryResult", ["total"])
        QUERY = """
            select count(energy_selfconsumption_supply_point.code) from energy_project_project
            inner join energy_selfconsumption_selfconsumption on
                energy_selfconsumption_selfconsumption.project_id = energy_project_project.id
            inner join energy_selfconsumption_distribution_table on
                energy_selfconsumption_distribution_table.selfconsumption_project_id = energy_selfconsumption_selfconsumption.id
            inner join energy_selfconsumption_supply_point_assignation on
                energy_selfconsumption_supply_point_assignation.distribution_table_id = energy_selfconsumption_distribution_table.id
            inner join energy_selfconsumption_supply_point on
                energy_selfconsumption_supply_point.id = energy_selfconsumption_supply_point_assignation.supply_point_id
            inner join energy_project_service_contract on
                energy_project_service_contract.project_id= energy_project_project.id
            inner join energy_project_provider on energy_project_service_contract.provider_id=energy_project_provider.id
            where
                energy_project_project.company_id={current_company_id} and
                energy_selfconsumption_distribution_table.state = 'active' and
                energy_project_provider.name LIKE '{arkenova_like}';
        """.format(
            current_company_id=int(self.community_company_id.id),
            arkenova_like="%Arkenova%",
        )
        self.env.cr.execute(QUERY)
        members = QueryResult._make(self.env.cr.fetchone())
        return members.total


class ContractRecurrencyMixin(models.AbstractModel):
    _inherit = "contract.recurrency.mixin"

    next_period_date_start = fields.Date(store=True)
    next_period_date_end = fields.Date(store=True)
