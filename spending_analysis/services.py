from datetime import datetime

class SpendsAnalyser:
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
        # print(pairs_by_categories)
        return pairs_by_categories

    def sum_of_spends(json):
        sum = 0
        for object in json:
            sum += object['sum']
        return sum


class IncomesAnalyser:
    def sum_for_period(json):
        sum_of_incomes = 0
        for object in json:
            sum_of_incomes += object['sum']
        return sum_of_incomes

    def incomes_spends_difference(json):
        return IncomesAnalyser.sum_for_period(json) - SpendsAnalyser.sum_of_spends(json)

    def difference_chart_data(incomes, spends, month_flag):

        def create_formated_list(objects, month_flag):
            """for json object creates pair date-sum. date field contains month or day depending the observed scale"""
            formated_list = []
            for object in objects:
                if month_flag: #if you sort objects within a month, it groups by days
                    formated_data = [datetime.strptime(object['date'], "%d-%m-%Y").day, int(object['sum'])]
                else: #if you sort objects within a year, it groups by moth
                    formated_data = [datetime.strptime(object['date'], "%d-%m-%Y").month, int(object['sum'])]
                formated_list.append(formated_data)
                formated_list.sort() #sort pairs month-sum by month
                for object in formated_list:
                    # if two operations made in one time period, its sums will sum (lol) and one object is removed
                    if object[0] < 0:
                        formated_list.remove(object)
                    for subject in formated_list:
                        if object is subject:
                            continue
                        if object[0] == subject[0]:
                            object[1] += subject[1]
                            subject[0] = -1
            return formated_list

        def unite_lists(spends, incomes):
            # unites two lists of spends and incomes into one list [date, spend, income]
            sp_counter = 0
            inc_counter = 0
            united_list = []
            while sp_counter < len(spends) or inc_counter < len(incomes): # while we have objects to sort
                if inc_counter < len(incomes):
                    if sp_counter < len(spends):
                        if spends[sp_counter][0] < incomes[inc_counter][0]:
                            united_list.append([spends[sp_counter][0], spends[sp_counter][1], 0])
                            sp_counter += 1
                        elif spends[sp_counter][0] == incomes[inc_counter][0]:
                            united_list.append([spends[sp_counter][0], spends[sp_counter][1], incomes[inc_counter][1]])
                            sp_counter += 1
                            inc_counter += 1
                        elif spends[sp_counter][0] > incomes[inc_counter][0]:
                            united_list.append([incomes[inc_counter][0], 0, incomes[inc_counter][1]])
                            inc_counter += 1
                        else:
                            raise Exception("Error during sort operation. services, 68")
                    else:
                        united_list.append([incomes[inc_counter][0], 0, incomes[inc_counter][1]])
                        inc_counter += 1
                else:
                    if sp_counter < len(spends):
                        united_list.append([spends[sp_counter][0], spends[sp_counter][1], 0])
                        sp_counter += 1
            return united_list

        spends_date_sum = create_formated_list(spends, month_flag)
        incomes_date_sum = create_formated_list(incomes, month_flag)
        united_list = unite_lists(spends_date_sum, incomes_date_sum)
        for i in range(1, len(united_list)):
            united_list[i][1] += united_list[i-1][1]
            united_list[i][2] += united_list[i-1][2]
        return united_list
