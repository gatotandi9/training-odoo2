from odoo import api, fields, models, _ 
from odoo.exceptions import ValidationError
import time

class Session(models.Model):
    _name = "academic.session"

    name = fields.Char("Name", required=True)
    course_id = fields.Many2one(
                comodel_name="academic.course", 
                string="Course", required=True
    )
    instructor_id = fields.Many2one(
                comodel_name="res.partner",
                string="Instructor", required=True
    )
    start_date = fields.Date(
        string="Start Date", 
        required=True,
        default=lambda self: time.strftime("%Y-%m-%d"),
    )
    duration = fields.Float(
        string="Duration", 
        required=True
    )
    seats = fields.Integer(
        string="Seats", 
        required=True
    )
    active = fields.Boolean(
        string="Active", 
        default=True
    )
    
    attendee_ids = fields.One2many(
        comodel_name="academic.attendee",
        inverse_name="session_id",
        string="Attendees"
    )

    taken_seats = fields.Float(
        string="Taken Seats",
        compute="_calc_taken_seats"
    )

    image_small = fields.Binary(
        string="Image Small",
    )

    state = fields.Selection(
        string="State",
        selection=[('draft','Draft'), ('open','Open'), ('done','Done')],
        default='draft',
        required=True,
        readonly=True
    )

    def action_open(self):
        self.state = "open"
    
    def action_done(self):
        self.state = "done"
    
    def action_draft(self):
        self.state = "draft"

    @api.depends("attendee_ids", "seats")
    def _calc_taken_seats(self):
        for record in self:
            if record.seats > 0:
                record.taken_seats = 100.0 * len(record.attendee_ids) / record.seats
            else:
                record.taken_seats = 0.0

    @api.constrains("instructor_id", "attendee_ids")
    def _check_instructor_not_in_attendees(self):
        for record in self:
            if record.instructor_id and record.instructor_id in record.attendee_ids.mapped("partner_id"):
                raise ValidationError(_("A session's instructor can't be an attendee"))
            
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {}, name= ("Copied from %s") % self.name)
        return super(Session, self).copy(default=default)
