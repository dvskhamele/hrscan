var domainName = "http://127.0.0.1:8000";
  //var domainName = "http://ec2-52-66-248-85.ap-south-1.compute.amazonaws.com:9001";
var keyvalues = [];
$('#addkey').click(function(){
  $(this).hide();
  $('#newkey').show();
  $('#closekey').show();
});

$(document).on('click', '#closekey', function(){
  $(this).hide();
  $('#newkey').hide();
  $('#addkey').show();
});

$(document).on('keypress', '#newkey', function(e){
  if(e.keyCode==13){
    var kw = $('#newkey');
    if(kw.val().length>1){
      $.get(domainName+'/adminpanel/addkeywords/'+kw.val(), function(data){
        //console.log(data);
        $("#keydata").prepend('<button class="btn btn-secondary" style="margin-bottom:3px;">'+kw.val()+'</button>');
        kw.val("");
        kw.hide();
        $('#addkey').show();
      }).fail(function(){
        alert('Server error');
        kw.val("");
        kw.hide();
        $('#addkey').show();
      });


    }
  }
});

var getData = function(){
  keyvalues = [];
  $.each($('.btn', '#keydata'),function(k){
    keyvalues.push({
      "k_value": $(this).text().trim()
    });
  });
  $('#key span').text("(Total "+keyvalues.length+" Keywords)");
  //console.log(keyvalues);
}
getData();

$(document).on('click', '#keydata .btn', function(){
  $(this).remove();
  getData();
});

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
  //  console.log(obj);
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
