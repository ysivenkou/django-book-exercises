from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy        # Deprecated
from django.urls import reverse
from django.template.loader import get_template

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic.dates import ArchiveIndexView, DateDetailView
from django.db.models import Q
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



from .models import Bb, Rubric

from .forms import BbForm

@login_required
def rubrics(request):
    RubricFormSet = modelformset_factory(Rubric, fields=('name', ), can_delete=True,) #can_order=True)
    if request.method == 'POST':
        formset = RubricFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('index')
    else:
        formset = RubricFormSet()
    context = {'formset': formset}
    return render(request, 'bboard/rubrics.html', context)


def index(request):
    # bbs = Bb.objects.order_by('-published')
    bbs = Bb.objects.all()
    # print(request.get_host(), request.get_port())
    # print(request.build_absolute_uri())
    # print(request.headers['accept_encoding'])
    # print(request.is_secure())
    rubrics = Rubric.objects.all()
    context = {
        'bbs': bbs,
        'rubrics': rubrics,
    }
    template = get_template('bboard/index.html')
    # return render(request, 'bboard/index.html', context)
    return HttpResponse(template.render(
        context=context,
        request=request,
    ))

def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {
        'bbs': bbs,
        'rubrics': rubrics,
        'current_rubric': current_rubric,
    }
    return render(request, 'bboard/by_rubric.html', context)


class BbIndexView(ArchiveIndexView):
    model = Bb
    date_field = 'published'
    date_list_period = 'year'
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('bboard:index') # '/bboard/' # reverse('index')
    # success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


# class BbByRubricView(TemplateView):
#     template_name = 'bboard/by_rubric.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['bbs'] = Bb.objects.filter(Q(rubric=context['rubric_id']))
#         context['rubrics'] = Rubric.objects.all()
#         context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
#         return context


class BbByRubricView(ListView):
    template_name = 'bboard/by_rubric.html' # default value: 'bboard/bb_list.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        result = Bb.objects.filter(Q(rubric=self.kwargs['rubric_id']))
        return Bb.objects.filter(Q(rubric=self.kwargs['rubric_id']))

    def get_context_data(self, **kwargs):
        # print(self.kwargs)
        # print(self.kwargs['rubric_id'])
        # print(self.context_object_name)
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(Q(pk=self.kwargs['rubric_id']))
        return context



# class BbDetailView(DetailView):
#     model = Bb

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubrics'] = Rubric.objects.all()
#         return context


class BbDetailView(DateDetailView):
    model = Bb
    date_field = 'published'
    month_format = '%m'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbAddView(FormView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    initial = {'price': 0.0}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('bboard/by_rubric.html', kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})


class BbEditView(LoginRequiredMixin, UpdateView):
    model = Bb
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbDeleteView(DeleteView):
    model = Bb
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context