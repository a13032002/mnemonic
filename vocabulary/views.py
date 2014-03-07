from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from vocabulary.models import Vocabulary, Explanation, Tag, TagRelation, Question
from vocabulary.yahoo import query_vocabulary
from django.utils.dateparse import parse_datetime

import random, pytz
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
		if time_begin is not None and vocabulary.time_inserted < time_begin:
			return False
		if time_end is not None and vocabulary.time_inserted > time_end :
			return False
		return True

	_time_begin = None if time_begin == 'none' else pytz.timezone("Asia/Taipei").localize(parse_datetime(time_begin), is_dst=False)
	_time_end = None if time_end == 'none' else pytz.timezone("Asia/Taipei").localize(parse_datetime(time_end), is_dst=False)
	vocabularies = [v for v in Vocabulary.objects.all() if filter(v, tag, _time_begin, _time_end)]

	number_of_vocabulary = len(vocabularies)
	
	indexes = [i for i in range(number_of_vocabulary)]
	random.shuffle(indexes)

	for index, vocabulary in zip(indexes, vocabularies):
		vocabulary.display_order = index
		vocabulary.save()

	return render(request, "information.html", {'text' : 'The display order of  %d vocabularies has been shuffled' % len(indexes)})


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

def initialize_test(request):
	for vocabulary in Vocabulary.objects.all():
		for explanation in vocabulary.explanation_set.all():
			question = Question(vocabulary = vocabulary, explanation = explanation, timestamp = 0, delay = 10)
			question.save()
	
	return render(request, "information.html", {'text' : 'Questions has been initialized!'})

def test(request):
	questions = Question.objects.order_by('timestamp')
	vocabulary = random.choice(questions).vocabulary
	choices = [{'id': question.id, 'answer': question.vocabulary.spell, 'description': question.explanation.description, 'is_answer': True} for question in questions.filter(vocabulary = vocabulary)[0:1]]
	number_of_correct_choices = len(choices)
	choices += [{'id': question.id, 'answer':question.vocabulary.spell, 'description': question.explanation.description, 'is_answer': False} for question in questions.exclude(vocabulary = vocabulary)[0:3]]
	random.shuffle(choices)
	return render(request, 'test.html', {'choices': choices, 'vocabulary': vocabulary, 'number_of_correct_choices': number_of_correct_choices})
	
def update_question_state(request, question_id, is_correct):
	target_question = Question.objects.get(id = question_id)
	if is_correct == "1":
		target_question.delay = max(target_question.delay / 10, 1)
	else:
		target_question.delay = min(target_question.delay * 10, 10000)

	target_question.timestamp += target_question.delay
	target_question.save()
	return HttpResponse('')

