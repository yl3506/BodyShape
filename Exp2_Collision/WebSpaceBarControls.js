Qualtrics.SurveyEngine.addOnload(function()
{
});

Qualtrics.SurveyEngine.addOnReady(function()
{	
	var eventCounter=0
	var startTime=0
	var finishTime=0
	jQuery('body').keyup(function(e){
   		if(e.keyCode == 16 && eventCounter==0){
       		jQuery('video').trigger('play')
			startTime=e.timeStamp
			eventCounter++
			jQuery("#NextButton").hide()
		}else if(e.keyCode==16 && eventCounter==1){
			jQuery('video').trigger("pause")
			finishTime=e.timeStamp-startTime
			//alert("Time Lapse: "+finishTime)
			eventCounter++
			jQuery("#NextButton").show()
			Qualtrics.SurveyEngine.setEmbeddedData("Sample",finishTime)
			alert("Time Lapse:" + Qualtrics.SurveyEngine.getEmbeddedData("Sample"))
		}else if(e.keyCode==16 && eventCounter==2){
			alert("Please Proceed, You Can Only Watch the Video Once")
		}
		else{
		alert("Wrong Button")
		}
	})
	
	
});

Qualtrics.SurveyEngine.addOnUnload(function()
{
	this.enableNextButton()
	jQuery('body').off()
});