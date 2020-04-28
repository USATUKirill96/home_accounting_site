import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date as currentdate
from .services import Analyser
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

    spends = requests.get(
        f'http://localhost:8000/api/spends?user_id={request.user.pk}&source=site&&year={year}&month={month}')
    spends_json = spends.json()["Spendings"]
    by_category = Analyser.spends_by_categories(spends_json)
    return render(request, 'spending_analysis/analysis.html', {'by_category': by_category, 'period_form': period_form})
