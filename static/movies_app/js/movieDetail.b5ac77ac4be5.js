// ==================rate the movie===================
let rating_form = document.querySelector('form[name=rating]');
rating_form.addEventListener('change', function () {
    let data = new FormData(this);
    fetch(`${this.action}`, {
        method: 'POST',
        body: data
    }).then(alert('well'))
        .catch(error => alert('153 some error'))

})
// ==================///rate the movie===================



// ===============================new form to react to the existing comments
function reactCommentMptt(parent_id) {
    parent = document.getElementById(parent_id);
    removeReviewFormMpttNew()

review_form_new ='<div style="text-align: center; width: 80%; margin: 0 auto;">\
    <form action="' + review_form_mptt.action + '" method="post" id="review_form_mptt_new">' + csrf_new_form_mptt.innerHTML + '<input type="hidden" name="parent" id="' + parent_id + '" value="' + parent_id + '">\
       <div class="row">\
         <div class="col-md-6">\
            <div id="div_id_name" class="mb-3">\
                 <label for="id_name" class="form-label requiredField">\
                User<span class="asteriskField">*</span>\
            </label>\
         <input type="text" name="name" maxlength="100" class="textinput form-control" required="" id="id_name"></div>\
    </div>\
            <div class="col-md-6">\
                <div id="div_id_email" class="mb-3">\
        <label for="id_email" class="form-label requiredField">\
                Email<span class="asteriskField">*</span> </label>                        <input type="email" name="email" maxlength="254" class="emailinput form-control" required="" id="id_email">    </div>\
</div>        </div>        <div>    <div id="div_id_text" class="mb-3">\
                 <label for="id_text" class="form-label requiredField">\
                Message<span class="asteriskField">*</span>\
            </label>\
            <textarea name="text" cols="40" rows="5" maxlength="5000" class="textarea form-control" required="" id="id_text"></textarea>\
    </div>\
    </div>\
        <div class="validationCheck"></div>\
        <button class="btn btn-info btn-rounded" type="submit">Add comment</button>\
    </form>\
</div>'

    parent.insertAdjacentHTML('beforeend', review_form_new)
    review_form_mptt_new.addEventListener('submit', formCheck)
}
// ===============================///new form to react to the existing comments

    
// ================================================aadding review sending the review form from block content and getting JsonResponse
let formCheck = function (e) {
    e.preventDefault()
    let data = new FormData(this);
    fetch(`${this.action}`, {
        method: 'POST',
        body: data
    }).then(response => response.json())
        .then(data => {
            if (data.status == 'success') {
                this.reset();
                removeReviewFormMpttNew();
                let respond = '<li> <div class="comment alert alert-info" id="' + data.new_review_id + '">\
                <h3>' + data.name + '</h3>\
                <h4>' + data.created_at + '</h4>\
                <p>' + data.text + '</p>  </div>\
                <a href="#review_form_mptt_new" onclick="reactCommentMptt('+ data.new_review_id + ')">Відреагувати</a> </li>'

                let respondWithParent = '<ul class="children pl-2 pl-md-5" style="list-style: None;">' + respond + '</ul>';
                // let parent0Review = review;

                if (data.parent_review_id != '') {
                    parent = document.getElementById(data.parent_review_id);
                    parent.nextElementSibling.insertAdjacentHTML('afterend', respondWithParent);
                } else {
                    document.getElementById('recursetree').insertAdjacentHTML('afterbegin', respond)
                }
            }
        })
        .catch(error => alert(error))
}
function removeReviewFormMpttNew() {
    if (document.getElementById('review_form_mptt_new')) {
        review_form_mptt_new.remove()
    }
}    
// ================================================///aadding review
    // sending the review form from block content and getting JsonResponse

review_form_mptt.addEventListener('submit', formCheck)