from frappe import _

def get_data():
	return {
		'fieldname': 'offence',
		'transactions': [
			{
				'label': _('Incidents'),
				'items': ['Disciplinary Incident']
			}
		]
	}
