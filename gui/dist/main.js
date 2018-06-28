$('document').ready(function(){
    $("#getting-started")
      .countdown("2018/06/30 16:50", function(event) {
        $(this).text(
          "End of bets: " + event.strftime('%d day, %H:%M:%S')
        );
      });

    $('form').submit(function(e){
        var employee_id = $('input[name="employee_id"]').val();
        var employee_name = $('input[name="employee_name"]').val();

        var bets = $('select[name^=games]').map(function(idx, elem) {
            return $(elem).val();
          }).get();


        var msg = employee_id + ',';
        msg += employee_name + ',';

        msg += bets.join();

        $("#prosubmit").addClass('disabled').text('Loading');
        $.ajax({
            type: "POST",
            url: FC_URL,
            // The key needs to match your method's input parameter (case-sensitive).
            data: JSON.stringify({ data: msg }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data){
                $("#prosubmit").text('Done!');
                alert("Your pronostics was send. Thank you!");
            },
            failure: function(errMsg) {
                alert(errMsg);
            }
        });
        return false;
    })
});