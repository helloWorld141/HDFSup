console.log("main.js loaded");
var file = document.getElementById("file");

var normalizeFileSize = function (filesize){
    dividend = filesize;
    rem = 0;
    unit = "B"
    if (filesize > 1024){
        dividend = filesize/1024;
        unit = "KB"
    }
    if (dividend > 1024){
        dividend = dividend/1024;
        unit = "MB"
    }
    if (dividend > 1024){
        dividend = dividend/1024;
        unit = "GB"
    }
    console.log(filesize);
    s_str = dividend.toFixed(2) + " " + unit;
    console.log(s_str);
    return s_str;
}

file.addEventListener(
    "change",
    function(event){
        filesize = file.files[0].size;
        $("#filesize").html(normalizeFileSize(filesize));
    },
    false
);
$("button#upload").click(function(){
    $("#progress-wrp").css("visibility", "visible");
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

    progressHandling(event){
        console.log("in progress handling")
        var percent = 0;
        var position = event.loaded || event.position;
        var total = event.total;
        var progress_bar_id = "#progress-wrp";
        if (event.lengthComputable) {
            percent = Math.ceil(position / total * 100);
        }
        // update progressbars classes so it fits your code
        $(progress_bar_id + " .progress-bar").css("width", +percent + "%");
        $(progress_bar_id + " .status").text(percent + "%");
    }

    doUpload(){
        console.log("javascript 6 yayyy");
        var formData = new FormData();
        // key value for post data
        formData.append("file", this._file, this.name);
        formData.append("upload_file", true);
        // call post endpoint to upload file
        self = this;
        console.log("this is doUpload")
        console.log(this)
        $.ajax({
            type: "POST",
            url: "/upload",
            xhr: function () {
                var myXhr = $.ajaxSettings.xhr();
                if (myXhr.upload) {
                    myXhr.upload.addEventListener(
                        'progress', 
                        self.progressHandling.bind(this)
                        , false
                    );
                }
                return myXhr;
            },
            success: function(response){
                // callback with http reponses
                console.log(response);
                console.log($("#status"));
                $("#status").html(response);

            },
            error: function(error) {
                // error handling 
                console.log(error.statusText);
            },
            async: true,
            processData: false,
            data: formData,
            contentType: false, // "multipart/form-data", // disable content-type header
            timeout: 36000//00 // for uploading large file - may take up to hours
        });

    }
}
