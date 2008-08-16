
    function toggleVisible(elem) {
        toggleElementClass("invisible", elem);
    }

    function makeVisible(elem) {
        removeElementClass(elem, "invisible");
    }

    function makeInvisible(elem) {
        addElementClass(elem, "invisible");
    }

    function isVisible(elem) {
        // you may also want to check for
        // getElement(elem).style.display == "none"
        return !hasElementClass(elem, "invisible");
    };


function flip() {
  makeVisible("back");
  }

function keyup(ev) {
  if (isVisible("back")) {
    if (ev.key().string == "KEY_Y" || ev.key().string == "KEY_SPACEBAR") {
      right();
    }
    if (ev.key().string == "KEY_N") {
      wrong();
    }

  } else {
    if (ev.key().string == "KEY_F" || ev.key().string == "KEY_SPACEBAR") {
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
  $("right").value = right;
  $("testform").submit();
}

function testInit() {
  connect(document,"onkeyup",keyup);
  }

addLoadEvent(testInit);
