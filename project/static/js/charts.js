
queue()
	.defer(d3.json, "/results")
	.await(makeGraphs);

function makeGraphs(error, resultsJson) {
	var streakResults = resultsJson;
	var dateFormat = d3.time.format("%Y%m%d");
	streakResults.forEach(function(d) {
		d["Date"] = dateFormat.parse(String(d["Date"]));
	});

	console.log("STRE: ", streakResults);

	var ndx = crossfilter(streakResults);

	var dateDim = ndx.dimension(function(d) { return d["Date"]; });
	var matchupDim = ndx.dimension(function(d) { return d["Matchup #"]; });
	var sportDim = ndx.dimension(function(d) { return d["Sport"]; });
	var matchupTimeDim = ndx.dimension(function(d) { return d["Matchup Time"]; });
	var winnerPctDim = ndx.dimension(function(d) { return d["Winner %"]; });

	var all = ndx.groupAll();
	var numResultsByDate = dateDim.group();
	var numResultsByMatchupNum = matchupDim.group();
	var numResultsBySport = sportDim.group();

	var dateChart = dc.barChart("#date-chart");
	var sportChart = dc.barChart("#sport-chart");

	var minDate = dateDim.bottom(1)[0]["Date"];
	var maxDate = dateDim.top(1)[0]["Date"];

	dateChart
		.width(600)
		.height(160)
		.margins({top: 10, right: 50, bottom: 30, left: 50})
		.dimension(dateDim)
		.group(numResultsByDate)
		.x(d3.time.scale().domain([minDate, maxDate]))
		.elasticY(true)
    	.xAxisLabel("Date")
    	.yAxis().ticks(4);

    sportChart
    	.width(300)
    	.height(250)
    	.dimension(sportDim)
    	.group(numResultsBySport)
    	.x()
    	.xAxis().ticks(4);

	dc.renderAll();

};
