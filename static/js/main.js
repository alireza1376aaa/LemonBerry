AOS.init({
    duration: 800,
    easing: 'slide'
});

(function ($) {

    "use strict";

    var isMobile = {
        Android: function () {
            return navigator.userAgent.match(/Android/i);
        },
        BlackBerry: function () {
            return navigator.userAgent.match(/BlackBerry/i);
        },
        iOS: function () {
            return navigator.userAgent.match(/iPhone|iPad|iPod/i);
        },
        Opera: function () {
            return navigator.userAgent.match(/Opera Mini/i);
        },
        Windows: function () {
            return navigator.userAgent.match(/IEMobile/i);
        },
        any: function () {
            return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
        }
    };


    $(window).stellar({
        responsive: true,
        parallaxBackgrounds: true,
        parallaxElements: true,
        horizontalScrolling: false,
        hideDistantElements: false,
        scrollProperty: 'scroll'
    });


    var fullHeight = function () {

        $('.js-fullheight').css('height', $(window).height());
        $(window).resize(function () {
            $('.js-fullheight').css('height', $(window).height());
        });

    };
    fullHeight();

    // loader
    var loader = function () {
        setTimeout(function () {
            if ($('#ftco-loader').length > 0) {
                $('#ftco-loader').removeClass('show');
            }
        }, 1);
    };
    loader();

    // Scrollax
    $.Scrollax();

    var carousel = function () {
        $('.carousel-testimony').owlCarousel({
            center: true,
            loop: true,
            items: 1,
            margin: 30,
            stagePadding: 0,
            nav: false,
            navText: ['<span class="ion-ios-arrow-back">', '<span class="ion-ios-arrow-forward">'],
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 2
                },
                1000: {
                    items: 3
                }
            }
        });

    };
    carousel();

    $('nav .dropdown').hover(function () {
        var $this = $(this);
        // 	 timer;
        // clearTimeout(timer);
        $this.addClass('show');
        $this.find('> a').attr('aria-expanded', true);
        // $this.find('.dropdown-menu').addClass('animated-fast fadeInUp show');
        $this.find('.dropdown-menu').addClass('show');
    }, function () {
        var $this = $(this);
        // timer;
        // timer = setTimeout(function(){
        $this.removeClass('show');
        $this.find('> a').attr('aria-expanded', false);
        // $this.find('.dropdown-menu').removeClass('animated-fast fadeInUp show');
        $this.find('.dropdown-menu').removeClass('show');
        // }, 100);
    });


    $('#dropdown04').on('show.bs.dropdown', function () {
        console.log('show');
    });

    // scroll
    var scrollWindow = function () {
        $(window).scroll(function () {
            var $w = $(this),
                st = $w.scrollTop(),
                navbar = $('.ftco_navbar'),
                sd = $('.js-scroll-wrap');

            if (st > 150) {
                if (!navbar.hasClass('scrolled')) {
                    navbar.addClass('scrolled');
                }
            }
            if (st < 150) {
                if (navbar.hasClass('scrolled')) {
                    navbar.removeClass('scrolled sleep');
                }
            }
            if (st > 350) {
                if (!navbar.hasClass('awake')) {
                    navbar.addClass('awake');
                }

                if (sd.length > 0) {
                    sd.addClass('sleep');
                }
            }
            if (st < 350) {
                if (navbar.hasClass('awake')) {
                    navbar.removeClass('awake');
                    navbar.addClass('sleep');
                }
                if (sd.length > 0) {
                    sd.removeClass('sleep');
                }
            }
        });
    };
    scrollWindow();

    var isMobile = {
        Android: function () {
            return navigator.userAgent.match(/Android/i);
        },
        BlackBerry: function () {
            return navigator.userAgent.match(/BlackBerry/i);
        },
        iOS: function () {
            return navigator.userAgent.match(/iPhone|iPad|iPod/i);
        },
        Opera: function () {
            return navigator.userAgent.match(/Opera Mini/i);
        },
        Windows: function () {
            return navigator.userAgent.match(/IEMobile/i);
        },
        any: function () {
            return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
        }
    };

    var counter = function () {

        $('#section-counter, .hero-wrap, .ftco-counter').waypoint(function (direction) {

            if (direction === 'down' && !$(this.element).hasClass('ftco-animated')) {

                var comma_separator_number_step = $.animateNumber.numberStepFactories.separator(',')
                $('.number').each(function () {
                    var $this = $(this),
                        num = $this.data('number');
                    console.log(num);
                    $this.animateNumber(
                        {
                            number: num,
                            numberStep: comma_separator_number_step
                        }, 7000
                    );
                });

            }

        }, {offset: '95%'});

    }
    counter();


    var contentWayPoint = function () {
        var i = 0;
        $('.ftco-animate').waypoint(function (direction) {

            if (direction === 'down' && !$(this.element).hasClass('ftco-animated')) {

                i++;

                $(this.element).addClass('item-animate');
                setTimeout(function () {

                    $('body .ftco-animate.item-animate').each(function (k) {
                        var el = $(this);
                        setTimeout(function () {
                            var effect = el.data('animate-effect');
                            if (effect === 'fadeIn') {
                                el.addClass('fadeIn ftco-animated');
                            } else if (effect === 'fadeInLeft') {
                                el.addClass('fadeInLeft ftco-animated');
                            } else if (effect === 'fadeInRight') {
                                el.addClass('fadeInRight ftco-animated');
                            } else {
                                el.addClass('fadeInUp ftco-animated');
                            }
                            el.removeClass('item-animate');
                        }, k * 50, 'easeInOutExpo');
                    });

                }, 100);

            }

        }, {offset: '95%'});
    };
    contentWayPoint();


    // magnific popup
    $('.image-popup').magnificPopup({
        type: 'image',
        closeOnContentClick: true,
        closeBtnInside: false,
        fixedContentPos: true,
        mainClass: 'mfp-no-margins mfp-with-zoom', // class to remove default margin from left and right side
        gallery: {
            enabled: true,
            navigateByImgClick: true,
            preload: [0, 1] // Will preload 0 - before current, and 1 after the current image
        },
        image: {
            verticalFit: true
        },
        zoom: {
            enabled: true,
            duration: 300 // don't foget to change the duration also in CSS
        }
    });

    $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
        disableOn: 700,
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false,

        fixedContentPos: false
    });


})(jQuery);


function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#blah').attr('src', e.target.result).width(150).height(200);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// function subfilter() {
//
//     var selectBox = document.getElementById("filter");
//     var selectedValue = selectBox.options[selectBox.selectedIndex].value;
//     var button_action = document.getElementById("click_sub");
//     var first_page = document.getElementById('first_for_filter');
//     var x = window.location.href;
//     // if (selectedValue.length > 0) {
//     //     var result = x.includes("?page=1#");
//     //     button_action.click();
//     //     if (result) {
//     //     } else {
//     //         first_page.click();
//     //     }
//     // }
//     selectedValue.preventDefault();
//
//     alert(selectedValue)
//
// }

// $('#form-id').submit(function () {
//     var data = {
//         'csrfmiddlewaretoken': '$(input[name=csrfmiddlewaretoken]).val()',
//         'filter': $('#filter').val(),
//         'search': $('#search').val(),
//     }
//
//     $.ajax({
//         url: '',
//         method: 'POST',
//         data: data,
//         dataType: 'json',
//         success: function (data) {
//         }
//     })
// });
//
//
//
// $(document).ready(function () {
//     $('#post_form').submit(function (e) {
//         e.preventDefault();
//         $.ajax({
//             method: 'POST',
//             url: 'http://127.0.0.1:8000/web_log/list/filter',
//             data: {
//                 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
//                 'filter': $('#filter').val(),
//                 'search': $('#search').val(),
//             },
//             success: function (e) {
//                 $('#alireza').html(e.body);
//             },
//
//         })
//
//     })
// })

function comment() {
    var massage = $('#message').val();
    var idofweb = $('#idofweb').val();
    var parent = $('#idofparentweb').val();

    $.get('/web_log/listcomment', {
        comment_mesage: massage,
        id_Weblog: idofweb,
        parent: parent
    }).then(res => {
        $('#comment_box').html(res)
        $('#message').val('');
        $('#idofparentweb').val('');
        if (parent !== null && parent !== '') {
            document.getElementById('box_commenr' + parent).scrollIntoView({behavior: "smooth"});
        } else {
            document.getElementById('comment_box').scrollIntoView({behavior: "smooth"});

        }
    })
};

function parentid(artcomment_child) {
    $('#idofparentweb').val(artcomment_child);
    document.getElementById('addcomment').scrollIntoView({behavior: "smooth"});
};


function filter_weblog() {
    var get_val_filter = $('#filter_web').find(':selected').val();
    var get_text_filter = $('#filter_web').find(':selected').text();

    if (get_val_filter.length > 2) {
        $.ajax({
            method: 'GET',
            url: '/web_log/list/cat/filter',
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'filter': get_val_filter,
            },
            success: function (res) {
                $('#set_first_filter').text(get_text_filter);
                $('#filter_web').val('');
                $('#container_id').html(res);
                console.log(res);
            },
        })
    }

}

function paginator(input) {
    $.ajax({
        method: 'GET',
        url: '/web_log/list/cat/filter',
        data: {
            'page': input,
        },
        success: function (res) {
            $('#container_id').html(res);
            document.getElementById('main_section').scrollIntoView({behavior: "smooth"});
        },
    })
}

function searchfunc() {
    var search = $('#search').val()
    $.ajax({
        method: 'GET',
        url: '/web_log/list/cat/search',
        data: {
            'search': search,
        },
        success: function (res) {
            $('#container_id').html(res);
            // $('#container_id').html(res);
            // document.getElementById('main_section').scrollIntoView({behavior: "smooth"});
        },
    })
}

function checkemail() {
    var Email = $('#email_fild').val()
    $.ajax({
        method: 'GET',
        url: '/contact/chekemail',
        data: {
            'email_ad': Email,
        },
        success: function (res) {
            if (res.length > 0) {
                var subject = $('#subject_co').prop('disabled', true);
                var massage = $('#massage_co').prop('disabled', true);
                var submit = $('#login_button').html('<a href="/user/login" class="btn btn-primary py-3 px-5">Log In</a>')

            }

            var alert_email = $('#alert_text_fild').html(res);
            document.getElementById().attr('color', 'red')

        },
    })
}

function send_contact() {
    var Email = $('#email_fild').val()
    var subject = $('#subject_co').val()
    var massage = $('#massage_co').val()

    $.ajax({
        method: 'GET',
        url: '/contact/chekemail/send_contact',
        data: {
            'email_ad': Email,
            'subject': subject,
            'massage': massage,
        },
        success: function (res) {

            var send_fidback = $('#massage_result').html(res).addClass('alert alert-success');

        },
    })
}

function searchtext() {
    var searchQuery = document.querySelector("#inputSearch");
    var context1 = document.querySelector("#context_1");
    var context2 = document.querySelector("#context_2");
    var context3 = document.querySelector("#context_3");
    var context4 = document.querySelector("#context_4");

    searchQuery.addEventListener('input', searchQueryResults)

    function searchQueryResults() {
        context1.innerHTML = context1.textContent.replace(new RegExp(searchQuery.value, "gi"), (match) => `<u style="color:#de0041; background-color: #ffe344">${match}</u>`);
        context2.innerHTML = context2.textContent.replace(new RegExp(searchQuery.value, "gi"), (match) => `<u style="color:#de0041; background-color: #ffe344">${match}</u>`);
        context3.innerHTML = context3.textContent.replace(new RegExp(searchQuery.value, "gi"), (match) => `<u style="color:#de0041; background-color: #ffe344">${match}</u>`);
        context4.innerHTML = context4.textContent.replace(new RegExp(searchQuery.value, "gi"), (match) => `<u style="color:#de0041; background-color: #ffe344">${match}</u>`);
    }
}

var list = [];

function addTag() {
    var tag = $('#inputTag').val();
    if (tag.length > 1) {
        if (list.length < 5) {
            list.push(tag)
            var addmethodclick = " onclick='removeTag(\"" + tag + "\");validlist()'";
            var tagcloud = $('#tagcloud').append('<a id="tagofid' + tag + '" ' + addmethodclick + ' class="tag-cloud-link remov_tag">' + tag + '</a>');
            var tage = $('#inputTag').val('');
        } else {
            var warning_tag = $('#warning_tag').html('<p> You cannot select more than 5 items </p>');
            var tage = $('#inputTag').val('');

        }
    }

}

function removeTag(input) {
    var power = $('#tagofid' + input + '').remove()
    var index_remove = list.indexOf(input);
    list.splice(index_remove, 1);
}


function show_section2() {
    $('.section_body_2').toggle("slow")
}

function show_section3() {
    $('.section_body_3').toggle("slow")
}

function show_section4() {
    $('.section_body_4').toggle("slow")
}


//
// function send_tag_list() {
//
//     $.ajax({
//         method: 'POST',
//         url: '/web_log/makeblog',
//         dataType: "json",
//         data: {
//             'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
//             'tag_list': list,
//
//         },
//
//         success: function (res) {
//             console.log(res)
//         },
//     })
// }

function showMyImage(fileInput, id, imgid) {
    var files = fileInput.files;
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        var imageType = /image.*/;
        if (!file.type.match(imageType)) {
            continue;
        }

        var reader = new FileReader();
        reader.onload = (function (aImg) {
            return function (e) {
                console.log(e.loaded);
                if (e.loaded < 5000000) {
                    var x = $(id).css({
                        'background-image': 'url(' + e.target.result + ')',
                        'background-size': 'contain'
                    });
                } else {
                    $(id).append('<h4>size photo more than 5mb</h4>');
                    $(imgid).val('');

                }
            };
        })();
        reader.readAsDataURL(file);
    }
}


$(document).ready(function () {
    $('#category option[value=""]').attr({'disabled': 'disabled', 'hidden': 'hidden', 'selected': 'selected'})
    $('#genre option:selected').attr({'disabled': 'disabled', 'hidden': 'hidden', 'selected': 'selected'})
    change_color();
});

function validlist() {

    $('#list_tag').val(list);

}

function add_score(user_id, weblog_id) {
    var rate_add = $('input[name=rating]:checked').val()
    if (rate_add == null) {
        $('#error_rate_text').text('select rate')
    } else {
        $.ajax({
            method: 'GET',
            url: '/web_log/list/cat/addrate',
            data: {'rate': rate_add, 'user': user_id, 'weblog_id': weblog_id},
            success: function (res) {
                $('#reload_rate_ajax').html(res);
                change_color();
            }
        })
    }
}

function change_color() {
    var myrateval = $('#number_rate').text();
    var convertval = Number(myrateval.split('%')[0])
    if (convertval <= 30) {
        $('#number_rate').css('background-color', '#ec204f');
    } else if (convertval <= 50 && convertval > 30) {
        $('#number_rate').css('background-color', '#fd673a');
    } else if (convertval > 50 && convertval <= 60) {
        $('#number_rate').css('background-color', '#ff922c')
    } else if (convertval <= 70 && convertval > 60) {
        $('#number_rate').css('background-color', '#feed47')
    } else if (convertval > 70 && convertval <= 80) {
        $('#number_rate').css('background-color', '#8de45f')
    } else if (convertval <= 95 && convertval > 80) {
        $('#number_rate').css('background-color', '#2ecf03')
    } else if (convertval > 95 && convertval <= 100) {
        $('#number_rate').css({'background-color': '#1c6b00', 'color': '#debb00'})
    }

}
z