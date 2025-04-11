from odoo import api, fields, models, _

class Course(models.Model):
    _name = "academic.course"

    name = fields.Char("Name" , required=True) 
    description = fields.Text(string="Description", required=True)
    responsible_id = fields.Many2one(
        comodel_name="res.users", 
        string="Responsible"
    )

    session_ids = fields.One2many(
        comodel_name="academic.session",
        inverse_name="course_id",
        string="Sessions",   
        ondelete="cascade",
    )

    _sql_constraints = [
        (
           'check_name_unique',
           'UNIQUE(name)',
            'The course name must be unique!'     
        ),

        (
            'check_name_description',
            'CHECK(name <> description)',
            'The course name and description must not be same!'
        ),
    ]
