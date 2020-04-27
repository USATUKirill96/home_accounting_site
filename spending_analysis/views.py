import requests
from django.shortcuts import render
from .services import Analyser



def main(request):
    spends = requests.get(
        f'http://localhost:8000/api/spends?user_id={request.user.pk}&source=site&&year=2020')
    spends_json = spends.json()["Spendings"]
    by_category = Analyser.spends_by_categories(spends_json)
    return render(request, 'spending_analysis/analysis.html', {'by_category': by_category})