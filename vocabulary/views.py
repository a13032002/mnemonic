from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from vocabulary.models import Vocabulary, Explanation, Tag, TagRelation
from vocabulary.yahoo import query_vocabulary
from django.utils.dateparse import parse_datetime

import random
# Create your views here.

def query(request, vocabulary):
	try:
		result = Vocabulary.objects.get(spell = vocabulary)
	except ObjectDoesNotExist as e:
		result = query_vocabulary(vocabulary)
	part_of_speechs = result.get_part_of_speechs()
	context = {'vocabulary' : result, 'part_of_speechs' : part_of_speechs}
	return render(request, "query.html", context)

def query_by_id(request, vocabulary_id):
	result = Vocabulary.objects.get(id = vocabulary_id)
	return  render(request, "query.html", {'vocabulary' : result, 'part_of_speechs': result.get_part_of_speechs()})

def explanation_change_order(request, explanation_id_1, explanation_id_2):
	explanation_1 = Explanation.objects.get(id = explanation_id_1)
	explanation_2 = Explanation.objects.get(id = explanation_id_2)
	explanation_1_order = explanation_1.order
	explanation_2_order = explanation_2.order

	explanation_1.order = explanation_2_order
	explanation_2.order = explanation_1_order

	explanation_1.save()
	explanation_2.save()
	return HttpResponse('')

def make_list(request, tag, time_begin, time_end):
	def filter(vocabulary, tag, time_begin, time_end):
		if tag != 'none' and len([tag for tagrelation in vocabulary.tagrelation_set.all() if tagrelation.tag.name == tag]) == 0:
			return False
		if time_begin != 'none' and vocabulary.time_inserted < parse_datetime(time_begin):
			return False
		if time_end != 'none' and vocabulary.time_end > parse_datetime(time_end):
			return False
		return True

	vocabularies = [v for v in Vocabulary.objects.all() if filter(v, tag, time_begin, time_end)]

	number_of_vocabulary = len(vocabularies)
	
	indexes = [i for i in range(number_of_vocabulary)]
	random.shuffle(indexes)

	for index, vocabulary in zip(indexes, vocabularies):
		vocabulary.display_order = index
		vocabulary.save()

	return render(request, "information.html", {'number' : len(indexes)})


def explanation_mark_important(request, explanation_id):
	explanation = Explanation.objects.get(id = explanation_id)
	explanation.mark_important = not explanation.mark_important
	explanation.save()

	return HttpResponse('')

def get_next_vocabulary(request, vocabulary_id):
	vocabulary = Vocabulary.objects.get(id = vocabulary_id)
	try:
		next_vocabulary = Vocabulary.objects.get(id = int(vocabulary_id) + 1)
	except ObjectDoesNotExist as e:
		return HttpResponse(vocabulary.spell)
	return HttpResponse(next_vocabulary.spell)

def get_previous_vocabulary(request, vocabulary_id):
	vocabulary = Vocabulary.objects.get(id = vocabulary_id)
	try:
		previous_vocabulary = Vocabulary.objects.get(id = int(vocabulary_id) - 1)
	except ObjectDoesNotExist as e:
		return HttpResponse(vocabulary.spell)
	return HttpResponse(previous_vocabulary.spell)

def add_tag(request, vocabulary_id, tag_name):
	vocabulary = Vocabulary.objects.get(id = vocabulary_id)
	tag = Tag.get_tag(tag_name)

	if len(TagRelation.objects.filter(vocabulary = vocabulary, tag = tag)) > 0:
		return HttpResponse('')
	
	tag_relation = TagRelation(vocabulary = vocabulary, tag = tag)
	tag_relation.save()
	return HttpResponse('')

def show_list(request, order):
	try:
		vocabulary = Vocabulary.objects.get(display_order = order)
	except ObjectDoesNotExist as e:
		return HttpResponse('<script>window.history.back()</script>')
	return render(request, 'show_list.html', {'vocabulary':vocabulary, 'part_of_speechs': vocabulary.get_part_of_speechs()})
