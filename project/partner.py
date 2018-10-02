# -*- coding: utf-8 -*-
from odoo_csv_tools.lib import mapper
from odoo_csv_tools.lib.transform import Processor
from datetime import datetime
from prefix import PARTNER_PREFIX, PARTNER_CATEGORY_PREFIX


def postprocess_country_id(val):
    if val:
        if val == 'GB':
            val = 'uk'
        return "base.{}".format(val.lower())
    return val


def postprocess_country_state_id(val):
    if val and val not in ('EE', 'TL'):
        if val == 'CU':
            val = 'CN'
        return 'base.state_it_{}'.format(val.lower())
    return ''


def postprocess_lang(val):
    return "Italian / Italiano"


def postprocess_vat(val):
    if val:
        if len(val) == 11 and val.isdigit():
            return 'IT{}'.format(val)
        if val[:2] == 'IT':
            if len(val) == 13 and val[:3].isdigit():
                return val.upper()
        if val[:2] in ('GB', 'EE', 'LT'):
            return val
    return ''


# STEP 1 : read the needed file(s)
processor = Processor('../data/NOMIN.CSV', delimiter=",")


# STEP 2 : Define the mapping for every object to import
mapping = {
    'id': mapper.m2o_map(PARTNER_PREFIX, mapper.val('CODICE')),
    'name': mapper.val('DESCRIZION', skip=True),
    'street': mapper.val('INDIRIZZO'),
    'city': mapper.val('COMUNE'),
    'zip': mapper.val('CAP'),
    'country_id/id': mapper.val('PAESE', postprocess=postprocess_country_id),
    'state_id/id': mapper.val('PROVINCIA', postprocess=postprocess_country_state_id),
    'vat': mapper.val('PARTITA_IV', postprocess=postprocess_vat),
    'phone': mapper.val('TELEFONO1'),
    'email': mapper.val('E_MAIL'),

    # OTHER
    'lang': mapper.val('PAESE', postprocess=postprocess_lang),
    'customer': mapper.const('1'),
    'supplier': mapper.const('1'),

}


# Contatti ulteriori
# 'TELEFONO2'
# 'RIFERIMEN2'
# 'TELEFONO3'
# 'RIFERIMEN3'
# 'NUMERO_FAX'
# 'RIFERIMEN4'
def postprocess_riferimento2(val):
    return '{}_RIF2'.format(val)


def postprocess_riferimento3(val):
    return '{}_RIF3'.format(val)


def postprocess_riferimento4(val):
    return '{}_RIF4'.format(val)


def postprocess_riferimento5(val):
    return '{}_RIF5'.format(val)


mapping2 = {
    'id': mapper.m2o_map(PARTNER_PREFIX, mapper.val('CODICE', postprocess=postprocess_riferimento2)),
    'parent_id/id': mapper.m2o_map(PARTNER_PREFIX, mapper.val('CODICE')),
    'name': mapper.val('RIFERIMEN2', default='Contatto'),
    'phone': mapper.val('TELEFONO2', skip=True),
    'type': mapper.const('contact'),
}

mapping3 = {
    'id': mapper.m2o_map(PARTNER_PREFIX, mapper.val('CODICE', postprocess=postprocess_riferimento3)),
    'parent_id/id': mapper.m2o_map(PARTNER_PREFIX, mapper.val('CODICE')),
    'name': mapper.val('RIFERIMEN3', default='Contatto'),
    'phone': mapper.val('TELEFONO3', skip=True),
    'type': mapper.const('contact'),
}

mapping4 = {
    'id': mapper.m2o_map(PARTNER_PREFIX, mapper.val('CODICE', postprocess=postprocess_riferimento4)),
    'parent_id/id': mapper.m2o_map(PARTNER_PREFIX, mapper.val('CODICE')),
    'name': mapper.val('RIFERIMEN4', default='Fax'),
    'phone': mapper.val('NUMERO_FAX', skip=True),
    'type': mapper.const('contact'),
}
mapping5 = {
    'id': mapper.m2o_map(PARTNER_PREFIX, mapper.val('CODICE', postprocess=postprocess_riferimento5)),
    'parent_id/id': mapper.m2o_map(PARTNER_PREFIX, mapper.val('CODICE')),
    'name': mapper.val('RIFERIMEN5', default='Fax'),
    'phone': mapper.val('NUMERO_FA2', skip=True),
    'type': mapper.const('contact'),
}

# Condizioni pagamento
# 'CODICE_PAG'
# 'DESCRIZIO3'

# Banca di appoggo
# 'DESCRIZIO5'
# 'ABI_VOSTRA'
# 'CAB_VOSTRA'
# 'CONTO_VOST'
# 'CIN'
# 'CIN_ESTERO'
# 'IBAN'

# Listini
# 'LISTINO_DO' (0 o 1)

# Step 4: Process data
processor.process(mapping, 'transformed/res.partner.csv', {'worker': 2, 'batch_size': 20})
processor.process(mapping2, 'transformed/res.partner.cs2', {'worker': 2, 'batch_size': 20})
processor.process(mapping3, 'transformed/res.partner.cs3', {'worker': 2, 'batch_size': 20})
processor.process(mapping4, 'transformed/res.partner.cs4', {'worker': 2, 'batch_size': 20})
processor.process(mapping5, 'transformed/res.partner.cs5', {'worker': 2, 'batch_size': 20})

# Step 5: Define output and import parameter
processor.write_to_file("1_partner.sh", python_exe='', path='')

print('Partner Done')
