jQuery().ready(function() {

    var v = jQuery("#basicform").validate({
        rules: {
            nisn: {
                required: true,
                minlength: 9,
                maxlength: 16
            },
            uemail: {
                required: true,
                minlength: 2,
                email: true,
                maxlength: 100,
            },
            upass1: {
                required: true,
                minlength: 6,
                maxlength: 15,
            },
            upass2: {
                required: true,
                minlength: 6,
                equalTo: "#upass1",
            }

        },
        errorElement: "span",
        errorClass: "help-inline",
    });


    // Binding next button on first step
    $(".open1").click(function() {
        if (v.form()) {
            $(".frm").hide("fast");
            $("#sf2").show("slow");
        }
    });

    $(".open2").click(function() {
        if (v.form()) {
            $(".frm").hide("fast");
            $("#sf3").show("slow");
        }
    });

    $(".open3").click(function() {
        if (v.form()) {
            $(".frm").hide("fast");
            $("#sf4").show("slow");
        }
    });

    // Binding back button on second step
    $(".back2").click(function() {
        $(".frm").hide("fast");
        $("#sf1").show("slow");
    });

    // Binding back button on third step
    $(".back3").click(function() {
        $(".frm").hide("fast");
        $("#sf2").show("slow");
    });

    // Binding back button on third step
    $(".back4").click(function() {
        $(".frm").hide("fast");
        $("#sf3").show("slow");
    });

    $(".open4").click(function() {
        if (v.form()) {
            // optional
            // used delay form submission for a seccond and show a loader image
            $("#loader").show();
            setTimeout(function(){
              $ ("#basicform").html('<h2>Thanks for your time.</h2>');
            }, 1000);
            // Remove this if you are not using ajax method for submitting values
            return false;
        }
    });
});