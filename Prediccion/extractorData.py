from datetime import datetime
from elasticsearch import Elasticsearch

import numpy as np
import pandas
from river import stream

class extractorData:

    def extractData(idSensor, fechaInicio, fechaFinal):

        elastic_client = Elasticsearch()
        result = elastic_client.search(index='sensor_data-*', body={"query": {"bool": {"must": [{ "match": { "sensorId":idSensor } },{ "range": {"datetime" : { "gt" : fechaInicio,"lte" : fechaFinal}}}]}}}, size=99)

        elastic_docs = result["hits"]["hits"]

        docs = pandas.DataFrame()
        #docs = {}
        #doc_data = {}
        for num, doc in enumerate(elastic_docs):
            source_data = doc["_source"]["Valor"]

            _id = doc["_source"]["datetime"]

            doc_data = pandas.Series(source_data, name = _id)
            docs = docs.append(doc_data)
            print(docs)

        return stream.iter_pandas(docs)
