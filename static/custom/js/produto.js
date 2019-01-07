$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-variacao").modal("show");
            },
            success: function (data) {
                $("#modal-variacao .modal-content").html(data.html_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#variacao-table tbody tr").html(data.html_variacao_list);
                    $("#modal-variacao").modal("hide");
                }
                else {
                    $("#modal-variacao .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    // Delete variacao
    $("#variacao-table").on("click", ".js-delete-variacao", loadForm);
    $("#modal-variacao").on("submit", ".js-variacao-delete-form", saveForm);

});