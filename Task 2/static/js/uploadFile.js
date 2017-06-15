var submitButton = document.getElementById('formSubmit');
// When upload button is clicked
submitButton.addEventListener('click', function (e) {
	if (e.preventDefault) {
		e.preventDefault();
	}
	// Take our uploaded file
	var file = document.getElementById('file-1').files[0];
	// Wraping our file to formdata
	var formData = new FormData();
	formData.append('file',file);
	// Set up the request.
	var xhr = new XMLHttpRequest();
	xhr.open('POST','/download',true);
	xhr.onload = function(){
		// If everything is fine
		if (xhr.status === 200) {
			// Response will be string of such type:
			// "SHA fileCounter"
			var response = xhr.responseText.split(' ');
			var sha = response[0];
			// How many times this file was uploaded
			var fileCounter = response[1];
			console.log(response[2]);
			// Recording this values to page
			document.getElementById('sha').innerHTML = `<i>SHA256 is:</i> ${sha}`;
			document.getElementById('fileCounter').innerHTML = `<i>Was downloaded:</i>${fileCounter} times.`;
		}
		// If our file is incorrect
		if (xhr.status === 400) {
			alert(
				'The file format or content is incorrect.Try again'
				);
		}
	}
	xhr.send(formData);
});