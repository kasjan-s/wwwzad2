// This function gets cookie with a given name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
 
/*
The functions below will create a header with csrftoken
*/
 
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
 
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$('.edit').click(function() {
    var obwod_id = $(this).attr("data-id");
    var editbtn = $(this);
    var savebtn = $("#save"+obwod_id);
    var cancelbtn = $("#cancel"+obwod_id);
    var karty_field = $("#karty"+obwod_id);
    var wyborcy_field = $("#wyborcy"+obwod_id);
    var post_karty_field = $("#post_karty"+obwod_id);
    var post_wyborcy_field = $("#post_wyborcy"+obwod_id);

    $.ajax({
        url : "/gminy/obwod/" + obwod_id, 
        type : "GET",
        dataType : 'json',
        success: function(data) {
            console.log(data);
            editbtn.hide();
            savebtn.show();
            cancelbtn.show();
            karty_field.hide();
            karty_field.html(data.karty);
            post_karty_field.show();
            post_karty_field.val(data.karty);
            wyborcy_field.hide();
            wyborcy_field.html(data.wyborcy);
            post_wyborcy_field.show();
            post_wyborcy_field.val(data.wyborcy);
        }
    });
});

$('.save').click(function() {
    var obwod_id = $(this).attr("data-id");
    var editbtn = $("#edit"+obwod_id);
    var savebtn = $("#save"+obwod_id);
    var cancelbtn = $("#cancel"+obwod_id);
    var karty_field = $("#karty"+obwod_id);
    var wyborcy_field = $("#wyborcy"+obwod_id);
    var post_karty_field = $("#post_karty"+obwod_id);
    var post_wyborcy_field = $("#post_wyborcy"+obwod_id);
    console.log(post_karty_field.val());
    console.log(post_wyborcy_field.val());
    $.ajax({
        url : "/gminy/obwod/" + obwod_id + "/", 
        type : "POST",
        data : { karty : post_karty_field.val(), wyborcy : post_wyborcy_field.val() },
        success: function(data) {
            console.log(data);
            editbtn.show();
            savebtn.hide();
            cancelbtn.hide();
            karty_field.show();
            karty_field.html(post_karty_field.val());
            post_karty_field.hide();
            wyborcy_field.show();
            wyborcy_field.html(post_wyborcy_field.val());
            post_wyborcy_field.hide();
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }

    });
});

$('.cancel').click(function() {
    var obwod_id = $(this).attr("data-id");
    var editbtn = $("#edit"+obwod_id);
    var savebtn = $("#save"+obwod_id);
    var cancelbtn = $("#cancel"+obwod_id);
    var karty_field = $("#karty"+obwod_id);
    var wyborcy_field = $("#wyborcy"+obwod_id);
    var post_karty_field = $("#post_karty"+obwod_id);
    var post_wyborcy_field = $("#post_wyborcy"+obwod_id);

    editbtn.show();
    savebtn.hide();
    cancelbtn.hide();
    karty_field.show();
    post_karty_field.hide();
    wyborcy_field.show();
    post_wyborcy_field.hide();
});
