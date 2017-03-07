/* document.addEventListener('DOMContentLoaded', function() {
    alert("Ready!");
}, false); */

$(document).ready(function(){
	// Send an AJAX request, to retrieve all articles, as soon as page loads
	$.ajax({
		url: '/writeajax',
		type: 'GET',

		success: function(received_data){
			data = JSON.parse(received_data);
			//console.log(received_data);
			var article_list = '';
			for (var i=0; i<data.length; i++) {
				var datum = data[i];
				article_list += '<div class="article-list-div">' + 
					'<div class="article-title">' + datum['title'] + '</div>' + 
					'<div class="article-sub-lining">' + 
						'<div class="article-kind">' + datum['kind'] + '</div>' +
						'last edited: ' + datum['lastEdited'] +
					'</div>' +
					'<div class="article-description">' + datum['description'] + '</div>' +
					'</div>';
			}
			// article_list += '';
			// Insert to the html 
			$('#display-articles').html(article_list);
		},
		error: function(e){
			console.log('Error' + e);
		}
	}); 
	
	
	// Click on previous article title should lead to writedown page
	$('#display-articles').on('click', '.article-title', function() {
		console.log('clicked')
		window.location.href = '../writedown'
	});	
	
})
