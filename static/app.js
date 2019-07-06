$(document).ready(function () {
    $("#addBot").click(function () {
        $("#botform").toggle();
    });

    $(".botRun").click(function () {
        var bot_name = $(this).attr('class').split(" ")[1];
        $.ajax({
                contentType: "application/json",

                url: "/run",
                method: "POST",
                async: false,
                dataType: "json",
                data: {
                    'bot_name': bot_name,
                },
                success: function (succs) {

                    location.reload();


                },
            }
        );
    });
    $(".botStop").click(function () {
        var bot_name = $(this).attr('class').split(" ")[1];
        $.ajax({
                contentType: "application/json",

                url: "/kill",
                method: "POST",
                async: false,
                dataType: "json",
                data: {
                    'bot_name': bot_name,
                },
                success: function (succs) {

                    location.reload();


                },
            }
        );
    });
    $(".botDelete").click(function () {
        var bot_name = $(this).attr('class').split(" ")[1];
        $.ajax({
                contentType: "application/json",

                url: "/delete",
                method: "POST",
                async: false,
                dataType: "json",
                data: {
                    'bot_name': bot_name,
                },
                success: function (succs) {

                    location.reload();


                },
            }
        );
    });
});