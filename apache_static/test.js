$(document).ready(function()
{
	$('div.checkbox').click(function(event)
		{
			$(event.target).children('input').trigger('click');
		});
	$('#btn-next').hide();
	$('#choice-form').bind('submit', function(event)
		{
			event.preventDefault();
			return false;
		});
	$('#btn-submit').bind('click', function(event)
		{
			answers = $('input[type="checkbox"]').filter('input[is-answer="true"]');
			selected_answers = $('input[type="checkbox"]')
								.filter('input[is-answer="true"]')
								.filter(':checked');
			not_selected_answers = $('input[type="checkbox"]')
								.filter('input[is-answer="true"]')
								.not(':checked');
			selected_non_answers = $('input[type="checkbox"]')
								.not('input[is-answer="true"]')
								.filter(':checked');
			if (selected_non_answers.size() + selected_answers.size() != answers.size())
			{
				alert('You have to choice ' + answers.size() + ' choices');
				return ;
			}

			not_selected_answers = not_selected_answers.parent();
			selected_non_answers = selected_non_answers.parent();
			selected_answers = selected_answers.parent();

			not_selected_answers.addClass('alert-danger');
			selected_non_answers.addClass('alert-danger');
			selected_answers.addClass('alert-success');
		
			for (var i = 0; i < selected_answers.size(); i++)
			{
				$.ajax({
					url: 'update/' + selected_answers.eq(i).attr('question-id') + '/1',
					async: false,
					dataType: 'text'
				});
			}
			for (var i = 0; i < not_selected_answers.size(); i++)
			{
				$.ajax({
					url: 'update/' + not_selected_answers.eq(i).attr('question-id') + '/0',
					async: false,
					dataType: 'text'
				});
			}
			$('#btn-next').show();
			$('#btn-submit').hide();
			$('span.answer').show();
		});
	$('#btn-next').bind('click', function(event){ location.reload();});
	$('span.answer').hide();
});



