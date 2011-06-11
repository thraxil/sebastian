var flipped = false;

function flip() {
  jQuery("#back").show();
  flipped = true;
}

var Y = 89;
var N = 78;
var SPACE = 32;

function keyup_handler(ev) {
  if (flipped) {
     if (ev.keyCode == Y || ev.keyCode == SPACE) {
       right();
     }
     if (ev.keyCode == N) {
       wrong();
     }

   } else {
     if (ev.keyCode == SPACE) {
       flip();
     }
   }
}

function  right() {
   submitForm("yes");
}

function wrong() {
   submitForm("no");
}

function submitForm(right) {
  jQuery("#right").val(right);
  jQuery("#testform").submit();
}


