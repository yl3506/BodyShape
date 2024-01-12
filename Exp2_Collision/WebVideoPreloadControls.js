Qualtrics.SurveyEngine.addOnload(function()
{

	var xhr = new XMLHttpRequest()
  xhr.open("GET", "https://harvard.az1.qualtrics.com/CP/File.php?F=F_brBLQCnZYff1bdI", true)
  xhr.responseType = "blob"
 video=document.getElementById("video1")

  xhr.addEventListener("load", function () {
    if (xhr.status === 200) {
      var URL = window.URL || window.webkitURL
      var blob_url = URL.createObjectURL(xhr.response);
	  video.src=blob_url
	}})
					   
  var prev_pc = 0
  xhr.addEventListener("progress", function(event) {
    if (event.lengthComputable) {
		
      var pc = Math.round((event.loaded / event.total) * 100)
	  
      if (pc != prev_pc) {
        prev_pc = pc
        progress_callback(pc)
      }
    }
  })
  
  xhr.send()
	
});