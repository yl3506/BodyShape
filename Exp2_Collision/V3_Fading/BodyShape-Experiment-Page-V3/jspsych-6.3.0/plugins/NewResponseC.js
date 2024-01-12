/**
 * Body-Shape Curtain Collision Experiment Plugin
 * Modified from jsPsych-keyboard-response.js
 * YingQiao Wang
 *
 **/

 jsPsych.plugins["NewResponseC"] = (function() {

    var plugin = {};
  
    jsPsych.pluginAPI.registerPreload('NewResponseC', 'stimulus', 'video');
  
    plugin.info = {
      name: 'NewResponseC',
      description: '',
      parameters: {
        stimulus: {
          type: jsPsych.plugins.parameterType.VIDEO,
          pretty_name: 'Video',
          default: undefined,
          description: 'The video file to play.'
        },
        choices: {
          type: jsPsych.plugins.parameterType.KEY,
          pretty_name: 'Choices',
          array: true,
          default: jsPsych.ALL_KEYS,
          description: 'The keys the subject is allowed to press to respond to the stimulus.'
        },
        prompt: {
          type: jsPsych.plugins.parameterType.STRING,
          pretty_name: 'Prompt',
          default: null,
          description: 'Any content here will be displayed below the stimulus.'
        },
        width: {
          type: jsPsych.plugins.parameterType.INT,
          pretty_name: 'Width',
          default: '',
          description: 'The width of the video in pixels.'
        },
        height: {
          type: jsPsych.plugins.parameterType.INT,
          pretty_name: 'Height',
          default: '',
          description: 'The height of the video display in pixels.'
        },
        autoplay: {
          type: jsPsych.plugins.parameterType.BOOL,
          pretty_name: 'Autoplay',
          default: true,
          description: 'If true, the video will begin playing as soon as it has loaded.'
        },
        controls: {
          type: jsPsych.plugins.parameterType.BOOL,
          pretty_name: 'Controls',
          default: false,
          description: 'If true, the subject will be able to pause the video or move the playback to any point in the video.'
        },
        start: {
          type: jsPsych.plugins.parameterType.FLOAT,
          pretty_name: 'Start',
          default: null,
          description: 'Time to start the clip.'
        },
        stop: {
          type: jsPsych.plugins.parameterType.FLOAT,
          pretty_name: 'Stop',
          default: null,
          description: 'Time to stop the clip.'
        },
        rate: {
          type: jsPsych.plugins.parameterType.FLOAT,
          pretty_name: 'Rate',
          default: 1,
          description: 'The playback rate of the video. 1 is normal, <1 is slower, >1 is faster.'
        },

        trialNumber : {
          type : jsPsych.plugins.parameterType.INT,
          pretty_name : "trialNumber",
          default: 1,
          description: 'asdfa'

        },

        totalNumber : {
          type : jsPsych.plugins.parameterType.INT,
          pretty_name : "totalNumber",
          default: 1,
          description: 'asdfa'

        },

      }
    }
  
    plugin.trial = function(display_element, trial) {
  
      // setup stimulus
      var video_html = '<div>'+"<p>Video: " + String(jsPsych.pluginAPI.getCurrentTrial())+"/"+String(22)+"</p>"+"</div>"
      video_html += '<div><video id="jspsych-video-keyboard-response-stimulus"';
  
      if(trial.width) {
        video_html += ' width="'+trial.width+'"';
      }
      if(trial.height) {
        video_html += ' height="'+trial.height+'"';
      }
      if(trial.autoplay & (trial.start == null)){
        // if autoplay is true and the start time is specified, then the video will start automatically
        // via the play() method, rather than the autoplay attribute, to prevent showing the first frame
        video_html += " autoplay ";
      }
      if(trial.controls){
        video_html +=" controls ";
      }
      if (trial.start !== null) {
        // hide video element when page loads if the start time is specified, 
        // to prevent the video element from showing the first frame
        video_html += ' style="visibility: hidden;"'; 
      }
      video_html +=">";
  
      var video_preload_blob = jsPsych.pluginAPI.getVideoBuffer(trial.stimulus[0]);
      if(!video_preload_blob) {
        for(var i=0; i<trial.stimulus.length; i++){
          var file_name = trial.stimulus[i];
          if(file_name.indexOf('?') > -1){
            file_name = file_name.substring(0, file_name.indexOf('?'));
          }
          var type = file_name.substr(file_name.lastIndexOf('.') + 1);
          type = type.toLowerCase();
          if (type == "mov") {
            console.warn('Warning: video-keyboard-response plugin does not reliably support .mov files.')
          }
          video_html+='<source src="' + file_name + '" type="video/'+type+'">';   
        }
      }

      video_html += "</video>";
      video_html += "</div>";
  
      // add prompt if there is one
      if (trial.prompt !== null) {
        video_html += trial.prompt;
      }
  
      display_element.innerHTML = video_html;
  
      var video_element = display_element.querySelector('#jspsych-video-keyboard-response-stimulus');
  
      if(video_preload_blob){
        video_element.src = video_preload_blob;
      }
      
      video_element.playbackRate = trial.rate;
  
      // store response
      var response = {
        rt: null,
        key: null
      };
  
      // function to end trial when it is time
      function end_trial() {
  
        // kill any remaining setTimeout handlers
        jsPsych.pluginAPI.clearAllTimeouts();
  
        // kill keyboard listeners
        jsPsych.pluginAPI.cancelAllKeyboardResponses();
        
        // stop the video file if it is playing
        // remove end event listeners if they exist
        video_element.pause()
        display_element.querySelector('#jspsych-video-keyboard-response-stimulus').onended = function(){ };
  
        // gather the data to store for the trial
        var trial_data = {
          rt: responseTime,
          stimulus: trial.stimulus[0],
          response: response.key
        };
  
        // clear the display
        display_element.innerHTML = '';
  
        // move on to the next trial
        jsPsych.finishTrial(trial_data);
      }
      
      var played=0
      var startingTime=0
      var endingTime=0
      var responseTime=0

      // function to handle responses by the subject
      var after_response = function(info) {
        // after a valid response, the stimulus will have the CSS class 'responded'
        // which can be used to provide visual feedback that a response was recorded;
        // only record the first response
        if (info.key == " " && played == 0){
          startingTime=info.rt,
          video_element.play(),
          played = played+1
        }
        

        else if (info.key == " " && played == 1){
          endingTime=info.rt,
          video_element.pause(),
          responseTime=(endingTime-startingTime),
          played = played+1
        }

        if (played == 2){
          end_trial()
        }
      };
  
      // start the response listener
      
      var keyboardListener = jsPsych.pluginAPI.getKeyboardResponse({
          callback_function: after_response,
          valid_responses: trial.choices,
          rt_method: 'performance',
          persist: true,
          allow_held_key: false,
        });


    };
  
    return plugin;
  })();
