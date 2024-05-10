from women.models import Category, Women
from django.db.models import Count
from django.http import Http404
from django.views.generic.detail import SingleObjectMixin

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]



class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        # cats = Category.objects.all()
        cats = Category.objects.annotate(Count('women'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        # context['menu'] = menu
        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context


class MyMixin(SingleObjectMixin):
    model = Women
    context_object_name = 'Pizza'
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        slug = self.kwargs.get('post_slug')
        obj = queryset.filter(slug=slug).first()
        obj.title = f'{obj.title}-томат'
        if obj is None:
            raise Http404("Запись не найдена")
        return obj