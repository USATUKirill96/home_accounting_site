import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date as currentdate
from .services import SpendsAnalyser, IncomesAnalyser
from .forms import *


@login_required
def main(request):
    if request.method == 'POST':
        period_form = PeriodForm(request.POST)
        if period_form.is_valid():
            # user changed month/year of spends
            month = period_form.cleaned_data['month']
            year = period_form.cleaned_data['year']
    else:
        # if the type of request if GET
        # initialize the forms with current data
        month = currentdate.today().month
        year = currentdate.today().year
        period_form = PeriodForm(
            initial={'year': year, 'month': month})
    # data sent to the template:
    spends = requests.get(
        f'http://localhost:8000/api/spends?user_id={request.user.pk}&source=site&&year={year}&month={month}')
    spends_json = spends.json()["Spendings"]
    by_category = SpendsAnalyser.spends_by_categories(spends_json)
    sum_of_spends = SpendsAnalyser.sum_of_spends(spends_json)
    incomes = requests.get(
        f'http://localhost:8000/api/incomes?user_id={request.user.pk}&source=site&month={month}&year={year}')
    incomes_json = incomes.json()["Incomes"]
    sum_of_incomes = IncomesAnalyser.sum_for_period(incomes_json)
    incomes_spends_difference = sum_of_incomes - sum_of_spends
    month_flag = False
    if month in range(1, 13):
        month_flag = True
    for i in range(1, 13):
        if str(i) == month:
            month_flag = True
    difference_chart_data = IncomesAnalyser.difference_chart_data(incomes_json, spends_json, month_flag)
    render_data = {'by_category': by_category, 'sum_of_spends': sum_of_spends, 'sum_of_incomes': sum_of_incomes,
                   'period_form': period_form, 'incomes_spends_difference': incomes_spends_difference,
                   'difference_chart_data': difference_chart_data}
    return render(request, 'spending_analysis/analysis.html', render_data)
