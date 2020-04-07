/*Для отправки сообщения*/ 
/*$(document).ready(function() {

	//E-mail Ajax Send
	$("form").submit(function() { //Change
		var th = $(this);
		$.ajax({
			type: "POST",
			url: "mail.php", //Change
			data: th.serialize()
		}).done(function() {
			alert("Thank you!");
			setTimeout(function() {
				// Done Functions
				th.trigger("reset");
			}, 1000);
		});
		return false;
	});

});

async function sendImage(form) {
	event.preventDefault();
    const scriptURL = "";

    var loading = document.createElement('div')
    loading.classList.add('lds-facebook');
    loading.innerHTML = "<div></div><div></div><div></div>"
    document.getElementById('top').appendChild(loading);
    alert("Изображение отправлено на проверку");

    let response = await fetch(scriptURL, {
        method: 'POST',
        body: new FormData(form)
    })

    let result = await response.json();
    document.getElementById('result').innerHTML = result.message; //сервер должен вернуть ответ в формате "{message:'Ваше изображение - фейк'}"

    document.getElementById('top').querySelector('lds-facebook').remove()
}
