from email import utils
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse

from . import util

class SearchForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
      "class": "search",
      "placeholder": "Wiki Search"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def go_to_publication(request, title):
    the_article_data_md = util.get_entry(title)

    if the_article_data_md:
        the_article_data_html = the_article_data_md
        return render(request, "encyclopedia/publication.html", {
            "the_article_data": the_article_data_html,
            "title_name": title,
            "form": SearchForm()
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title_name": title,
            "entries": util.list_entries(),
             "form": SearchForm()
        })

def search(request):
    # If search page reached by submitting search form:
    if request.method == "POST":
        form = SearchForm(request.POST)

        # If form is valid try to search for title:
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry_md = util.get_entry(title)

            print('search request: ', title)

            if entry_md:
                # If entry exists, redirect to entry view
                return redirect(reverse('wiki:go_to_publication', args=[title]))
            else:
                # Otherwise display relevant search results
                related_titles = util.related_titles(title)

                return render(request, "encyclopedia/search.html", {
                "title_name": title,
                "related_titles": related_titles,
                "form": SearchForm()
                })

    # Otherwise form not posted or form not valid, return to index page:
    return redirect(reverse('wiki:index'))






