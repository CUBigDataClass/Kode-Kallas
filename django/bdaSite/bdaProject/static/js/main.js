function show(val, element, file) {
  //element = '#' + element;

  if (val == "") {
    //$(element).html("");
    document.getElementById(element).innerHTML = "";
    return;
  }
  else {
    if (window.XMLHttpRequest) {
      // code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp = new XMLHttpRequest();
    }
    else {
      // code for IE6, IE5
      xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function() {
      if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        //$(element).html(xmlhttp.responseText);
        document.getElementById(element).innerHTML = xmlhttp.responseText;
      }
    }
    xmlhttp.open("GET", file+"?q="+val, true);
    xmlhttp.send();
    return val;
    console.log(val+" "+element+" "+file);
  }
}
