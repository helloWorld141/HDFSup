console.log("main.js loaded");
var file = document.getElementById("file");
$("button#upload").click(function(){
    var myfile = file.files[0]
    if (myfile === undefined)
        alert("Please choose a file");
    else {
        console.log("Uploading file " + myfile.name);
        var upload = new Upload(myfile);
        // maybe perform check size and check type here
        upload.doUpload();
        console.log(upload.name);
        console.log(upload.size);
        console.log(upload.type);
    }
});

class Upload{
    constructor(file){
        this._file = file;
    }

    get name(){
        return this._file.name;
    }

    get size(){
        return this._file.size;
    }
    get type(){
        return this._file.type;
    }

    doUpload(){
        console.log("javascript 6 yayyy");
        var formData = new FormData();
        // key value for post data
        formData.append("file", this._file, this.name);
        formData.append("upload_file", true);
        // call post endpoint to upload file
        $.ajax({
            type: "POST",
            url: "/upload",
            // xhr: function(){
            //     // to update progress bar
            //     console.log("hello")
            // },
            success: function(response){
                // callback with http reponses
                console.log(response);
            },
            error: function(error) {
                // error handling 
                console.log(error);
            },
            async: true,
            processData: false,
            data: formData,
            contentType: false, // "multipart/form-data", // disable content-type header
            timeout: 36000//00 // for uploading large file - may take up to hours
        });

    }
}
