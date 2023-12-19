## Theodoulou

Customizations of theodoulouparts.com
.

#### License

MIT

## Import data
* Import Item Groups
* Create Supplier Group Parts
* Import Suppliers
* Import Item
* Import Item Barcodes
* Import Item Alternatives
* When final Import Stock Entry

## How to publish all items to webshop
* ```shell
bench console
import importlib
from theodoulou.theodoulou.utils.utils import publish_all_items
from theodoulou.theodoulou.utils import utils
importlib.reload(utils)
utils.publish_all_items()
``````
