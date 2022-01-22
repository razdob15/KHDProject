function showElement(elem) {
    elem.removeClass('d-none')
}

function dismissElement(elem) {
    elem.addClass('d-none')
}

function validatePassword(passwordRowElem, givenPassword) {
    if (window.localStorage.getItem('valid_password') === "true") {
        return true;
    } else {
        $.ajax({
            contentType: 'application/json',
            data: JSON.stringify({
                "password": givenPassword
            }),
            dataType: 'json',
            success: function () {
                dismissElement(passwordRowElem)
                dismissAlert(alertElement)
                window.localStorage.setItem("valid_password", "true")
            },
            error: function () {
                showElement(passwordRowElem)
            },
            type: 'POST',
            url: '/api/validate-password'
        });
    }
}