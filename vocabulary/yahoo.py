#!/usr/bin/env python3.2
# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
from lxml import etree
import urllib

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from vocabulary.models import Vocabulary, PartOfSpeech, Explanation, SampleSentence, Tag, TagRelation

def yahoo_vocabulary_filter(string):
	if "【英】" in string :return False
	if "formal -【正式】" in string :return False
	for c in string:
		if 0x4e00 <= ord(c) and ord(c) <= 0x9fff:
			return True
	return False

def find_first_chinese_character_position(string):
	for position, c in enumerate(string):
		if 0x4e00 <= ord(c) and ord(c) <= 0x9fff:
			return position
	return -1

def query_vocabulary(query):
	yahoo_url = "http://tw.dictionary.yahoo.com/dictionary?p=%s" % (urllib.parse.quote(query))
	req = urllib.request.Request(yahoo_url)
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
	req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36')
	req.add_header('Accept-Encoding', 'html')
	req.add_header('Accept-Language','en-US,en;q=0.8,zh-TW;q=0.6')
	req.add_header('Referer', 'http://tw.dictionary.yahoo.com/')
	html = urllib.request.urlopen(req).read().decode('utf8')

	d = pq(html)
	types = d(".type-item");
	if types.size() <= 0:
		return None

	spell = d.find('div.summary h2').eq(0).text()
	others = d.find('div.disambiguate-wrapper').find('div.summary')
	kk = d.find('dd').eq(0).text()

	try:
		return Vocabulary.objects.get(spell = spell)
	except ObjectDoesNotExist as e:
		pass
	
	vocabulary = Vocabulary(spell = spell, kk = kk, time_inserted = timezone.now())
	vocabulary.save()
	
	default_tag = Tag.get_tag("gre")
	TagRelation(tag = default_tag, vocabulary = vocabulary).save()
	
	count = 0
	seen = set()
	for i in range(types.size()):
		type_description = types.eq(i).find('div.type').text()
		part_of_speech = PartOfSpeech.get_part_of_speech_by_description(type_description)
		ols = types.eq(i).find('li.exp-item')
		for j in range(ols.size()):
			meaning = ols.eq(j).find('.exp').text()
			explanation = Explanation(vocabulary = vocabulary, part_of_speech = part_of_speech, description = meaning, order = count)
			explanation.save()
			count += 1
			if ols.eq(j).find('.sample').size() > 0 :
				sample = ols.eq(j).find('.sample').text().replace("\n", "")
				pos = find_first_chinese_character_position(sample)
				sample_sentence = SampleSentence(explanation = explanation, 
									english_sentence = sample[:pos],
									chinese_sentence = sample[pos:])
				sample_sentence.save()
			seen.add(meaning)
			
	for i in range(others.size()):
		w = others.eq(i).find('h2').text()
		if w != vocabulary:continue
		meaning = others.eq(i).find('p.explanation').text()
		if not yahoo_vocabulary_filter(meaning) or meaning in seen: continue
		explanation = Explanation(description = meaning, part_of_speech = PartOfSpeech.get_part_of_speech_by_description(""), order = count)
		explanation.save()
		seen.add(meaning)
		count += 1

	return vocabulary
