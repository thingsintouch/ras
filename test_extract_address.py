
from common.connectivity import extract_odoo_host_and_port as extract

from common.params import Params

from common import constants as co

params = Params(db=co.PARAMS)


def test_results(odooAddress):
    print()
    params.put("odooUrlTemplate", odooAddress)
    extract()
    odooHost = params.get("odoo_host")
    odooPort = params.get("odoo_port")
    template = params.get("odooUrlTemplate")
    print(f"template: {template}   -----   odoo_host: {odooHost}   -----    odoo_port: {odooPort}")
    print("_"*110)
    print()

template_original = params.get("odooUrlTemplate")

test_results("https://example.com:443")
test_results("https://example.com:450")
test_results("https://example.com")
test_results("http://example.com")
test_results("http://example.com:8072")
test_results("example.com")
test_results("http://localhost:9135/iot/8c284667-624d-447b-b226-85e38c196ac0/action")
test_results("localhost.com/iot/8c284667-624d-447b-b226-85e38c196ac0/action")

test_results(template_original)