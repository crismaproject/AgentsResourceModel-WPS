var wpsApp = angular.module ("wpsApp", []);
var x2js = new X2JS();     


wpsApp.controller ('wpsCtrl', function ($scope, $http) {
    // test system:
    // $scope.wpsEndpoint = "http://pinguin2.ait.ac.at/~peter/indicators/pywps.cgi";
    // production system
    $scope.wpsEndpoint = "http://crisma.ait.ac.at/models/pywps.cgi";

    // list of indicators from WPS capabilities - to be updated from WPS Capabilities
    $scope.indicators = [];  // ["AgentsResourceModel"];
    $scope.indicator = null; // $scope.indicators[0];

    // example ICMM worldstate URL
    $scope.worldstateUrl = "http://crisma.cismet.de/pilotC/icmm_api/CRISMA.worldstates/2";

    // ask WPS for indicators (Processes in GetCapabilities)
    $scope.loadIndicators = function() {
	$http({
	    method: "GET",
	    url: $scope.wpsEndpoint + "?service=WPS&request=GetCapabilities"
	}).
	    success(function(data, status, headers, config) {
		// console.log (data);
		if (data != null) {
		    var response = x2js.xml_str2json (data)
		    // console.log (JSON.stringify (response));

		    var processes = response.Capabilities.ProcessOfferings.Process;
		    var indicators = [];

		    if (Array.isArray (processes)) {
			for (var i = 0; i < processes.length; i++) {
			    indicators.push (processes[i].Identifier.__text);
			}
		    } else {
			// let's asum tere is at least one process!
			indicators.push (processes.Identifier.__text);
		    }
		    $scope.indicators = indicators;
		    $scope.indicator = $scope.indicators.length > 0 ? $scope.indicators[0] : null;
		} else {
		    alert ("Got no Capabilities from WPS!");
		}
	    }).
	    error(function(data, status, headers, config) {
		alert ("WPS server " + $scope.wpsEndpoint + " not available");
	    });
    };

    $scope.loadIndicators();

});