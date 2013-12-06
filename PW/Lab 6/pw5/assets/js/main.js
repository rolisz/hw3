var jplayer = $("#jquery_jplayer_1");
$('body').on('click', '.container-mesaj',function (e) {
    e.preventDefault();
    var hidden = $(this).find('.hidden').clone();
    var el = hidden.replaceAll($('.details'));
    console.log($(this).find('.mp3_link'));
    el.removeClass('hidden').addClass('details').addClass('span4').addClass('hidden-phone');
    jplayer.jPlayer("setMedia", {
        mp3:el.find('.mp3_link').attr("href")
    }).jPlayer("play");

}).on('click', '#loginBtn, #backLogin ',function (e) {
        e.preventDefault();
        var m = $('#modal').removeData("modal").modal({remote: 'login.php'});
        m.find('.modal-header h3').text('Autentificare');
        m.find('.modal-footer').html('<a href="inregistrare.php" id="inreg" class="btn">Înregistrare</a>\
            <a href="forgot.php" id="forgot" class="btn">Am uitat parola</a>');


    }).on('submit', '#loginForm', function (e) {
        e.preventDefault();
        $.post('login.php', {
                username: $('#inputUser').val(),
                password: $('#inputPassword').val(),
                remember: $('#rememberMe').is(':checked')
            }, function (data) {
            if (data.result == 'success') {
                $('.modal-body').text('Autentificare cu succes');
                location.reload();
            } else {
                $('.modal-body').prepend('<p>Autentificare e?uat?. Încerca?i din nou!</p>')
            }
        },'json');


    }).on('click','#inreg',function(e) {
        e.preventDefault();
        var m = $('#modal').removeData("modal").modal({remote: 'inregistrare.php'});
        m.find('.modal-header h3').text('Înregistrare');
        m.find('.modal-footer').html('<button type="submit" class="btn btn-primary" id="register">Înregistrare</button>\
        <button type="button" class="btn" id="backLogin">Înapoi</button>');


    }).on('click', '#forgot',function(e) {
        e.preventDefault();
        var m = $('#modal').removeData("modal").modal({remote: 'forgot.php'});
        m.find('.modal-header h3').text('Recuperare parol?');
        m.find('.modal-footer').html('<button type="submit" class="btn btn-primary" id="recover">Trimite email</button>\
        <button type="button" class="btn" id="backLogin">Înapoi</button>');


    })
    .on('click', '#register', function(e) {
        e.preventDefault();
        var viewArr = $('#regForm').serializeArray(), view = {};

        for (var i in viewArr) {
            view[viewArr[i].name] = viewArr[i].value;
        }
        $.post('inregistrare.php', view, function(data) {
            if (data.result == 'success') {
                $('.modal-body').text('Înregistrare cu succes');
                location.reload();
            } else {
				var p = $('<p>Înregistrare eșuată. Încercați din nou!</p>').prependTo('.modal-body');
                console.log(p);
				$.each(data.errors, function(ind, val) {
					p.after('<p>' + val + '</p>');
				});
                //todo highlight errors
            }
        },'json')


    })
    .on('click','#recover', function(e) {
        e.preventDefault();
        $.post('forgot.php', {
            email: $('#email').val()
        }, function (data) {
            $('.modal-body').text(data.result);
        },'json');


    }).on('click','#logoutBtn', function(e) {
        e.preventDefault();
        $.get('logout.php',function() {
            location.reload();
        });


    }).on('click','#contact', function(e) {
        e.preventDefault();
        var m = $('#modal').removeData("modal").modal({remote: 'contact.php'});
        m.find('.modal-header h3').text('Contact');
        m.find('.modal-footer').html('<button type="submit" class="btn btn-primary" id="contact_send">Trimite email</button>');

    }).on('click','#contact_send', function(e) {
        $.post('contact.php', $('#contactForm').serialize(), function (data) {
            $('.modal-body').text(data.result);
        },'json');
    })


$('#modal').on('hidden', function() {
    $('#modal').removeData("modal");
})

jplayer.jPlayer({
    swfPath: "assets/js",
    supplied: "mp3",
    wmode: "window",
    smoothPlayBar: true,
    keyEnabled: true,
    verticalVolume: true,
    ready: function () {
        $(this).jPlayer("setMedia", {
            mp3: "http://"+$('#live_play').data('ip')
        });
    }
});

$('.search_form li').click(function(e) {
    e.stopPropagation();
});

$('.lang_menu a').click(function(e) {
    e.preventDefault();
    var date = new Date();
    date.setFullYear(date.getFullYear() + 1);
    document.cookie = "lang="+$(this).data("lang")+";expires="+date.toUTCString();
    location.reload();
})

$('#live_play').click(function(e) {
    console.log($(this).data());
    jplayer.jPlayer("setMedia", {
        mp3:"http://"+$(this).data('ip')
    }).jPlayer("play");
})

$('.dropdown-toggle').click(function(e) {
    e.preventDefault();
    setTimeout($.proxy(function() {
        if ('ontouchstart' in document.documentElement) {
            $(this).siblings('.dropdown-backdrop').off().remove();
        }
    }, this), 0);
});