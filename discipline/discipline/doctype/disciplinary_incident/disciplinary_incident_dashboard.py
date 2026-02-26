from frappe import _

def get_data():
	return {
		'fieldname': 'incident_ref',
		'transactions': [
			{
				'label': _('Process'),
				'items': ['Disciplinary Investigation', 'Restorative Mediation']
			}
		]
	}
