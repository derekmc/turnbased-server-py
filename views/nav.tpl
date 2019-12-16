<span class="nav">
  <a href="/new"> New Game </a>
  <a href="/lists"> List Games </a>
  
  %if login_info['is_admin']:
    <a href="/admin"> Admin </a>
  %end
  %if login_info['logged_in']:
    <a href="/logout">Log Out</a>
  %else:
    <a href="/login">Log In</a>
  %end

</span>
