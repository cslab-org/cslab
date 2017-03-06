/* document.addEventListener('DOMContentLoaded', function() {
    alert("Ready!");
}, false); */

$(document).ready(function(){
	$.ajax({
			url: '/writeajax',
			type: 'GET',

			success: function(received_data){
				console.log(received_data);
			},
			error: function(e){
				console.log('Error' + e);
			}
		}); 
	
	
})
