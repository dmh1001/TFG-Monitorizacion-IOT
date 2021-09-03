from datetime import datetime
from elasticsearch import Elasticsearch


class Extractor:

    def extraer_data(idSensor, fecha_inicio, fecha_final, campo):

        elastic_client = Elasticsearch()

        result = elastic_client.search(
            index='sensor_data-*',
                    body=
                {
                    "sort" :
                    {
                      "datetime": {"order" : "asc"}
                    },
                       "query":
                        {
                          "bool":
                            {
                                "filter":
                                {
                                    "exists":{
                                        "field":campo.value
                                    }
                                },

                                "must":
                                [
                                    {
                                        "match":
                                        {
                                            "sensorId":idSensor
                                        }
                                    },
                                    {
                                        "range":
                                        {
                                             "datetime" :
                                              {
                                               "gt" : fecha_inicio,
                                               "lte" : fecha_final
                                              }
                                        }
                                    }
                                ]
                            }
                        }
                    },
            size=9999)
        elastic_docs = result["hits"]["hits"]
        data = {}


        for num, doc in enumerate(elastic_docs):

            try:

                value = doc["_source"][campo]

                dateId = datetime.strptime(doc["_source"]["datetime"], '%d/%m/%Y %H:%M:%S')
                dateId = dateId.strftime('%Y-%m-%d %H:%M:00')
                dateId = datetime.strptime(dateId, '%Y-%m-%d %H:%M:00')

                data[dateId] = value

            except:
                    pass


        return data


