from django.urls import path
from .views import index, by_rubric, BbCreateView, BbByRubricView, BbDetailView, BbEditView, BbDeleteView, BbIndexView, rubrics

# app_name = 'bboard'
# После объявления app_name имя маршрута для вызова будет указываться в формате app_name:name
# Таким же образом нужно ссылкаться для вызова контроллера по url, приложению в include указывается псевдоним (namespace), т.е. namespace:name

app_name = 'bboard'
urlpatterns = [
    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'), # by_rubric
    path('', BbIndexView.as_view(), name='index'),
    path('add/', BbCreateView.as_view(), name='add'),
    # path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('detail/<int:year>/<int:month>/<int:day>/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('edit/<int:pk>/', BbEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
    path('rubrics/', rubrics, name='rubrics')
]