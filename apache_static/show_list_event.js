
function btnNextVocabulary(event)
{
	vocabulary_order = parseInt($('#vocabulary-id').text()) + 1;
	window.location.href = vocabulary_order;
}

function btnPreviousVocabulary(event)
{
	vocabulary_order = parseInt($('#vocabulary-id').text()) - 1;
	window.location.href = vocabulary_order;
}
