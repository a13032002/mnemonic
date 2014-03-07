from django.db import models
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.

class Vocabulary(models.Model):
	spell = models.CharField(max_length = 200, unique = True)
	kk = models.CharField(max_length = 200)
	display_order = models.IntegerField(default = -1)
	time_inserted = models.DateTimeField()
	
	def __str__(self):
		return self.spell

	def __unicode__(self):
		return self.spell

	def get_part_of_speechs(self):
		return set([explanation.part_of_speech for explanation in self.explanation_set.all()])
	

class PartOfSpeech(models.Model):
	description = models.CharField(max_length = 200, unique = True)
	
	def get_part_of_speech_by_description(description, auto_creatation = True):
		try:
			return PartOfSpeech.objects.get(description = description)
		except ObjectDoesNotExist as e:
			if not auto_creatation: raise e
			part_of_speech = PartOfSpeech(description = description)
			part_of_speech.save()
			return part_of_speech
	
class Explanation(models.Model):
	vocabulary = models.ForeignKey(Vocabulary)
	part_of_speech = models.ForeignKey(PartOfSpeech)
	description = models.CharField(max_length = 200)
	order = models.IntegerField()
	mark_important = models.BooleanField(default = False)
	class Meta:
		ordering = ['order']

class SampleSentence(models.Model):
	explanation = models.ForeignKey(Explanation)
	chinese_sentence = models.CharField(max_length = 200, null = True)
	english_sentence = models.CharField(max_length = 200)

class Tag(models.Model):
	name = models.CharField(max_length = 200)

	def get_tag(tag_name):
		try:
			return Tag.objects.get(name = tag_name)
		except ObjectDoesNotExist as e:
			tag = Tag(name = tag_name)
			tag.save()
		return tag


class TagRelation(models.Model):
	tag = models.ForeignKey(Tag)
	vocabulary = models.ForeignKey(Vocabulary)


class Question(models.Model):
	vocabulary = models.ForeignKey(Vocabulary)
	explanation = models.ForeignKey(Explanation)
	timestamp = models.IntegerField()
	delay = models.IntegerField()

