function btnNextVocabulary(event)
{
	vocabulary_id = $('#vocabulary-id').text()
	$.ajax({
		url:vocabulary_id + '/next',
		async: false,
		dataType: 'text',
		success:function(data){window.location.href = data;}
	});
}

function btnPreviousVocabulary(event)
{
	vocabulary_id = $('#vocabulary-id').text()
	$.ajax({
		url:vocabulary_id + '/previous',
		async: false,
		dataType: 'text',
		success:function(data){window.location.href = data;}
	});
}
