# -*- coding: utf-8 -*-
import os
from odoo_csv_tools.lib import mapper
from odoo_csv_tools.lib.transform import Processor
from datetime import datetime
from prefix import CLIENT_PREFIX, PARTNER_CATEGORY_PREFIX


def data_dir(filename):
    return os.path.join('..', 'data', filename)


def transform_dir(filename):
    return os.path.join('transformed', filename)


def postprocess_country_id(val):
    if val:
        if val == 'GB':
            val = 'uk'
        return "base.{}".format(val.lower())
    return val


def postprocess_lang(val):
    # if val == 'IT' or not val:
    #     return "Italian / Italiano"
    return "English"


# STEP 1 : read the needed file(s)
processor = Processor(data_dir('NOMIN.CSV'), delimiter=",")

# STEP 2 : Define the mapping for every object to import
mapping = {
    'id': mapper.m2o_map(CLIENT_PREFIX, mapper.val('CODICE')),
    'name': mapper.val('DESCRIZION', skip=True),
    'phone': mapper.val('TELEFONO1'),
    # 'fax': mapper.val('NUMERO_FAX'),
    'street': mapper.val('INDIRIZZO'),
    'city': mapper.val('COMUNE'),
    'zip': mapper.val('CAP'),
    'country_id/id': mapper.val('PAESE', postprocess=postprocess_country_id),
    'lang': mapper.val('PAESE', postprocess=postprocess_lang),
    'customer': mapper.const('1'),
    'supplier': mapper.const('1'),
    # 'lang': mapper.val('Language', lang_map),
    # 'image': mapper.binary("Image", "origin/img/"),
    # 'create_uid': mapper.val('Create BY'),
    # 'create_date': mapper.val('Create ON',
    #    postprocess=lambda x: datetime.strptime(x, "%d/%m/%y").strftime("%Y-%m-%d 00:00:00")),
    # 'category_id/id': mapper.m2m(PARTNER_CATEGORY_PREFIX, 'Tag', 'Fidelity Grade'),
}

# tag_mapping = {
#     'id': mapper.m2m_id_list(PARTNER_CATEGORY_PREFIX, 'Tag'),
#     'name': mapper.m2m_value_list('Tag'),
# }

# grade_mapping = {
#     'id': mapper.m2m_id_list(PARTNER_CATEGORY_PREFIX, 'Fidelity Grade'),
#     'name': mapper.m2m_value_list('Fidelity Grade'),
# }

# Step 4: Process data
# processor.process(tag_mapping, transform_dir('res.partner.category.csv'), {}, m2m=True)
# processor.process(grade_mapping, transform_dir('res.partner.category.grade.csv'), {'model': 'res.partner.category'}, m2m=True)
# processor.process(mapping, transform_dir('res.partner.csv'), {'worker': 2, 'batch_size': 20, 'context': {'write_metadata': True}})
processor.process(mapping, transform_dir('res.partner.csv'), {'worker': 2, 'batch_size': 20})

# Step 5: Define output and import parameter
processor.write_to_file("1_client.sh", python_exe='', path='')

print('Client Done')
