$.getScript('/static/js/slide_meta.js');
$.getScript('/static/js/exercise.js');

MathJax.Hub.Config({
                        TeX: {
			   equationNumbers : { autoNumber: "AMS"},
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


console.log('loading header');
$.get('/static/tex/header.tex', function(data) {
	var newdiv = $('<div id="mathjaxheader"/>');
	console.log('Mathjax header load was performed.');
	$('body').append(newdiv);
	$('#mathjaxheader').text("$$ " + data + " $$");
	MathJax.Hub.Queue(['Typeset', MathJax.Hub, 'mathjaxheader']);
    });
MathJax.Hub.Update();

// console.log('loading header from web');
// $.get('http://www.stanford.edu/class/stats306b/header.tex', function(data) {
// 	console.log(data);
// 	var newdiv = $('<div id="mathjaxheaderweb"/>');
// 	console.log('loading header from web successful');
// 	$('body').append(newdiv);
// 	$('#mathjaxheaderweb').text("$$ " + data + " $$");
// 	MathJax.Hub.Queue(['Typeset', MathJax.Hub, 'mathjaxheaderweb']);
//     });
// MathJax.Hub.Update();

