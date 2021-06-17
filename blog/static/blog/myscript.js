
window.onload = function(){

	/*Function to update the x position of the image from the admin dynamically*/
	$( "#id_thumb_nail_y_position" ).change(function() {

		var title = document.getElementById("id_title");
		console.log(title);
		var title = title.value.replace(/\s+/g, '_')
		console.log(title);

		var image = document.getElementById("id_image_" + title);

		console.log(image);
		var x = document.getElementById("id_thumb_nail_x_position").value;
		var y = document.getElementById("id_thumb_nail_y_position").value;

		console.log(y);

		image.style.objectPosition = String(x) +"% " + String(y) + "%";
		console.log(image);
	});

	/*Function to update the y position of the image from the admin dynamically*/
	$( "#id_thumb_nail_y_position" ).bind('input', function() {

		var $this = $(this);
	    var delay = 1000; // 2 seconds delay after last input

	    clearTimeout($this.data('timer'));
	    $this.data('timer', setTimeout(function(){

	        $this.removeData('timer');

	        var title = document.getElementById("id_title");
	        var title = title.value.replace(/\s+/g, '_');

        	var image = document.getElementById("id_image_" + title);
			var x = document.getElementById("id_thumb_nail_x_position").value;
			var y = document.getElementById("id_thumb_nail_y_position").value;

			image.style.objectPosition = String(x) +"% " + String(y) + "%";

			console.log(20);

	    }, delay));
	});


	/*Function to update the y position of the image from the admin dynamically*/
	$( "#id_thumb_nail_x_position" ).bind('input', function() {

		var $this = $(this);
	    var delay = 1000; // 2 seconds delay after last input

	    clearTimeout($this.data('timer'));
	    $this.data('timer', setTimeout(function(){

	        $this.removeData('timer');

	        var title = document.getElementById("id_title");
	        var title = title.value.replace(/\s+/g, '_');

        	var image = document.getElementById("id_image_" + title);
			var x = document.getElementById("id_thumb_nail_x_position").value;
			var y = document.getElementById("id_thumb_nail_y_position").value;

			image.style.objectPosition = String(x) +"% " + String(y) + "%";

			console.log(20);

	    }, delay));
	});
	
	/*Function to update the image dynamically without uploading from the admin*/
	$("#id_thumb_nail").change(function(e){

	    for (var i = 0; i < e.originalEvent.srcElement.files.length; i++) {

	        var title = document.getElementById("id_title");
	        var title = title.value.replace(/\s+/g, '_');

	        var file = e.originalEvent.srcElement.files[i];

	        var image = document.getElementById("id_image_" + title);

	        var reader = new FileReader();
	        reader.onloadend = function() {
	             image.src = reader.result;
	        }
	        reader.readAsDataURL(file);
	    }
	});

};
