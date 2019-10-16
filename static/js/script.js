function all_good(headertext,maintext) {
    return Swal.fire(headertext, maintext, "success")
}

function not_all_good(headertext,maintext) {
    return Swal.fire(headertext, maintext, "error")
}

function profile_form_validation_response() {
    if (document.ProfileForm.alert.value==1){       
        all_good("All Good", "Your profile update has been saved")
    }
    if (document.ProfileForm.alert.value==0){
        not_all_good("Oops!", "There was a problem with your profile update.")
    }
}

function edit_template_form_validation_response() {
    if (document.EditQuoteTemplateForm.alert.value==1){       
        all_good("All Good", "Your template update has been saved")
    }
    if (document.EditQuoteTemplateForm.alert.value==0){
        not_all_good("Oops!", "There was a problem with your template update.")
    }
}