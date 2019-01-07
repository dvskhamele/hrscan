//var domainName = "http://127.0.0.1:8000";
  var domainName = "http://ec2-52-66-248-85.ap-south-1.compute.amazonaws.com:9001";
var keyvalues = [];
var key_len = 0;
$('#skey').change(function(){
  var skey = $(this).find('option:selected').val();
  flg = 0;
  $.each(keyvalues, function(i, v) {
    if (v.k_value == skey) {
        flg = 1;
        console.log(v.k_value);
        return;
    }
  });
  if (flg==0){
    $('.keytable').append('<tr><td>'+(key_len+1)+'.</td><td><span class="badge badge-dark">'+skey+'</span></td><td><img src="/static/css/close.png" style="width:30px;cursor:pointer" alt=""></td></tr>');
    getData();
    $('#sinfo').removeClass('text-danger');
    $('#sinfo').addClass('text-success');
    $('#sinfo').html('<br/>'+skey+' is added');
    $('#sinfo').html('<br/>'+skey+' is already added');
  }else{
    $('#sinfo').removeClass('text-success');
    $('#sinfo').addClass('text-danger');
    $('#sinfo').html('<br/>'+skey+' is already added');
  }
  $('#skey').val("");
});

$(document).on('click', '#newkeybtn', function(e){
  var kw = $('#newkey').val();
  if(kw.length>1){
      $.get(domainName+'/adminpanel/addkeywords/'+kw, function(data){
        $('.keytable').append('<tr><td>'+(key_len+1)+'</td><td><span class="badge badge-dark">'+kw+'</span></td><td><img src="/static/css/close.png" style="width:30px;cursor:pointer" alt=""></td></tr>');
        $('#snew').removeClass('text-danger');
        $('#snew').addClass('text-success');
        $('#snew').text(kw+' is Added');
        getData();
      }).fail(function(){
        $('#snew').removeClass('text-success');
        $('#snew').addClass('text-danger');
        $('#snew').text('Server error');
      });
      $('#newkey').val("");
    }else {
      $('#snew').removeClass('text-success');
      $('#snew').addClass('text-danger');
      $('#snew').text('field is required');
    }
});
$(document).on('click', '.keytable img', function(e){
  var $tds = $(this).parent().parent().find('td');
  neuarr = [];
  $.each(keyvalues, function(i, v) {
    if (v.k_value != $tds.eq(1).text()) {
      neuarr.push({
        "k_value": v.k_value
      });
    }
  });
  keyvalues = neuarr;
  //console.log(keyvalues);
  key_len = keyvalues.length;
  $('#key span').text("(Total "+key_len+" Keywords)");
  $(this).parent().parent().remove();
});

var getData = function(){
  keyvalues = [];
  $('.keytable').find('tr').each(function (i, el) {
        var $tds = $(this).find('td');
        if($tds.eq(1).text()!=""){
          keyvalues.push({
            "k_value": $tds.eq(1).text()
          });
        }
    });
  key_len = keyvalues.length;
  $('#key span').text("(Total "+key_len+" Keywords)");
  //console.log(keyvalues);
}
getData();

$('#process').click(function(){
  //console.log(keyvalues);
  $(this).hide();
  //keyvalues
  $('.loader').fadeIn();
  $("#college").empty();
  $("#degree").empty();
  $("#keyword").empty();
  $("#overall").empty();
  $.post(domainName+'/adminpanel/api/v1/processcv',{'keyvalues[]': JSON.stringify(keyvalues)}, function(data){
    $('.loader').hide();
    $('#process').show();
    var obj = JSON.parse(data);
    console.log(obj);
    var clgRank = [];
    var degreeRank = [];
    var keywordRank = [];
    for(i=0;i<obj.collegeRank.length;i++){
      $.each( obj.collegeRank[i], function( key, value ) {
        $("#college").append('<tr><td></td><td><strong>'+key+"</strong></td><td>"+value+"</td></tr>");
        if(key!="college"){
          var min = Math.min.apply(null, value);
          clgRank.push({
            'name': key,
            'rank': (obj.college_count-min)
          });
        }
      });
      $("#college").append("<tr><td colspan='3'></td></tr>");
    }

    for(i=0;i<obj.degreeRank.length;i++){
      flg = 0;
      $.each( obj.degreeRank[i], function( key, value ) {
        if(value!=""){
          flg = 0;
          $("#degree").append('<tr><td><strong>'+key+"</strong></td><td>"+value+"</td></tr>");
          if(key!="degree"){
            var min = Math.min.apply(null, value);
            degreeRank.push({
              'name': key,
              'rank': (obj.degree_count-min)
            });
          }
        }else {
          flg = 1;
        }
      });
      if (flg==0){
        $("#degree").append("<tr><td colspan='3'></td></tr>");
      }
    }

    for(i=0;i<obj.keywordRank.length;i++){
      $.each( obj.keywordRank[i], function( key, value ) {
        if(key=='keywords'){
          $("#keyword").append('<tr><td><strong>'+key+"</strong></td><td>"+value+"</td></tr>");
        }else if(key=='keywordsCount'){
          $("#keyword").append('<tr><td><strong>'+key+"</strong></td><td>"+value+"</td></tr>");
        }else{
          $("#keyword").append('<tr><td><strong>'+key+"</strong></td><td>"+(value*100).toFixed(2)+"</td></tr>");
          keywordRank.push({
            'name': key,
            'rank': (value*100).toFixed(2)
          });
        }
      });
      $("#keyword").append("<tr><td colspan='2'></td></tr>");
    }
  //  keywordRank = sortJSON(keywordRank,'rank', '321');
    //clgRank = sortJSON(clgRank,'rank', '321');
    //grandArr = sortJSON(grandArr,'rank', '321');
    var grandArr = [];
    var tempArr = [keywordRank, clgRank, degreeRank];
    //console.log(tempArr);
    for(k=0;k<tempArr.length;k++){
      $.each( tempArr[k], function( key, value ) {
        flg=0;
        for(x=0;x<grandArr.length;x++){

          if(grandArr[x]['name']==value.name){
            flg=1;
            xvar = value.rank+"";
            //console.log(xvar.length);
            if (xvar.length>0){
              grandArr[x]['total'] = value.rank+ Number(grandArr[x]['total']);
              grandArr[x]['values'] = value.rank+" "+grandArr[x]['values'];
            }
          }
      }
      if(flg==0){
        grandArr.push({
          'name': value.name,
          'total': value.rank,
          'values': value.rank
        });
      }
      });
    }

    grandArr = sortJSON(grandArr,'total', '321');

    grandTotal = 0;
    $.each( grandArr, function( key, value ) {
      grandTotal += value.total;
    });
    var t_rank = 1;
    $("#overall").append('<tr><th>Rank</th><th>Name of Applicant</th><th>Total Score</th></tr>');
    $.each( grandArr, function( key, value ) {
      var per = (value.total*100)/grandTotal;
      $("#overall").append('<tr><td>'+(t_rank++)+'.</td><td>'+value.name+"</td><td>"+per.toFixed(2)+"%</td></tr>");
    });
  //  console.log(grandArr);
  //exportTableToExcel('overall', 'CVResults');
  }).fail(function(){
    alert('Server error try again after some time.');
    $('.loader').hide();
    $('#process').show();
  });

  var sortJSON = function sortJSON(data, key, way) {
    return data.sort(function(a, b) {
        var x = a[key]; var y = b[key];
        if (way === '123' ) { return ((x < y) ? -1 : ((x > y) ? 1 : 0)); }
        if (way === '321') { return ((x > y) ? -1 : ((x < y) ? 1 : 0)); }
    });
  }
});


function exportTableToExcel(tableID, filename = ''){
  var downloadLink;
  var dataType = 'application/vnd.ms-excel';
  var tableSelect = document.getElementById(tableID);
  var tableHTML = tableSelect.outerHTML.replace(/ /g, '%20');

  // Specify file name
  filename = filename?filename+'.xls':'excel_data.xls';

  // Create download link element
  downloadLink = document.createElement("a");

  document.body.appendChild(downloadLink);

  if(navigator.msSaveOrOpenBlob){
      var blob = new Blob(['\ufeff', tableHTML], {
          type: dataType
      });
      navigator.msSaveOrOpenBlob( blob, filename);
  }else{
      // Create a link to the file
      downloadLink.href = 'data:' + dataType + ', ' + tableHTML;

      // Setting the file name
      downloadLink.download = filename;

      //triggering the function
      downloadLink.click();
  }
}
