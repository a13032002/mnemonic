$(document).ready(function()
{
	$('#btn-remove').bind('click', btnRemoveFromList)
		.css({'position':'fixed', 'right': '10px', 'bottom': '0px'});
});


function btnNextVocabulary(event)
{
	index = parseInt($('#vocabulary-id').text()) + 1;
	window.location.href = index;
}

function btnPreviousVocabulary(event)
{
	index = parseInt($('#vocabulary-id').text()) - 1;
	window.location.href = index;
}

function btnRemoveFromList(event)
{
	$.ajax({url: $('#vocabulary-id').text() + '/remove',
		async: false,
		dataType: 'text',
		success: function(data){location.reload();}
	});
}
	
