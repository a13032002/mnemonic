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

$(document).ready(function()
		{
			$('#query-form').bind('submit', function(event)
				{
					event.preventDefault();
					text = $('#query').val();
					window.location.href = text;
					return false;
				}
				);
			$('#query-form')
				.css('bottom', '10px')
				.css('right', '10px')
				.css('position','fixed');
			}
		);
