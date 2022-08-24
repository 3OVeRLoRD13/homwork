function commentRplyToggle(parent_id){
    const row = document.getElementById(parent_id);
    const test = document.getElementById("test");

    if (row.classList.contains('d-none')){
        row.classList.remove('d-none')
    }else{
        row.classList.add('d-none')
    }

    if (test.classList.contains('d-none')){
        test.classList.remove('d-none')
    }else{
        test.classList.add('d-none')
    }
}
