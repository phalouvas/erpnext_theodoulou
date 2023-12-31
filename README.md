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

## How to import TecDoc database
* Unzip file SQL-CONVERTED.7z to folder SQL-CONVERTED
* Copy the TecDoc files "CommonSQL_Queries_24.TXT  CreateTablesTAF24.sql  IMPORT-ON-MYSQL-SERVER.sh  SQL-CONVERTED" to the server frappe-bench/sites/assets/tecdoc
*
* ```shell
bench db-console
source /workspace/development/v15/tecdoc/CreateTablesTAF24.sql
```
* In db console run the commands in file “CommonSQL_Queries_24.TXT”
* To import data
* ```shell
PATH_TO_SQL_FILES="/path_to_folder_with_sql_files/"
for sql_file in $PATH_TO_SQL_FILES*.sql ; do echo $sql_file; bench mariadb < $sql_file ; done
```
