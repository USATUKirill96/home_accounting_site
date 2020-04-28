
class Analyser:
    def spends_by_categories(json):
        result = {}
        for object in json:
            try:
                result[str(object['category']).lower()] += object['sum']
            except:
                result[str(object['category']).lower()] = object['sum']
        pairs_by_categories = []
        for object in result:
            pairs_by_categories.append([object, result[object]])
        print(pairs_by_categories)
        return pairs_by_categories