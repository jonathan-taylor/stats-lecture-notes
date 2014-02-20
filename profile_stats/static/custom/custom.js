// we want strict javascript that fails
// on ambiguous syntax
"using strict";

console.log('loading slide meta');
$.getScript('/static/js/slide_meta.js');
console.log('loading exercise');
$.getScript('/static/js/exercise.js');

MathJax.Hub.Config({
    TeX: {
        equationNumbers : {autoNumber: "AMS"},
    extensions: ["AMSmath.js", "AMSsymbols.js", "autobold.js"],
    },
    tex2jax: {
        inlineMath: [ ['$','$'], ["\\(","\\)"] ],
    displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
    },
    displayIndent: "10em",
    displayAlign: 'center',
    "HTML-CSS": {
        styles: {'.MathJax_Display': {"margin": 4}}
    }
});

console.log('loading MathJax tex header');
$.get('/static/tex/header.tex', function(data) {
    var newdiv = $('<div id="mathjaxheader"/>');
    console.log('Mathjax header load was performed.');
    $('body').append(newdiv);
    $('#mathjaxheader').text("$$ " + data + " $$");
    MathJax.Hub.Queue(['Typeset', MathJax.Hub, 'mathjaxheader']);
});
MathJax.Hub.Update();


// do not use notebook loaded  event as it is re-triggerd on
// revert to checkpoint but this allow extesnsion to be loaded
// late enough to work.
//

$([IPython.events]).on('app_initialized.NotebookApp', function(){


	/**  Use path to js file relative to /static/ dir without leading slash, or
	 *  js extension.
	 *  Link directly to file is js extension.
	 *
	 *  first argument of require is a **list** that can contains several modules if needed.
	 **/

	// require(['custom/noscroll']);
	// require(['custom/clean_start'])
	// require(['custom/toggle_all_line_number'])
	// require(['custom/gist_it']);

	/**
	 *  Link to entrypoint if extesnsion is a folder.
	 *  to be consistent with commonjs module, the entrypoint is main.js
	 *  here youcan also trigger a custom function on load that will do extra
	 *  action with the module if needed
	 **/
	require(['custom/slidemode/main'],function(slidemode){
		//     // do stuff
	    })

});