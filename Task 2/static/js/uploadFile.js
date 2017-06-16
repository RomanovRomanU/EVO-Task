const submitButton = document.getElementById('formSubmit');
// When upload button is clicked
submitButton.addEventListener('click', e => {
	if (e.preventDefault) {
		e.preventDefault();
	}
    // Take our uploaded file
	const file = document.getElementById('file-1').files[0];
    // Wraping our file to formdata
	const formData = new FormData();
	formData.append('file', file);
    // Set up the request.
	const xhr = new XMLHttpRequest();
	xhr.open('POST', '/download', true);
	xhr.onload = function () {
        // If everything is fine
		if (xhr.status === 200) {
            // Response will be string of such type:
            // "SHA fileCounter"
			const response = xhr.responseText.split(' ');
			const sha = response[0];
            // How many times this file was uploaded
			const fileCounter = response[1];
            // Now lets count MD4 hashon client side
			cilent_crc16 = hash_crc16(file);
            // Recording this values to page
			document.getElementById('sha256').innerHTML = `<p><b>SHA256 is:</b></p> ${sha}`;
			document.getElementById('crc16').innerHTML = `<p><b>MD4 id:</b></p> ${cilent_crc16}`;
			document.getElementById('fileCounter').innerHTML = `<p><b>Was downloaded:</b></p>${fileCounter} times.`;
		}
        // If our file is incorrect
		if (xhr.status === 400) {
			alert(
                'The file format or content is incorrect.Try again'
            );
		}
	};
	xhr.send(formData);
});

function hash_crc16(file) {
	file = String(file);
	return crc16(file);
}
