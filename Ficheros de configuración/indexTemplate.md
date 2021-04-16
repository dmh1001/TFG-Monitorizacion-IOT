```shell
POST _template/sensor_data_template
{
  "index_patterns": [
    "sensor_data*"
  ],
  "settings": {
    "number_of_replicas": "1",
    "number_of_shards": "5"
  },
  "mappings": {
    "properties": {
      "sensorId": {
        "type": "integer"
      },
      "datetime":{
        "type": "date",
        "format": "dd/MM/yyyy HH:mm:ss"
      },
      "reading": {
        "type": "nested", 
        "properties": { 
          "name": {"type":"keyword"},
          "description": {"type":"double"}
        }
      }
    }
  }
}
```
