 $(function () {
        $("span.errorMessage").html("${msg}");
        $("div.login_error_message_div").show();
        $("form.loginForm").submit(function () {
            if (0 == $("#name").val().length || 0 == $("#password").val().length) {
                $("span.errorMessage").html("请输入账号密码");
                $("div.login_error_message_div").show();
                return false;
            }
            return true;
        });

        $("form.loginForm input").keyup(function () {
            $("div.login_error_message_div").hide();
        });


        var left = window.innerWidth / 2 + 162;
        $("div.login_small_div").css("left", left);
    })