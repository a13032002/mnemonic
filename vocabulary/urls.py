from django.conf.urls import patterns, include, url
from vocabulary import views

urlpatterns = patterns('',
	url(r'^(?P<vocabulary>[A-Za-z ]+)$', views.query),
	url(r'^explanation/change-order/(?P<explanation_id_1>\d+)/(?P<explanation_id_2>\d+)$', views.explanation_change_order),
	url(r'^explanation/mark-important/(?P<explanation_id>\d+)$', views.explanation_mark_important),
	url(r'^list/explanation/change-order/(?P<explanation_id_1>\d+)/(?P<explanation_id_2>\d+)$', views.explanation_change_order),
	url(r'^list/explanation/mark-important/(?P<explanation_id>\d+)$', views.explanation_mark_important),
	url(r'^make-list/(?P<tag>[A-Za-z]+)/(?P<time_begin>[a-z0-9: -]+)/(?P<time_end>[a-z0-9: -]+)$', views.make_list),
	url(r'^(?P<vocabulary_id>\d+)/next$', views.get_next_vocabulary),
	url(r'^(?P<vocabulary_id>\d+)/previous$', views.get_previous_vocabulary),
	url(r'^(?P<vocabulary_id>\d+)/tag/add/(?P<tag_name>[a-zA-Z]+)$', views.add_tag),
	url(r'^list/(?P<index>\d+)/tag/add/(?P<tag_name>[a-zA-Z]+)$', views.add_tag_list),
	url(r'^list/(?P<index>[-]{0,1}\d+)$', views.show_list),
	url(r'^list/(?P<index>[-]{0,1}\d+)/remove$', views.remove_from_list),
	url(r'^test/initialize_test$', views.initialize_test),
	url(r'^test/test$', views.test),
	url(r'^test/update/(?P<question_id>\d+)/(?P<is_correct>[01])$', views.update_question_state),
)
