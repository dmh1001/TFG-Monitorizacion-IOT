from datetime import datetime
from elasticsearch import Elasticsearch

class extractorData:

    def extractData(idSensor, fechaInicio, fechaFinal):

        elastic_client = Elasticsearch()
        result = elastic_client.search(index='sensor_data-*', body={"query": {"bool": {"must": [{ "match": { "sensorId":idSensor } },{ "range": {"datetime" : { "gt" : fechaInicio,"lte" : fechaFinal}}}]}}}, size=99)

        elastic_docs = result["hits"]["hits"]

        data = {}
        for num, doc in enumerate(elastic_docs):

            value = doc["_source"]["Valor"]
            dateId = datetime.strptime(doc["_source"]["datetime"], '%d/%m/%Y  %H:%M:%S')

            data[dateId] = value


        return sorted(data.items())

