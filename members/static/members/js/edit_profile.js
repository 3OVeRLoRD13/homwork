var EditProfileChecker = document.getElementById('profile_image-clear_id');
var SaveChangesBtn = document.getElementById('SaveChanges');

EditProfileChecker.onchange = function(){
    if(this.checked){
        SaveChangesBtn.disabled = true;
    } else {
        SaveChangesBtn.disabled = false;
    };
    
};
