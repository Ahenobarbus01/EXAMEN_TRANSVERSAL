$(document).ready(function() {

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200) {
            document.getElementById('pie-de-pagina').outerHTML 
                = this.responseText;
        }
    };
    xhttp.open('GET', 'footer.html',true);
    xhttp.send();

});