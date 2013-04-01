$.getScript('/static/js/slide_meta.js');

console.log('none');
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
MathJax.Hub.Update();
console.log('mathjaxconfig')
