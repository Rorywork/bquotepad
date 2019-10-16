function all_good(headertext,maintext) {
    return Swal.fire(headertext, maintext, "success")
}

function not_all_good(headertext,maintext) {
    return Swal.fire(headertext, maintext, "error")
}