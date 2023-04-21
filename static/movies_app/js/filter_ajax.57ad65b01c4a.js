// _______________________request-test
    // fetch('http://127.0.0.1:8000/xhr_request/', {
    //     method: 'GET',
    //     headers: {
    //         'Content-Type': 'application/json',
    //     },
    // })
    //     .then(response => response.json())
    //     // .then(alert('json has been parsed'))
    //     .catch(error => console.error(error))
// ______________________________________________

let div = document.querySelector('.left-ads-display.col-lg-9 .row');

function ajaxSend(url, params) {
    
    $.ajax({
        type        : 'GET', // define the type of HTTP verb we want to use (POST for our form)
        url         : url, // the url where we want to POST
        data : $("form[name=filter_ajax]").serialize(),
         success     :   function (response) {

            
            //alert('yes, the get-request was send with ajax');
            div.innerHTML=response.movies;
            
            
        
    }    
})
}

//__________________________ фільтр за допомогою аякс. Віключено тому,що  form[name=filter_ajax] з html виключеною. але робочий
// let forms = document.querySelector('form[name=filter_ajax]');

// forms.addEventListener('submit', function(event){
//     event.preventDefault();
//     let url = forms.action;
//     let params = new URLSearchParams(new FormData(this)).toString();
    
//     console.log(`${url}?${params}`);


//     //URLSearchParams is an object to handle with url, one can get it and change, приймає рядок
    

//     //FormData об'єкт який забезпечує можливість легко побудувати набір пар ключ/значення, які представляють поля форми і їх значення, і потім можуть бути відправлені запитом методом POST.
    

//     // toString() метод об'єкта URLSearchParams який повертає рядок з повною URL адресою.
//     //Метод використовується коли необхідно об'єкт URLSearchParams представити як рядок.
    
//     ajaxSend(url, params);
// })
// _________________________________________________


// _____________________________________request-test
//getting from xhr-request
let requestURL = 'http://127.0.0.1:8000/xhr_request/';
let xhr = new XMLHttpRequest;
xhr.open('GET',requestURL)
xhr.onload = ()=>{
    // alert('yes, the get-request was send with xhr');    
    var instance = JSON.parse(xhr.response);
    console.log(instance, '68///', typeof(instance));

    
}
xhr.send()
// ______________________________________



// _________________________request-test 
// getting from fetch request
fetch(requestURL).then((response) => {
    
    return (response.json())
}).then((instance)=>{
    // alert('yes, the get-request was send with fetch');
    console.log(instance)});
// _________________________________________________


// мало б перекластися
// let c = function(){alert(gettext('Український JS'))}
// c()



