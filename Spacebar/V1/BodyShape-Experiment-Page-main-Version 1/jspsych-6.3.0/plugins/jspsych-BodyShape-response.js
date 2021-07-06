/*
 * Example plugin template
 */

jsPsych.plugins["BodyShape-response"] = (function() {

  var plugin = {};

  jsPsych.pluginAPI.registerPreload('NewResponse', 'stimulus', 'video');

  plugin.info = {
    name: 'BodyShape-response',
    description: '',
    parameters: {
      stimulus: {
        type: jsPsych.plugins.parameterType.VIDEO,
        pretty_name: 'Video',
        default: undefined,
        description: 'The video file to play.'
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
    }
  }

  plugin.trial = function(display_element, trial) {
    var video_html="<div>"
    video_html+= '<video id="jspsych-video-keyboard-response-stimulus"'
    video_html += ' width="'+trial.width+'"'
    video_html += ' height="'+trial.height+'"'
    video_html += ">"
    var video_preload_blob = jsPsych.pluginAPI.getVideoBuffer(trial.stimulus[0]);

    video_html += "</video>";
    video_html += "</div>";

    display_element.innerHTML = video_html

    var video_element = display_element.querySelector('#jspsych-video-keyboard-response-stimulus');

    video_element.src = video_preload_blob

    // data saving
    var trial_data = {
      parameter_name: 'parameter value'
    };

    // end trial
    jsPsych.finishTrial(trial_data);
  };

  return plugin;
})();
