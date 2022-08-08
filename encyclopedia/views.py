from email import utils
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from django.contrib import messages
import random
from markdown2 import Markdown

from . import util

class EditForm(forms.Form):
  text = forms.CharField(label='', widget=forms.Textarea(attrs={
      "placeholder": "Enter Page Content using Github Markdown"
    }))

class SearchForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
      "class": "search",
      "placeholder": "Wiki Search"}))

class CreateForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
      "placeholder": "Page Title"}))
    text = forms.CharField(label='', widget=forms.Textarea(attrs={
      "placeholder": "Enter Page Content using Github Markdown"
    }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def go_to_publication(request, title):
    the_article_data_md = util.get_entry(title)

    if the_article_data_md:
        the_article_data_html = Markdown().convert(the_article_data_md)
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
        # othervice the form is not valid
        else:
             return render(request, "encyclopedia/search.html", {
                "title_name": title,
                "related_titles": related_titles,
                "form": form
                })
    

def create(request):

    if request.method == "POST":
        form = CreateForm(request.POST)

        if form.is_valid():
          title = form.cleaned_data['title']
          text = form.cleaned_data['text']
        else:
            messages.error(request,"something went worog, pleas check the input data")
            return render(request, "encyclopedia/create.html", {
                "form_article": form,
                "form_search": SearchForm()
                })

        if  util.get_entry(title):
            messages.error(request, 'The page with the same name exists')
            return render(request, "encyclopedia/create.html", {
              "create_form": form,
              "search_form": SearchForm(),
              "existing_page": title
            })

        util.save_entry(title, text)
        messages.success(request, f'New page "{title}" created successfully!')
        return redirect(reverse('wiki:go_to_publication', args=[title]))

    # case of get request
    return render(request, "encyclopedia/create.html", {
        "create_form": CreateForm(),
        "form": SearchForm()
        })

def edit(request, title):
    """ Lets users edit an already existing page on the wiki """

    if request.method == "POST":
        form = EditForm(request.POST)

        if form.is_valid():
          text = form.cleaned_data['text']
          util.save_entry(title, text)
          messages.success(request, f'Entry "{title}" updated successfully!')
          return redirect(reverse('wiki:go_to_publication', args=[title]))

        else:
          messages.error(request, f'Editing form not valid, please try again!')
          return render(request, "encyclopedia/edit.html", {
            "title": title,
            "edit_form": form,
            "search_form": SearchForm()
          })

    text = util.get_entry(title)

    # If title does not exist, return to index with error:
    if text == None:
        messages.error(request, f'"{title}"" page does not exist and can\'t be edited, please create a new page instead!')

    # Otherwise return pre-populated form:
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "edit_form": EditForm(initial={'text':text}),
        "search_form": SearchForm()
    })

def random_title(request):

    # Get list of titles, pick one at random:
    titles = util.list_entries()
    title = random.choice(titles)

    # Redirect to selected page:
    return redirect(reverse('wiki:go_to_publication', args=[title]))







