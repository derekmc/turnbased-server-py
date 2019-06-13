<!doctype html>
<html>
  <head>
    <style>
      body{ font-family: sans-serif; }
      td{
        padding: 0.25em;
        text-align: center; }
      tr:nth-child(even){
         background: #d0e8ff; }
      th{ background: #014; color: #fff; padding: 0.8em; font-weight: normal; }
      table{
        border-spacing: 0; }
      a:visited{ color: blue; }
    </style>
    <script>
      window.onload = function(){
        render_list(document.getElementById("main"), game_list);
      }
      var game_list = {{!game_list}};
      //alert(game_list)
      //document.write(JSON.stringify(game_list));
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
        console.log('render_list', list);
        var table = elem(container, 'table');
        var tr = elem(table, 'tr');
        elem(tr, 'th', {text: 'Game Id'});
        elem(tr, 'th', {text: 'Type'});
        elem(tr, 'th', {text: 'Allowed Players'});
        for(var i=0; i<list.length; ++i){
          var game = list[i];
          var tr = elem(table, 'tr');
          elem(elem(tr, 'td'), 'a', {href: '/game/' + game.id + '/lobby', text: game.id});
          elem(tr, 'td', {text: game.paradigm});
          elem(tr, 'td', {text: game.min_players + " - " + game.max_players});
        }
      }
    </script>
  </head>
  <body>
    <hr>
    <h1> List Games </h1>
    <div id="main"></div>
    <hr>
  </body>
</html>