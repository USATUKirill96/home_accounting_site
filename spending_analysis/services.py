
class Analyser:
    def spends_by_categories(json):
        result = {}
        for object in json:
            try:
                result[object['category']] += object['sum']
            except:
                result[object['category']] = object['sum']
        return result

