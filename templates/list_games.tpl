<!doctype html>
<html>
  <head>
    <style>
      body{ font-family: sans-serif; }
      td{ padding: 0.25em; }
      a:visited{ color: blue; }
    </style>
    <script>
      window.onload = function(){
        alert('here');
      }
      var game_list = {{game_list}};
      //alert(game_list)
      //document.write(JSON.stringify(game_list));
      render_list(document.body, game_list);
      function elem(container, tag, props){
        var el = document.createElement(tag);
        for(var k in props){
          var val = props[k];
          if(k == 'style'){
            for(var k2 in val){
              el.style[k2] = val[k2]; }}
          else if(k == 'html'){
            el.innerHTML = val; }
          else if(k == 'text'){
            el.appendChild(document.createTextNode(val)); }
          else{
            el[k] = val; }}
        if(container) container.appendChild(el);
        return el;
      }
      function render_list(container, list){
        var table = elem(container, 'table');
        var tr = elem(table, 'tr');
        elem(tr, 'th', {text: 'Game Id'});
        elem(tr, 'th', {text: 'Game Type'});
        for(var i=0; i<list.length; ++i){
          var game = list[i];
          var tr = elem(table, 'tr');
          elem(tr, 'td', {text: game.id});
          elem(tr, 'td', {text: game.paradigm}); }
      }
    </script>
  </head>
  <body>
    <hr>
    <h1> List Games </h1>
    <table>
      <tr>
        <th> Game Type </th>
        <th> Sit </th>
        <th> Spectate </th>
      </tr>
    <table>
    {{game_list}}
    <hr>
  </body>
</html>
