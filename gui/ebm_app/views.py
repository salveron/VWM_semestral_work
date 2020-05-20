import time

from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import QueryForm
from query_parser.parser import QueryParser
from utils import InvalidQueryException, InvalidTokenException


def home(request):
    if request.method == "POST":
        form = QueryForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data.get("query")

            try:
                if "sequential_search" in request.POST:
                    start_point = time.time()
                    result = QueryParser(query, sequential=True).start()
                else:
                    start_point = time.time()
                    result = QueryParser(query).start()

                result.sort(key=lambda x: x[1], reverse=True)

            except InvalidQueryException as ex:
                messages.error(request, *ex.args)
                return redirect("ebm_home")

            except InvalidTokenException as ex:
                messages.error(request, *ex.args)
                return redirect("ebm_home")

            end_point = time.time()
            return render(request, "ebm_app/home.html", {"form": form,
                                                         "result": result,
                                                         "time": round(end_point - start_point, 2)})
        else:
            print(form.errors())
    else:
        form = QueryForm()
    return render(request, "ebm_app/home.html", {"form": form, "result": {}})
