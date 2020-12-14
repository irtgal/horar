
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

var dates = $(".date");
var i;
for (i = 0; i < dates.length; i++) {
  var shifts = $(dates[i]).find(".shift");
  var span = Math.floor(12/shifts.length);
  if (0 < span && span < 13){
    $(shifts).attr("colspan", span);
  }
}



// obarvani tedni
function colorWeeks(e){
    var first_mon = $(".day-td:contains('Mon')")[0].closest(".date");
    var days = $(first_mon).nextAll();
    var original_len = days.length;
    $(first_mon).find(".day-td").addClass("co-blue");
    for (i = 0; i < days.length; i++) {
        if (Math.floor((i+1)/7)%2 == 0) {
            $(days[i]).find(".day-td").addClass("co-blue");
        }
        delete days[i];
    }

    }


$(".maybe, .yes, .no").click(function(){
  var shift_class = $(this).data("class");
  var id = $(".context").attr("id");
  var csrf = $('input[name ="csrfmiddlewaretoken"]').val();
  var url = $("#url").val() + "dodaj/";


 $.ajax({
    url: url,
    data: {
    "shift_class":shift_class,
    "id":id,
    "csrfmiddlewaretoken": csrf
  },
    type: 'post',
    cache: false,

    success:function(data){
      if (data.shift_class){
        $("#modal-choice").modal("hide");
        var element = $("#"+id);
        $(element).removeClass("y m a").addClass(data.shift_class);
        var time = $(element).data("time");
        $(element).html(data.username + " <small>"+ time +"</small>");
       $("#success").html("Zabeleženo");
       $("#success").show().delay(700).fadeOut();

    }
    else if (data.error){
       $("#error").html(data.error);
       $("#error").show().delay(2000).fadeOut();
    }
    },
    error: function(data){
      alert("Napaka. Preverite povezavo z internetom.");
      $(".img-form-btn").html('Shrani');
    }
  })



});
function isNotObsolete(id) {
  var clicked_date = new Date(id.replace( /(\d{2})-(\d{2})-(\d{4})/, "$2/$1/$3"))
  var last_current = $(".table-active").first().attr('id');
  var last_current_date = new Date(last_current.replace( /(\d{2})-(\d{2})-(\d{4})/, "$2/$1/$3"));
  if (last_current_date > clicked_date){
    return false
  }
  else {
    return true
  }
}
$(".shift").click(function(){
  var id = $(this).data("id");
  var date = $(this).parents(".date").find(".day-td").attr("id");
  if (isNotObsolete(date)){
  var group = $("#group").val();
  $(".context").attr("id", id);

          $.ajax({
            url: '/urniki/' + group +"/"+id+"/",
            datatype: 'json',
            type: 'GET',
            success: function(data) {
              statuses = JSON.parse(data.statuses);
              var context = "";
              for (i = 0 ; i < Object.values(statuses).length; i++) {
                user = Object.keys(statuses)[i];
                status = Object.values(statuses)[i];
                line = '<div class="w-50 mt-05 float-left ' + status + '-user status">'+ user+'</div>';
                var context = context + (line);
              }
              $(".load-statuses-container .load-statuses").html('<h6 class="text-center text-secondary">Zaposleni</h6>' + context);
              $(".n-user").css("background-color", "#DC3545");
              $(".m-user").css("background-color", "#f5c88a");
              $(".y-user").css("background-color", "#AFCFB7");

            }
        });
  $("#modal-choice").modal("show");
  }
});

$("#load-up").click(function(){
  var date = $(".day-td").first().attr("id");
  window.location = '?load_to=' + date;
});
$("#load-down").click(function(){
  var date = $(".day-td").last().attr("id");
  window.location = "?load_to=" + date + "&scroll=True";
});



$("#messages-submit").click(function(){
  var message = $("#messages-input").val();
  var group =$("#group").val();
  if (message != ""){
          $.ajax({
            url: '/urniki/' + group +"/message_add/",
            data:{
            "message": message,              
            },
            datatype: 'json',
            type: 'GET',
            success: function(data) {
              if (data.success){
                window.location.reload();
              }
              if (data.error){
                $("#error").html(data.error);
                $("#error").show().delay(2000).fadeOut();
              }

            }
        });
  }
});


$("#modal-edit-schedule").on("hidden.bs.modal", function () {
    $(".load-statuses-container .load-statuses").html("<small class='text-muted'>Nalaganje</small>");
});

$(".day-td").click(function(){
  var id = $(this).attr('id');
  if (isNotObsolete(id)){
  var date_nice = $(this).html();
  $(".modal-absent-title").html("Odsotnost na " + date_nice);
  $("#modal-absent").modal("show");
  $("#modal-absent").attr("data-day-id", id);
  $(".load-absents-container .load-absents").html("");

            var group = $("#group").val();
            $.ajax({
            url: '/urniki/' + group +"/urnik/absent/"+id+"/",
            datatype: 'json',
            type: 'GET',
            success: function(response) {
            var data = JSON.parse(response);
            var absents = data[1];
            if (data[0]==true){
                $("#absents-button").removeClass("no-absent yes-absent").addClass("yes-absent");
                $("#absents-button").html('<i class="far fa-check-circle" style="margin: 3vh;"></i>');
            }
            else {
                $("#absents-button").removeClass("no-absent yes-absent").addClass("no-absent");
                $("#absents-button").html('<i class="far fa-times-circle" style="margin: 3vh;"></i>');
            }

            var context = "";
            if (absents.length > 0) {
              for (i = 0 ; i < absents.length; i++) {
                 var line = '<div class="w-100 float-left bg-danger bt-1">'+ absents[i] +'</div>';
                 $(".load-absents-container .load-absents").append(line);
              }
              $(".load-absents-container .load-absents").prepend('<h6 class="text-center text-secondary">Odsotni</h6>');
              }

            }
        });
       }
});
$(".yes-absent, .no-absent").click(function(){
  var day_id = $("#modal-absent").attr("data-day-id");
  var day = $("#"+day_id);
  var group = $("#group").val();
  var url = "/urniki/"+group+"/urnik/absent/"
  var csrf = $('input[name ="csrfmiddlewaretoken"]').val();

 $.ajax({
    url: url,
    data: {
    "day_id": day_id,
    "csrfmiddlewaretoken": csrf
  },
    type: 'post',
    cache: false,

    success:function(data){
      $("#success").html("Zabele&zcaron;eno");
      $("#success").show().delay(700).fadeOut();

      $("#modal-absent").modal("hide");
      if (data){
      shifts = JSON.parse(data);
      days = $(day).nextAll();
      for (i = 0; i < shifts.length; i++) {
           var time = $(days[i]).data("time");
           $(days[i]).html(shifts[i][0] + " <small>"+ time +"</small>");
           $(days[i]).removeClass("y m a").addClass(shifts[i][1])
        }
    }
    },
    error: function(data){
      alert("Napaka. Preverite povezavo z internetom.");
    }
  })

});


$("#reset").click(function(){
window.location  = window.location.pathname;
});

$(".clickable").click(function(){
    var url = $(this).data("href");
    window.location.href = url;
});