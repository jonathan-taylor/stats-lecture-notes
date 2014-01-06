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
