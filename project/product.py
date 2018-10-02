# -*- coding: utf-8 -*-
from odoo_csv_tools.lib import mapper
from odoo_csv_tools.lib.transform import ProductProcessorV10
from prefix import TEMPLATE_PREFIX
from config import CONNECTION_FILE


# context = {'create_product_product': True, 'tracking_disable': True}
context = {'tracking_disable': True}


def postprocess_uom_id(val):
    if val == 'kg':
        return "product.product_uom_kgm"
    return "product.product_uom_unit"


# STEP 1 : read the needed file(s)
processor = ProductProcessorV10('../data/ARTICOLI.CSV', conf_file=CONNECTION_FILE, delimiter=',')


# STEP 3 : Product Template mapping
template_map = {
    'id': mapper.m2o_map(TEMPLATE_PREFIX, mapper.val('CODICE')),
    'name': mapper.val('DESCRIZION'),
    'uom_id/id': mapper.val('UNITA_MISU', postprocess=postprocess_uom_id),
    'uom_po_id/id': mapper.val('UNITA_MISU', postprocess=postprocess_uom_id),
    'list_price': mapper.const(0)
}

processor.process(template_map, 'transformed/product.template.csv', {'worker': 4, 'batch_size': 10,
                                                                     'context': context}, 'set')


# #Step 8: Define output and import parameter
processor.write_to_file("4_product_import.sh", python_exe='', path='')


print('Product Done')
