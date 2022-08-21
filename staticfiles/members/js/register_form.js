var RegisterChecker = document.getElementById('RegisterChecker_id');
var RegisterBtn = document.getElementById('RegisterBtn_id');
RegisterBtn.disabled = true;

RegisterChecker.onchange = function(){
    if(this.checked){
        RegisterBtn.disabled = false;
    } else {
        RegisterBtn.disabled = true;
    };
    
};
