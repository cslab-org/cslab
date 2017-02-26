var disp = document.getElementById('text-disp-div');
var tarea = document.getElementById('textarea-div');

tarea.addEventListener('input', function (evt) {
    disp.innerHTML = window.marked(tarea.innerText);
    window.renderMathInElement(disp);
});

// Button click handlers
icon_group.addEventListener('click', function(event){



}


