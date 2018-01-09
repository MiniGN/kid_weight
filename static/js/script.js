$(document).ready(function () {
    // Обработка отправки формы
    var form = $('#form_adding');
    console.log(form)
    form.on('submit', function (e) {
        e.preventDefault();
        $('.error-msg').addClass('hidden');

        var data = {};
        data.date = $('#date').val();
        data.weight = $('#weight').val();
        var csrf_token = $('#form_adding [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;
        var url = form.attr("action");
        console.log(url);
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                console.log("OK");
                if (data.error) {
                    $('#error_msg').text(data.error);
                    $('.error-msg').removeClass('hidden');
                } else {
                    // Обновляем таблицу
                    $.ajax({
                        url: '/async_weight_table/',
                        success: function (data) {
                            $('#weight-table').html(data);
                        }
                    });
                    // Обновляем графики
                    $.ajax({
                        url: '/async_weight_chart/',
                        success: function (data) {
                            $('#weight-chart').html(data);
                        }
                    });
                }
            },
            error: function () {
                console.log('error');
            }
        })
    })

    // Удаление строчки из таблицы
    $(document).on('click', '.delete-item', function (e) {
        e.preventDefault();
        var data = {};
        data.weight_id = $(this).data("weight_id");
        var csrf_token = $('#form_adding [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;
        $.ajax({
            url: '/remove_weight/',
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                console.log("OK");
                // Обновляем таблицу
                $.ajax({
                    url: '/async_weight_table/',
                    success: function (data) {
                        $('#weight-table').html(data);
                    }
                });
                // Обновляем графики
                $.ajax({
                    url: '/async_weight_chart/',
                    success: function (data) {
                        $('#weight-chart').html(data);
                    }
                });
            },
            error: function () {
                console.log('error');
            }
        })
    })

    // Кнопка Редактирование строчки из таблицы
    $(document).on('click', '.glyphicon-edit', function (e) {
        e.preventDefault();
        var weight_id = $(this).data("weight_id");
        var desc_id="desc_"+weight_id
        var td=$('#'+desc_id)
        var desc_text_old=td.html()
        console.log()
        td.html('<form><div class="input-group"><input type="text" size=30 maxlength="25" class="form-control edit-field" id="input_'+weight_id+'" value='+desc_text_old+'></div></form>')
        $(this).removeClass('glyphicon-edit')
        $(this).addClass('glyphicon-ok')
    })

    // Кнопка Сохранение строчки из таблицы
    $(document).on('click', '.glyphicon-ok', function (e) {

        e.preventDefault();
        btn=$(this)
        var weight_id = $(this).data("weight_id");
        var desc_id="input_"+weight_id;
        var input=$('#'+desc_id);
        desc=input.val();
        var data = {};
        data.weight_id=weight_id;
        data.desc=desc
        var csrf_token = $('#form_adding [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;
        $.ajax({
            url: '/edit_desc_weight/',
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                var desc_id="desc_"+weight_id;
                var td=$('#'+desc_id);
                console.log(td);
                td.html(desc);
                console.log(desc);
                btn.removeClass('glyphicon-ok');
                btn.addClass('glyphicon-edit');
            },
            error: function () {
                console.log('error');
            }
        })
    })




})