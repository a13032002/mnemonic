$(document).ready(
	function()
	{
		$('[name="btn-up"]').bind('click', btnUpClick);
		$('[name="btn-down"]').bind('click', btnDownClick);
		$('[name="btn-mark-important"]').bind('click', btnMarkImportantClick);
		$('#btn-prev')
			.css({'position':'fixed', 'left':'10px', 'top': ($(window).height() / 2 - $('#btn-prev').height() / 2) + 'px'})
			.bind('click', btnPreviousVocabulary)
			;
		$('#btn-next')
			.css({'position':'fixed', 'left':($(window).width() - 100 - $('#btn-next').width()) + 'px', 'top': ($(window).height() / 2 - $('#btn-next').height() / 2) + 'px'})
			.bind('click', btnNextVocabulary)
			;
		$('#tag-form').bind('submit', formTagSubmit);
	});

function formTagSubmit(event)
{
	event.preventDefault();
	vocabulary_id = $('#vocabulary-id').text();
	tag = $('#tag').val();
	$.ajax({url : vocabulary_id + '/tag/add/' + tag,
		dataType: 'text',
		async: 'false',
		success: function(data){//document.location.reload();
		}
	});
	return false;
}

function btnMarkImportantClick(event)
{
	explanation = $(event.target).parents('.explanation');
	explanation_id = explanation.attr('explanation-id');
	$.ajax({
		url:'explanation/mark-important/' + explanation_id,
		async:false,
		success:function(data){explanation.children('span.description').toggleClass('important');}
		});
}

function btnUpClick(event)
{
	current_explanation = $(event.target).parents('.explanation');
	previous_explanation = current_explanation.prev();
	if (previous_explanation.size() == 0)
		return ;
	current_explanation_id = current_explanation.attr('explanation-id');
	previous_explanation_id = previous_explanation.attr('explanation-id');

	$.ajax({
		url:'explanation/change-order/' + current_explanation_id + '/' + previous_explanation_id,
		async:false,
		success:function(data){ current_explanation.insertBefore(previous_explanation);}
	});
}

function btnDownClick(event)
{
	current_explanation = $(event.target).parents('.explanation');
	next_explanation = current_explanation.next();
	if (next_explanation.size() == 0)
		return ;

	current_explanation_id = current_explanation.attr('explanation-id');
	next_explanation_id = next_explanation.attr('explanation-id');
	$.ajax({
		url:'explanation/change-order/' + current_explanation_id + '/' + next_explanation_id,
		async:false,
		success:function(data){ current_explanation.insertAfter(next_explanation);}
	});
}

