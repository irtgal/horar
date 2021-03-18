var dates = $(".date");
var i;
for (i = 0; i < dates.length; i++) {
  var shifts = $(dates[i]).find(".shift");
  var span = Math.floor(12/shifts.length);
  if (0 < span && span < 13){
    $(shifts).attr("colspan", span);
  }
}
var in_turnusi = window.location.pathname.includes("turnusi");

/* handlanje errorjev */
$( document ).ready(function() {
let queries_all = new URLSearchParams(window.location.search);
let error = queries_all.get("error");
let success = queries_all.get("success");
if (error){
  $("#error").html(error);
  $("#error").show().delay(3000).fadeOut();

} else if (success){
  $("#success").html(success);
  $("#success").show().delay(3000).fadeOut();
}
});
/* administrator */
$(".delete-timetable").click(function(){
    $("#modal-confirm-title").html("Ali ste prepričani?");
    $("#modal-confirm").modal("show");
    var group = $("#group").val();
    var start = $(this).data("start");
    var end = $(this).data("end");
    $("#form-confirm").attr("action", "/administrator/"+group+"/timetable_delete");
    $("#start").val(start);
    $("#end").val(end);
  });

$(".url-timetable").click(function(){
  var url = $(this).parent("tr").data("url");
  window.location = url;
});

$("#timetable-add-button").click(function(){
  $("#timetable-add-modal").modal("show");
});

/* urejanje shifta */
$(".shift").click(function(){
    $("#shift-remove").css("display", "block");
    var group = $("#group").val();
    var employee = $(this).data("employee");
    var date = $(this).data("date");
    var start = $(this).data("start");
    var end = $(this).data("end");
    var id =$(this).data("id");
    var shift_class = $(this).data("class");
        $("#title-modal-edit-shift").html("Uredi " + date);
        $("#date").val(date);
        $("#edit-from").val(start);
        $("#edit-to").val(end);
        $("#id").val(id);
        $("option:selected").removeAttr("selected");
        $(".current-user").html(employee);
        $("#delete-shift").css("display", "block");
        if (!in_turnusi){
          $.ajax({
            url: '/urniki/'+group+'/'+id+'/',
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
              $(".load-statuses-container .load-statuses").html('<h6 class="text-center text-secondary">Ostali</h6>' + context);
              $(".n-user").css("background-color", "#DC3545");
              $(".m-user").css("background-color", "#f5c88a");
              $(".y-user").css("background-color", "#AFCFB7");

            }

        });
        }
    $("#modal-edit-shift").modal("show");
});
$("#modal-choice").on("hidden.bs.modal", function () {
    $(".load-statuses-container .load-statuses").html("<small class='text-muted'>Nalaganje</small>");
});
$(".day-td").click(function(){
  var date = $(this).attr("id");
  $(".load-statuses").html("");
  $("#date").val(date);
  $("#title-modal-edit-shift").html("Ustvari " + date);
  $("#edit-from").val("");
  $("#edit-to").val("");
  $("#id").val("");
  $("#modal-edit-shift").modal("show");
  $("#shift-remove").css("display", "none");
  if (in_turnusi){
    $("#modal-edit-shift").attr("action", "")
  }
  if (date && !in_turnusi) {
            var group = $("#group").val();
            $.ajax({
            url: '/urniki/' + group +"/urnik/absent/"+date+"/",
            datatype: 'json',
            type: 'GET',
            success: function(response) {
            var data = JSON.parse(response);
            var absents = data[1];
            var context = "";
            if (absents.length > 0) {
              $(".load-absents-container .load-absents").html('<h6 class="text-center text-secondary">Ne morejo</h6>');
              for (i = 0 ; i < absents.length; i++) {
                 var line = '<div class="w-100 float-left bg-danger bt-1">'+ absents[i] +'</div>';
                 $(".load-absents-container .load-absents").append(line);
              }
              }

            }
        });

  }

});
$("#modal-edit-shift").on("hidden.bs.modal", function () {
    $(".load-absents").html("");
});
$("#shift-remove").click(function(){
console.log(location.search);
  var url = $("#url").val() +"shift_remove/"+location.search;
  $("#form-edit-shift").attr("action", url);
  $("#form-edit-shift").submit();
});


/* izbira turnusa za zdelavo urnika */
$(".turnus-picker-el").click(function(){
  var id = $(this).data("id");
  $("#turnus-id").val(id);
  $("#turnus-picker-row").css("display", "none");
  $("#date-picker-row").css("display", "inline");

});


$("#load-up").click(function(){
  var date = $(".day-td").first().attr("id");
  window.location = '?load_to=' + date;
});
$("#load-down").click(function(){
  var date = $(".day-td").last().attr("id");
  window.location = "?load_to=" + date + "&scroll=True";
});

$("#user-add").click(function(){
  $("#modal-user-add").modal('show');
});

$("#toggle-messages").on("click", function () {
  let caret = $(this).find(".fas");
  let extra_messages = $("#messages-div > .alert").slice(3);
  if (caret.hasClass("fa-caret-down")) {
    caret.toggleClass('fa-caret-down fa-caret-up');
    $(extra_messages).removeClass("hidden");
  }
  else {
    caret.toggleClass('fa-caret-up fa-caret-down');
    $(extra_messages).addClass("hidden");
  }
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

            }
        });
  }
});

/* urnik prikaze samo current dni */
$("#reset").click(function(){
window.location  = window.location.pathname;
});

/* resetiraj modal za nov urnik */
$("#timetable-add-modal").on("hidden.bs.modal", function () {
    $("#turnus-picker-row").css("display", "block");
    $("#date-picker-row").css("display", "none");
});

/* izbriši uporabnika */
    $('.remove-user').bind('mouseenter', function() {
      $(this).html('<i class="fas fa-trash text-danger"></i>');
}).bind('mouseleave', function(){
  var user = $(this).data("user");
    $(this).html(user);
});
$(".remove-user").click(function(){
    var user = $(this).data("user");
    var id =$(this).data("id")
    $("#modal-confirm-title").html("Odstrani uporabnika: <b>"+user+"</b>");
    $("#modal-confirm").modal("show");
    var group = $("#group").val();
    $("#form-confirm").attr("action", "/administrator/"+group+"/user_remove")
    $("#employee").val(id);
});

$(".clickable").click(function(){
    var url = $(this).data("href");
    window.location.href = url;
});




