/**
 * jspsych-same-different
 * Josh de Leeuw
 *
 * plugin for showing two stimuli sequentially and getting a same / different judgment
 *
 * documentation: docs.jspsych.org
 *
 */

jsPsych.plugins['automaticPage'] = (function() {

  var plugin = {};

  plugin.info = {
    name: 'automaticPage',
    description: '',
    parameters: {
      stimuli: {
        type: jsPsych.plugins.parameterType.HTML_STRING,
        pretty_name: 'Stimuli',
        default: undefined,
        array: true,
        description: 'The HTML content to be displayed.'
      },
      first_stim_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'First stimulus duration',
        default: null,
        description: 'How long to show the first stimulus for in milliseconds. If null, then the stimulus will remain on the screen until any keypress is made.'
      },
      gap_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Gap duration',
        default: 500,
        description: 'How long to show a blank screen in between the two stimuli.'
      },
      second_stim_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Second stimulus duration',
        default: null,
        description: 'How long to show the second stimulus for in milliseconds. If null, then the stimulus will remain on the screen until a valid response is made.'
      },
      prompt: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Prompt',
        default: null,
        description: 'Any content here will be displayed below the stimulus.'
      }
    }
  }

  plugin.trial = function(display_element, trial) {

    display_element.innerHTML = '<div class="jspsych-same-different-stimulus">'+trial.stimuli[0]+'</div>';

    var after_response = function() {

      // kill any remaining setTimeout handlers
      jsPsych.pluginAPI.clearAllTimeouts();

      display_element.innerHTML = '';

      jsPsych.finishTrial();
    }

    if (trial.first_stim_duration > 0) {
      jsPsych.pluginAPI.setTimeout(function() {
        after_response();
      }, trial.first_stim_duration);
    } 


    function showSecondStim() {

      var html = '<div class="jspsych-same-different-stimulus">'+trial.stimuli[1]+'</div>';
      //show prompt here
      if (trial.prompt !== null) {
        html += trial.prompt;
      }
      display_element.innerHTML = html;

      if (trial.second_stim_duration > 0) {
        jsPsych.pluginAPI.setTimeout(function() {
          after_response();
        }, trial.second_stim_duration);
      }

    }

  };

  return plugin;
})();
