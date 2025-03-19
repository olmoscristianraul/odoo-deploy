"""
Este módulo define el modelo MyModel.
Un modelo de ejemplo.
"""

from odoo import models, fields


    class MyModel(models.Model):
    """
    Esta clase representa mi modelo personalizado.
    """

    _name = 'my.model'
    _description = 'My Model'

    name = fields.Char(string='Nombre')