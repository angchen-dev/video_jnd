import * as $ from 'jquery';

export const sendMsg = (data) => {
    return new Promise((resolve,reject)=>{
        $.ajax({
            type: 'POST',
            url: "http://127.0.0.1:8000/scheduler",
            data: JSON.stringify(data),
            contentType: 'application/json; charset=UTF-8',
            dataType: 'json', 
        }).done((response) => {
            console.log(response)
            resolve(response);
        }).fail((err) => {
            resolve(err);
        });
    });
}