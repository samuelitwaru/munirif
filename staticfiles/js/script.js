var calculateTimeLeft = function (stopTime){
	stopTime = new Date(stopTime)
	now = Date.now()
	// full time left in days
	var fullTimeLeft = (stopTime.getTime() - now) / 1000 / 3600 / 24
	// days
	days = Math.floor(fullTimeLeft)
	// hours
	hours = Math.floor((fullTimeLeft-days)*24)
	// minutes
	_mins = (fullTimeLeft-(days+(hours/24)))*24*60
	var mins = Math.floor(_mins)
		var secs = Math.floor((_mins-mins)*60)
	if (fullTimeLeft > 0){
		return `${days} days, ${hours} hours, ${mins} minutes, ${secs} seconds`
	}
	else {
		return "Finished <span class='fa fa-check'></span>"
	}
}

var setTimeLeft = function(widgetId){
    widget = $(widgetId)[0]
    stopTime = widget.dataset.stopTime
    timeLeft = calculateTimeLeft(stopTime)
    $(widgetId).html(timeLeft)
    setTimeout(()=>setTimeLeft(widgetId), 1000)    

}





function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

var csrftoken = getCookie('csrftoken');


function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});

function updateTimeLeft (stopTime) {
	stopTime = new Date(stopTime)

	// full time left in days
	var fullTimeLeft = (stopTime.getTime() - Date.now()) / 1000 / 3600 / 24
	// days
	days = Math.floor(fullTimeLeft)
	// hours
	hours = Math.floor((fullTimeLeft-days)*24)
	// minutes
	_mins = (fullTimeLeft-(days+(hours/24)))*24*60
	var mins = Math.floor(_mins)
		var secs = Math.floor((_mins-mins)*60)
	if (fullTimeLeft > 0){
		return `${days} days, ${hours} hours, ${mins} minutes, ${secs} seconds`
	}
	else {
		return "Time out!"
	}
	setTimeout(()=>this.updateTimeLeft(), 1000)
}


var ajaxSubmit = function(event){
	event.preventDefault(); //prevent default action
    $(this).attr("action")
    var post_url = $(this).attr("action"); //get form action url
    var request_method = $(this).attr("method"); //get form GET/POST method
    var form_data = $(this).serialize(); //Encode form elements for submission
    var progressContainer = $(this)[0].dataset.progressContainer
    var patchContainers = JSON.parse($(this)[0].dataset.patchContainers)

    $(progressContainer).html(`
            <div class="spinner-border text-info" role="status">
                <span class="sr-only">Loading...</span>
            </div>
            `)

    $.ajax({
    	url : post_url,
        type: request_method,
        data : form_data,
    }).done(function(response){
    	for (var i = 0; i < patchContainers.length; i++) {
    		patchContainer = patchContainers[i]
    		$(patchContainer).replaceWith(response.form_templates[patchContainer]);
    	}
    })
}

$(".ajaxForm").submit(ajaxSubmit)

var loadUrl = function(url, progressContainer, patchContainers){
    $(progressContainer).html(`
        <div class="spinner-border text-info" role="status" align="center">
            <span class="sr-only">Loading...</span>
        </div>
    `)
    $.get(url, function(response) {
        for (var i = 0; i < patchContainers.length; i++) {
            patchContainer = patchContainers[i]
            $(patchContainer).replaceWith(response.form_templates[patchContainer]);
        }
    })
}

var ajaxMultipartSubmitForm = function(event){
	event.preventDefault(); //prevent default action
	var post_url = $(this).attr("action"); //get form action url
	var request_method = $(this).attr("method"); //get form GET/POST method
	var form_data = new FormData(this); //Creates new FormData object

	var progressContainer = $(this)[0].dataset.progressContainer
    var patchContainers = JSON.parse($(this)[0].dataset.patchContainers)

	$(progressContainer).html(`
	        <div class="spinner-border text-info" role="status">
	            <span class="sr-only">Loading...</span>
	        </div>
	`)

	$.ajax({
        url : post_url,
        type: request_method,
        data : form_data,
        contentType: false,
        cache: false,
        processData:false
    }).done(function(response){
    	for (var i = 0; i < patchContainers.length; i++) {
    		patchContainer = patchContainers[i]
    		$(patchContainer).replaceWith(response.form_templates[patchContainer]);
    	}
	});
}

$(".ajaxMultipartForm").submit(ajaxMultipartSubmitForm);