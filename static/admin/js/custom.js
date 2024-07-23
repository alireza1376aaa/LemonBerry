function toggle_add() {
    $("#toggle_add_val").css('visibility', 'visible');
}

function toggle_add_close() {
    $("#toggle_add_val").css('visibility', 'hidden');
}


function short_active_blog(id) {
    var checkbox = $('#cat_id_' + id).prop('checked');
    $('#set_act_jq_' + id).val(checkbox);
}

function load_rate() {
    $('.number_rate').click()
}

function color(convertval, id) {
    if (convertval <= 30) {
        $('#number_rate' + id).css('background-color', '#ec204f');
    } else if (convertval <= 50 && convertval > 30) {
        $('#number_rate' + id).css('background-color', '#fd673a');
    } else if (convertval > 50 && convertval <= 60) {
        $('#number_rate' + id).css('background-color', '#ff922c')
    } else if (convertval <= 70 && convertval > 60) {
        $('#number_rate' + id).css('background-color', '#feed47')
    } else if (convertval > 70 && convertval <= 80) {
        $('#number_rate' + id).css('background-color', '#8de45f')
    } else if (convertval <= 95 && convertval > 80) {
        $('#number_rate' + id).css('background-color', '#2ecf03')
    } else if (convertval > 95 && convertval <= 100) {
        $('#number_rate' + id).css({'background-color': '#1c6b00', 'color': '#debb00'})
    }
}

function filter_li(id) {
    var filter_i = $('#' + id).text()
    var filter_val = null
    if (filter_i === 'Title') {
        filter_val = 'title'
    } else if (filter_i === 'Writer') {
        filter_val = 'auter.get_full_name'
    } else if (filter_i === 'date') {
        filter_val = 'date'
    } else if (filter_i === 'Active/Disabel') {
        filter_val = 'is_active'
    } else if (filter_i === 'deleted') {
        filter_val = 'is_delete'
    } else if (filter_i === 'Rate') {
        filter_val = 'satisfaction_percentage'
    }
    $.ajax({
        url: 'admin/admin_panel/weblog/list_blog',
        method: 'GET',
        data: {'filter': filter_val},
        success: function (res) {
        }
    })
}

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