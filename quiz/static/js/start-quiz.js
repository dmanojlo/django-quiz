// django url tags ("{% url "quiz:choose_quiz" %}") wont work beacuse it is external js. Only works will in internal js

$(document).ready(function() {

   var count = 1;
   var score = 0;
   var num_of_questions = num_of_q
   $('#container').on('click', '.ans', function() {
     var myVar = document.getElementById("myVar").value;
     $('.bounce-in').delay(200).fadeTo(500, 0);
     var a = $(this).attr('answer');
     if(a!==myVar){
         $(this).addClass('worngans');
     }
     else{
       $(this).addClass('correct-answer');
       score++;
     }

     $( ".fade-in" ).delay(800).animate({
       opacity: "0",
       right: "+100%"
     }, 500, function() {
       // Animation complete.
     });
     setTimeout(function () {
       var form = $('#ajax-test-form');
       form.submit(function(e) {
           // prevent form submission
           e.preventDefault();
           // submit the form via Ajax
           $.ajax({
               url: form.attr('action'),
               type: form.attr('method'),
               dataType: 'json',
               data: form.serialize(),
               success: function(data) {
                   // Inject the result in the HTML
                   //window.location = data.url  django url redirect in ajax success
                   if (data.form_is_valid) {
                       count++;
                       $('#container').load(data.url + ' #container', function(){ $('.num').html(count.toString()); });


                   }
                   else {
                     $('.card-header').empty();
                     if (score < Math.floor(num_of_questions/2)){
                        $('.card-header').html("<h3>" + "Go read a book! Your miserable score is " + score.toString() + "/" + num_of_questions.toString() + "</h3>").fadeIn("slow");
                     }
                     else{
                         $('.card-header').html("<h3>" + "Unbelivable. Your little brain got " + score.toString() + "/" + num_of_questions.toString() + "</h3>").fadeIn("slow");
                     }
                     // $('.card-header').html("<h3>" + "Your score is " + score.toString() + "</h3>").fadeIn("slow");
                     $('.fade-in').empty();
                     $('.fade-in').html('<div class="about"><div class="about-text"><a class="btn btn-start" href="">Play Again</a><a class="btn btn-start"  href="/choose_quiz/">Choose Quiz</a></div></div>').css({"opacity":"1", "text-align": "center", "right":""}).fadeIn("slow");
                     $(".bounce-in").animate({
                   opacity: "1",
                 }, 1000, function() {
                   // Animation complete.
                 });
                   }

               }
           });
       });
       $('#ajax-test-form').submit();
     }, 1500);

});

});
