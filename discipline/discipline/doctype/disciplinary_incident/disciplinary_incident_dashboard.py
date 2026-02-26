from frappe import _

def get_data():
	return {
		'fieldname': 'incident_ref',
		'non_standard_fieldnames': {
			'Disciplinary Appeal': 'disciplinary_incident',
			'Performance Improvement Plan': 'disciplinary_incident',
		},
		'transactions': [
			{
				'label': _('Investigation & Resolution'),
				'items': ['Disciplinary Investigation', 'Restorative Mediation']
			},
			{
				'label': _('Post-Decision'),
				'items': ['Disciplinary Appeal', 'Performance Improvement Plan']
			}
		]
	}
