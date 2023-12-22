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

## Enable RediSearch
Need to replace in yaml file the image from "redis:6.2-alpine" to "redis/redis-stack-server"

Then in webshop settings enable RediSearch and add the search fields. For example: "web_item_name,item_code,item_name,item_group"
Be aware that the alpine image is around 45Mb and the redis/redis-stack-server is around 500Mb
