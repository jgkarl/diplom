function lookupAndCopy() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet1 = ss.getSheetByName('baas');
  var sheet2 = ss.getSheetByName('Sheet1');
  
  var data = sheet1.getDataRange().getValues();
  
  for (var i = 1; i < data.length; i++) { // Start from 1 to skip header row
    var token = data[i][columnToIndex('A')].substring(1);
    var col1 = data[i][columnToIndex('AK')];
    var col2 = data[i][columnToIndex('AL')];
    var col3 = data[i][columnToIndex('AM')];
    
    if (col1 || col2 || col3) {
      if (col1) {
        splitAndAppendRows(sheet2, token, col1);
      }
      if (col2) {
        splitAndAppendRows(sheet2, token, col2);
      }
      if (col3) {
        splitAndAppendRows(sheet2, token, col3);
      }
    }
  }
}


function columnToIndex(column) {
  var base = 'A'.charCodeAt(0);
  var index = 0;
  for (var i = 0; i < column.length; i++) {
    index = index * 26 + (column.charCodeAt(i) - base + 1);
  }
  return index - 1; // Convert to zero-based index
}

function splitAndAppendRows(sheet, token, value) {
  var values = value.split('.').map(function(part) {
    return part.trim();
  });
  for (var i = 0; i < values.length; i++) {
    if (values[i] != '') {
      sheet.appendRow([token, values[i]]);
    }
  }
}