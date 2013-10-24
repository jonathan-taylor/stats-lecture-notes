//----------------------------------------------------------------------------
//  Copyright (C) 2012  The IPython Development Team
//
//  Distributed under the terms of the BSD License.  The full license is in
//  the file COPYING, distributed as part of this software.
//----------------------------------------------------------------------------

//============================================================================
// CellToolbar Example
//============================================================================

/**
 * Example Use for the CellToolbar library
 * add the following to your custom.js to load
 * Celltoolbar UI for slideshow
 *
 * ```
 * $.getScript('/static/js/celltoolbarpresets/example.js');
 * ```
 */
 // IIFE without asignement, we don't modifiy the IPython namespace

(function (IPython) {
    "use strict";

    var CellToolbar = IPython.CellToolbar;

    var exercise_preset = [];

    var checkbox_solution = CellToolbar.utils.checkbox_ui_generator('Solution?',
         // setter
         function(cell, value){
             // we check that the slideshow namespace exist and create it if needed
             if (cell.metadata.exercise == undefined){cell.metadata.exercise = {}}
             // set the value
             cell.metadata.exercise.solution = value
								  },
         //geter
         function(cell){ var ns = cell.metadata.exercise;
             // if the slideshow namespace does not exist return `undefined`
             // (will be interpreted as `false` by checkbox) otherwise
             // return the value
			 return (ns == undefined)? undefined: ns.solution
             }
    );

    CellToolbar.register_callback('exercise.solutionbox',checkbox_solution);
    exercise_preset.push('exercise.solutionbox');

    var checkbox_output = CellToolbar.utils.checkbox_ui_generator('Output?',
         // setter
         function(cell, value){
             // we check that the slideshow namespace exist and create it if needed
             if (cell.metadata.exercise == undefined){cell.metadata.exercise = {}}
             // set the value
             cell.metadata.exercise.output = value
								  },
         //geter
         function(cell){ var ns = cell.metadata.exercise;
             // if the slideshow namespace does not exist return `undefined`
             // (will be interpreted as `false` by checkbox) otherwise
             // return the value
			 return (ns == undefined)? undefined: ns.output
             }
    );

    CellToolbar.register_callback('exercise.outputbox',checkbox_output);
    exercise_preset.push('exercise.outputbox');

    var checkbox_start = CellToolbar.utils.checkbox_ui_generator('Start?',
         // setter
         function(cell, value){
             // we check that the slideshow namespace exist and create it if needed
             if (cell.metadata.exercise == undefined){cell.metadata.exercise = {}}
             // set the value
             cell.metadata.exercise.start = value
								  },
         //geter
         function(cell){ var ns = cell.metadata.exercise;
             // if the slideshow namespace does not exist return `undefined`
             // (will be interpreted as `false` by checkbox) otherwise
             // return the value
			 return (ns == undefined)? undefined: ns.start
             }
    );

    CellToolbar.register_callback('exercise.startbox',checkbox_start);
    exercise_preset.push('exercise.startbox');

    var checkbox_input = CellToolbar.utils.checkbox_ui_generator('Input?',
         // setter
         function(cell, value){
             // we check that the slideshow namespace exist and create it if needed
             if (cell.metadata.exercise == undefined){cell.metadata.exercise = {}}
             // set the value
             cell.metadata.exercise.input = value
             },
         //geter
         function(cell){ var ns = cell.metadata.exercise;
             // if the slideshow namespace does not exist return `undefined`
             // (will be interpreted as `false` by checkbox) otherwise
             // return the value
			 return (ns == undefined)? undefined: ns.input
             }
    );

    CellToolbar.register_callback('exercise.inputbox',checkbox_input);
    exercise_preset.push('exercise.inputbox');

    CellToolbar.register_preset('Exercise',exercise_preset);
    console.log('Exercise extension for metadata editing loaded.');


}(IPython));
