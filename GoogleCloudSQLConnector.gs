function onOpen() {
  var spreadsheet = SpreadsheetApp.getActive();
  var menuItems = [
    {name: 'Import requests', functionName: 'readFromRequestsTable'}
  ];
  spreadsheet.addMenu('Simple GAE App', menuItems);
}

// Replace the variables in this block with real values.
var address = '';
var user = '';
var userPwd = '';
var db = '';

var dbUrl = 'jdbc:mysql://' + address + '/' + db;

// Read up to 1000 rows of data from the table and log them.
function readFromRequestsTable() {
  var sheet = SpreadsheetApp.getActiveSheet();
  sheet.clear()
  
  var conn = Jdbc.getConnection(dbUrl, user, userPwd);
  
  var start = new Date();
  var stmt = conn.createStatement();
  // stmt.setMaxRows(1000);
  var results = stmt.executeQuery('SELECT * FROM requests');
  var numCols = results.getMetaData().getColumnCount();
  
  while (results.next()) {
    var listString = [];
    for (var col = 0; col < numCols; col++) {
      listString.push(results.getString(col + 1));
    }
    sheet.appendRow(listString);
  }

  results.close();
  stmt.close();
}
