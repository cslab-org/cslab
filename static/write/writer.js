/* document.addEventListener('DOMContentLoaded', function() {
    alert("Ready!");
}, false); */

$(document).ready(function(){
	$.ajax({
			url: '/writeajax',
			type: 'GET',

			success: function(received_data){
				data = JSON.parse(received_data);
				//console.log(received_data);
				var article_list = '<ol>';
				for (var i=0; i<data.length; i++) {
					var datum = data[i];
					article_list += '<li>' + datum['title'] + '</li>';
				}
				article_list += '</ol>';
				// Insert to the html 
				$('#display-articles').html(article_list);
			},
			error: function(e){
				console.log('Error' + e);
			}
		}); 
	
	
})
