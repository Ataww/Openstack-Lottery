var input = "";
var url = "http://localhost:8090/"
var status_s = false
var status_w = false
var current_id = 0


$(document).ready(function () {

    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1);
    if (hashes == "error") {
        input = "#inputError";
        $("#inputIdentifiant").css("display", "none")
        $("#inputIdentifiantError").css("display", "block")
        $("#error").css("display", "block")
    } else if (hashes == "error_auth") {
        input = "#inputError";
        $("#inputIdentifiant").css("display", "block")
        $("#inputIdentifiantError").css("display", "none")
        $("#error").css("display", "none")
        $("#error_auth").css("display", "block")
    } else {
        input = "#identifiant";
        $("#inputIdentifiant").css("display", "block")
        $("#inputIdentifiantError").css("display", "none")
        $("#error").css("display", "none")
    }

    check_status_i();
    check_status_s();
    check_status_w();
    check_status_p();
    check_status_b();
});

function checkForm() {

    val = $(input).val();

    if (isNumber(val)) {
        isConnect = find_id(val)
        if (isConnect) {
            current_id = val;
            window.location.href = url + val;
        } else {
            window.location.href = url + "?error_auth";
        }
    } else {
        window.location.href = url + "?error";
    }

}

function check_status_i() {
    $.ajax({
        url: url + "ident/0",
        type: "GET",
        isLocal: true,
        success: function () {
            success("#service-I")
            return true
        },
        error: function (jqXHR) {
            if ("404" == jqXHR.statusCode().status) {
                error("#service-I")
            } else {
                warning("#service-I")
            }
        }
    });
    return false
}

function check_status_b() {

    $.ajax({
        url: url + "status_b/",
        type: "GET",
        isLocal: true,
        success: function () {
            if (!status_w || !status_s) {
                warning("#service-B");
            } else {
                success("#service-B")
                return true
            }
        },
        error: function (jqXHR) {
            if ("404" == jqXHR.statusCode().status) {
                error("#service-B");
            } else {
                warning("#service-B");
            }
        }
    });
    return false
}

function check_status_s() {
    $.ajax({
        url: url + "status/0",
        type: "GET",
        isLocal: true,
        success: function () {
            $("#status_not_accessible").css("display", "none")
            success("#service-S");
            status_s = true;
            return true
        },
        error: function (jqXHR) {
            status_s = false;
            if ("404" == jqXHR.statusCode().status) {
                error("#service-S");
                $("#status_not_accessible").css("display", "block")
            } else {
                warning("#service-S");
                $("#status_not_accessible").css("display", "block")

            }
        }
    });
    return false
}

function check_status_w() {
    $.ajax({
        url: url + "status_w/0",
        type: "GET",
        isLocal: true,
        success: function () {
            status_w = true;
            success("#service-W");
            return true
        },
        error: function (jqXHR) {
            status_w = false;
            if ("404" == jqXHR.statusCode().status) {
                error("#service-W");
            } else {
                warning("#service-W");
            }
        }
    });
    return false
}

function check_status_p() {
    $.ajax({
        url: url + "image/0",
        type: "GET",
        isLocal: true,
        success: function () {
            success("#service-P");
            return true
        },
        error: function (jqXHR) {
            if ("404" == jqXHR.statusCode().status) {
                error("#service-P");
            } else {
                warning("#service-P");
            }
        }
    });
    return false
}

function find_id(id) {
    $.ajax({
        url: url + "ident/" + id,
        type: "GET",
        isLocal: true,
        success: function () {
            return true;
        },
        error: function () {
            return false;
        }
    });

}

function recover_status() {
    $.ajax({
        url: url + "status/" + current_id,
        type: "GET",
        isLocal: true,
        success: function (json) {
            var status = json.status;
            if (status === "open") {
                $("#status_not_play").css("display", "block")
                $("#status_play").css("display", "none")
                if (check_status_b()) {
                    $("#play-button").css("display", "block")
                } else {
                    $("#play-button").css("display", "none")
                }
            } else {
                $("#status_not_play").css("display", "none")
                $("#status_play").css("display", "block")
                recover_image()
            }
        },
        error: function () {
            $("#status_not_play").css("display", "none")
            $("#status_play").css("display", "none")
        }
    });
}

function launch_game() {
    $("#play-button").css("display", "none")
    $("#play-button-progressbar").css("display", "block")
    $.ajax({
        url: url + "play/" + current_id,
        type: "GET",
        isLocal: true,
        success: function () {
            $("#play-button-progressbar").css("display", "none")
            recover_image()
        },
        error: function () {
            $("#play-button-progressbar").css("display", "none")
            $("#service_b_error").css("display", "block")
            warning("#service-B")
        }
    });

}

function recover_image() {
    if (check_status_p()) {
        $("#picture").css("display", "block")
        $("#picture_error").css("display", "none")
        var img = $("#photo")[0];
        img.src = url + "image/" + current_id;
    } else {
        $("#picture").css("display", "none")
        $("#picture_error").css("display", "block")

    }
}

function setValue(url_render, id) {
    url = url_render
    current_id = id;
}


function disconnect() {
    window.location.href = url;
}

function isNumber(n) {
    return /^-?[\d.]+(?:e-?\d+)?$/.test(n);
}

function warning(id_balise) {
    $(id_balise).removeClass("label-danger");
    $(id_balise).removeClass("label-success");
    $(id_balise).addClass("label-warning");
}

function success(id_balise) {
    $(id_balise).removeClass("label-danger");
    $(id_balise).removeClass("label-warning");
    $(id_balise).addClass("label-success");
}

function error(id_balise) {
    $(id_balise).removeClass("label-success");
    $(id_balise).removeClass("label-warning");
    $(id_balise).addClass("label-danger");
}