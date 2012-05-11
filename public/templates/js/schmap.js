<script type="text/javascript">

clors = ['#80ac70','

function mapper()
{
  var i = 0;
  var c = 0
  {% for k,v in sections %}
    for(i=0;i<{{v.duration}};i++)
    {
      full = $('#cell{{v.day}}'+(parseInt({{v.hour}})+i)); 
      full.html(k);
      full.css({'background-color':colors[c]});
      c++;
    }
  {% endfor %}
}
</script>
