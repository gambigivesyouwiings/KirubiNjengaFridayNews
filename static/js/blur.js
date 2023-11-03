const loadingText = document.querySelector('.loading-text')
const bgSection = document.querySelector('.blur')
let loading = 70
let interVal = setInterval(() => {
    loadingText.style.opacity = scale(loading,0,100,1,0)
    bgSection.style.filter = `blur(${scale(loading,0,100,30,0)}px)`
},50)
const scale = (num,in_min,in_max,out_min,out_max) => {
    return ( (num - in_min) * (out_max - out_min)) / (in_max - in_min) + out_min
}

// Progress Bar
//function update() {
//            var element = document.getElementById("myprogressBar");
//            var width = 1;
//            var identity = setInterval(scene, 10);
//            function scene() {
//            if (width >= 100) {
//                clearInterval(identity);
//            } else {
//                width++;
//                element.style.width = width + '%';
//                }
//            }
//        }

// Progress bar 2
document.getElementById("file-form").addEventListener("submit", function(event) {
  event.preventDefault();

  var files = document.getElementById("media").files;
  var formData = new FormData();

  for (var i = 0; i < files.length; i++) {
    formData.append("files[]", files[i]);
  }

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/upload", true);
  xhr.onload = function() {
    if (xhr.status === 200) {
      alert("Upload successful!");
    } else {
      alert("Error uploading files. Please try again.");
    }
  };

  xhr.upload.onprogress = function(event) {
    var progress = (event.loaded / event.total) * 100;
    document.getElementById("myprogressBar").style.width = progress + "%";
  };

  xhr.send(formData);
});