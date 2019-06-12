$(document).ready(function() {
    $('#bookTable').dataTable();
    $('#transTable').dataTable();
    $('#searchTable').dataTable();

    $(".btn-danger").click(function() {
        var conf = confirm("Do you want to remove this item?");
        if(conf == true)
        {
            sendDataRemove(this.id);
            alert("Book Removed!");
            window.location.reload(true);
            //event.preventDefault();
        }
    });

    $(".btn-success").click(function() {
        sendDataAdd(this.id);
        alert("Book Added.Visit library to view added books!!");
        window.location.reload();
        //event.preventDefault();
    });

    $("#imageUpload").click(function() {
        //readURL(this);
        getUrl();
        // var img = $('#imagePreview').css('background-image');
        // img = img.replace(/(url\(|\)|")/g, '');
        // $.ajax({
        //     url: '/update_profile',
        //     type: 'POST',
        //     contentType: 'application/json',
        //     data: JSON.stringify({
        //         img_src: img
        //     }),
        //     dataType: 'json'
        // });
    });

    $("#btnDelete").click(function() {
        var conf = confirm("Do you want to delete your account?");
        if(conf == true)
        {
            sendDataDelete();
            window.location.reload();
        }
    });

});

function getUrl() {
var url = prompt('Enter image URL');

if (url) { // Do string and URL validation here and also for image type
        $('#imagePreview').css('background-image', 'url('+url +')');
        $('#imagePreview').hide();
        $('#imagePreview').fadeIn(650);
        sendDataImg(url);
    }
}

// function readURL(input) {
//     if (input.files && input.files[0]) {
//         var reader = new FileReader();
//         reader.onload = function(e) {
//             $('#imagePreview').css('background-image', 'url('+e.target.result +')');
//             $('#imagePreview').hide();
//             $('#imagePreview').fadeIn(650);
//         }
//         reader.readAsDataURL(input.files[0]);
//     }
// }


function sendDataRemove(param) {
    $.ajax({
        url: '/removeItem',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            book_id: param,
        }),
        dataType: 'json'
    });
}


function sendDataAdd(param) {
    $.ajax({
        url: '/addItem',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            book_id: param,
        }),
        dataType: 'json'
    });
}

function sendDataDelete() {
    $.ajax({
        url: '/delete_account',
        type: 'POST'
    });
}

function sendDataImg(param){
    $.ajax({
        url: '/update_profile',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            img_src: param,
        }),
        dataType: 'json'
    });
}
